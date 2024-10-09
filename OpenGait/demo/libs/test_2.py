import uuid
import configparser
import aiohttp
import asyncio
import aiofiles
import os
from aiohttp import ClientError
import pickle
from utils_server.api_server import *
from pathlib import Path
person_log_file = "demo/logs/log_person.txt"
error_log_file = "demo/logs/log_error.log"
compare_log_file = "demo/logs/log_compare.txt"
log_track_segment_img_file = "demo/logs/log_track_segment_img.txt"

for log_file in [compare_log_file, person_log_file, error_log_file, log_track_segment_img_file]:
    with open(log_file, "w") as f:
        pass

import logging
logging.basicConfig(filename=error_log_file, level=logging.ERROR)

config = configparser.ConfigParser()
current_script_directory = os.path.dirname(os.path.abspath(__file__))
config.read(current_script_directory +'/config.ini')
host_ip = config['DEFAULT']['host'] 
seg_port_num = config['DEFAULT']['seg_port_num'] 
rec_port_num = config['DEFAULT']['rec_port_num']
seg_url = f"http://{host_ip}:{seg_port_num}/segment-no-video"
rec_url = f"http://{host_ip}:{rec_port_num}/extract-sil-function-v0"

min_segment_valid = 5 
segment_frame_skip = 4
min_track_frame_sequence = (min_segment_valid-1)*segment_frame_skip +1 
folder_track = os.path.join(os.path.dirname(current_script_directory),"output/TrackingResultTest")

p = "demo/libs/pickle_variables"
q = os.path.join(p, "people_session_info")
os.makedirs(q, exist_ok=True)

async def log_person(item):
    async with aiofiles.open(person_log_file, "a") as f:
        await f.write(f'{item}\n')

async def log_compare(item):
    async with aiofiles.open(compare_log_file, "a") as f:
        await f.write(f'{item}',"\n")



# Fetch with retries
async def fetch_with_retries(session, url, data, retries=3, backoff_factor=0.5):
    for attempt in range(retries):
        try:
            async with session.post(url, data=data) as response:
                response.raise_for_status()  # Raise exception for bad status
                return await response.json()
        except (ClientError, asyncio.TimeoutError) as e:
            if attempt < retries - 1:
                wait_time = backoff_factor * (2 ** attempt)
                print(f"Attempt {attempt + 1} failed for {url}. Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                logging.error(f"All {retries} attempts failed for {url} with data: {data}")
                print(f"All {retries} attempts failed for {url}.")
                raise e

# Segment video
async def segment_video(person_folder_track_path, session):
    payload = {'folder_track_path': person_folder_track_path, 'frame_skip_num': '0'}
    response_json = await fetch_with_retries(session, seg_url, payload)
    sil_pickle_path = response_json["result"]["sil_pickle_path"]
    return person_folder_track_path, sil_pickle_path

# Extract embedding
async def extract_embed(person_folder_track_path, sil_path, session):
    payload = {'sil_pickle_path': sil_path}
    response_json = await fetch_with_retries(session, rec_url, payload)
    embedding_path = response_json["result"]["embedding_path"]
    return embedding_path
async def process_video(person, session, sem):
    async with sem:
        try:
            item = person.person_folder_track_path
            person_folder_track_path, sil_path = await segment_video(item, session)
            person.update_folder_track_path(person_folder_track_path)
            person.update_sil_pickle_path(sil_path)
            embedding_path = await extract_embed(person_folder_track_path, sil_path, session)
            person.update_embedding_path(embedding_path)
            person.mark_processed()
            return person
        except asyncio.TimeoutError:
            logging.error(f"Timeout processing {item}")
            print(f"Timeout processing {item}")
            return None
        except ClientError as e:
            logging.error(f"Client error processing {item}: {e}")
            print(f"Client error processing {item}: {e}")
            return None
        except Exception as e:
            person.set_error(str(e))
            logging.error(f"Unexpected error processing {item}: {e}")
            print(f"Unexpected error processing {item}: {e}")
            return None

# Process list of videos
async def process_video_list(person_ls, session):
    sem = asyncio.Semaphore(10)  # Limit to 10 concurrent tasks
    tasks = []
    for person in person_ls:
        person_object = process_video(person, session, sem)
        tasks.append(person_object)
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
# Main entry point
async def main(person_ls):

    timeout = aiohttp.ClientTimeout(total=1200)  # Adjust as needed
    connector = aiohttp.TCPConnector(limit=10)  # Limit concurrent connections
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        results = await process_video_list(person_ls, session)
    return results

class Person:
    def __init__(self, video_folder_track_path=None, person_folder_track_path=None, person_type=None, sil_pickle_path=None, embedding_path=None):
        self.id = str(uuid.uuid4())  # Generate a unique ID using UUID
        self.video_folder_track_path = video_folder_track_path
        self.person_folder_track_path = person_folder_track_path
        self.type = person_type
        self.sil_pickle_path = sil_pickle_path
        self.embedding_path = embedding_path
        self.processed = False
        self.error_message = None

    def update_video_folder_track_path(self, path):
        self.video_folder_track_path = fix_path(path)

    def update_folder_track_path(self, path):
        self.person_folder_track_path = fix_path(path)

    def update_type(self, type):
        self.type = type
    def update_sil_pickle_path(self, path):
        self.sil_pickle_path = fix_path(path)

    def update_embedding_path(self, path):
        self.embedding_path = fix_path(path)

    def mark_processed(self):
        self.processed = True

    def set_error(self, error_message):
        self.error_message = error_message

    def get_status(self):
        if self.processed:
            return "Processed successfully"
        elif self.error_message:
            return f"Error: {self.error_message}"
        else:
            return "Pending"
    def get_attributes(self):
        return self.__dict__

    def __repr__(self):
    
        return f"Person(ID={self.id}, processed={self.processed}, error={self.error_message})"

if __name__ == "__main__":
    track_folder_ls = []
    person_ls = []
    for video_folder_track_path in os.listdir(folder_track):
        tmp = os.path.join(folder_track, video_folder_track_path)
        for filename in os.listdir(tmp):
            person_folder_track_path = os.path.join(tmp, filename)
            if len(os.listdir(person_folder_track_path)) < min_track_frame_sequence:
                continue
            person = Person(video_folder_track_path=video_folder_track_path, person_folder_track_path=person_folder_track_path)
            person_ls.append(person)  # Add the person  # Use the generated ID as the key
                    
    # Run the asynchronous processing for all videos
    try:
        results = asyncio.run(main(person_ls))
    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
        print(f"An error occurred during processing: {e}")

    # Optionally, handle results
    successful = [res for res in results if res is not None]
    print(f"Successfully processed {len(successful)} out of {len(person_ls)} videos.")
    save_info_pkl = os.path.join(q, str(uuid.uuid4()) + ".pkl")
    save_info_ls = []
    # Log the attributes of each Person object to a file
    with open(person_log_file, "a") as log_file:  # Open the file in append mode
        for person in results:
            # Get the full attributes of the person object
            if isinstance(person, Exception):  # Spot exceptions
                print(f"Task raised an exception: {person}")
                continue
            person_attributes = person.get_attributes()
            save_info_ls.append(person_attributes)
            # Write the ID and attributes to the file
            log_file.write(f"Attributes: {person_attributes}\n")
            log_file.write('-----------------------------------------------------\n')
    with open (log_track_segment_img_file, "a") as f:
                for index, person in enumerate(results):
                    f.write (f"Item {index}:\n")
                    if isinstance(person, Exception):  # Spot exceptions
                        print(f"Task raised an exception: {person}")
                        continue
                    person_folder_track_path = person.person_folder_track_path
                    f.write(f"{person_folder_track_path}\n")
                    sil_folder = os.path.join(os.path.dirname(current_script_directory),"output/GaitSilhouette", Path(person.sil_pickle_path).name.split(".")[0])
                    f.write(f"{fix_path(sil_folder)}\n")
                    f.write('-----------------------------------------------------\n')

    with open(save_info_pkl, "wb") as f:
        pickle.dump(save_info_ls, f)
    print (f"Saved people results to {save_info_pkl}")

