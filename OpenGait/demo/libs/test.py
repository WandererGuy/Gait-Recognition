# from segment import *

# video_path = "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 4 ngay 24-3-2021/5167526383877495248.mp4"
# track_result_pickle = "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/libs/pickle_variables/track/bed0c427-6a0d-4968-ab96-5cfaf8074862"
# track_crop(vdieo_path, track_result_pickle)


# video_dict = {
# "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 4 ngay 24-3-2021/5167526383877495248.mp4":"/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/libs/pickle_variables/track/bed0c427-6a0d-4968-ab96-5cfaf8074862",

# "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 1/C0103.MP4":"/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/libs/pickle_variables/track/622675fe-380a-4de4-8da2-6756b433b919",

# "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 3 ngay 22-11-2020/8300278661057155957.mp4":"/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/libs/pickle_variables/track/58c2dd82-f19d-4087-9a2c-61f117de46b9",

# "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 3 ngay 22-11-2020/7180747282665697279.mp4":"/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/libs/pickle_variables/track/1132b021-8bc2-4099-8150-21e229444885",

# "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 5 ngay 30-11-2020/5234757553247363443.mp4":"/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/libs/pickle_variables/track/a7c0dfa5-0b4d-491c-9121-de743c405768",

# "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 2 ngay 02-11-2020/8328534836514339442.mp4":"/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/libs/pickle_variables/track/0587f470-135a-498c-8952-786509ffde75",

# "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 2 ngay 02-11-2020/5652104598115489538 (1).mp4":"/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/libs/pickle_variables/track/4b71fd79-b249-4850-a2bc-54c9273360ae",

# "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau SS/di vao 01h28p.mp4":"/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/libs/pickle_variables/track/82a76341-8a70-4dbc-9e78-77effc208d44",

# "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau SS/di ra 03h13p.mp4":"/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/libs/pickle_variables/track/2112f758-19ce-4efa-8efc-374590ad77c2"

# }
# for key, value in video_dict.items():
#     track_crop(key, value)



import requests
import json 
# def extract_embed(sil_path):

#     url = "http://10.0.68.103:2003/extract-sil-function"

#     payload = {'sil_pickle_path': sil_path}
#     files=[

#     ]
#     headers = {}

#     response = requests.request("POST", url, headers=headers, data=payload, files=files)
#     info = response.json()["result"]["embedding_path"]
#     with open ("demo/log_rec.txt", "a") as f:
#         f.write ('sil_pickle_path' + sil_path + '\n')
#         f.write("embedding_path" + info + '\n')
#         f.write('-------------')
#     return info 



# # item = "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/TrackingResult/di ra 03h13p/001"
# def segment_video(item):
#     url = "http://10.0.68.103:2002/segment-no-video"

#     payload = {'folder_track_path': item,
#     'frame_skip_num': '4'}
#     files=[

#     ]
#     headers = {}

#     response = requests.request("POST", url, headers=headers, data=payload, files=files)
#     info = response.json()["result"]["sil_pickle_path"]
#     with open ("demo/log_segment.txt", "a") as f:
#         f.write ('folder_track_path'+ item + '\n')
#         f.write("sil_pickle_path" + info + '\n')
#         f.write('-------------')
#     return info 


import aiohttp
import asyncio
import aiofiles
import os
from aiohttp import ClientError

# Asynchronous logging functions
async def log_segment(folder_track_path, sil_pickle_path):
    async with aiofiles.open("demo/log_segment.txt", "a") as f:
        await f.write(f'folder_track_path {folder_track_path}\n')
        await f.write(f"sil_pickle_path {sil_pickle_path}\n")
        await f.write('-------------\n')

async def log_rec(folder_track_path, sil_path, embedding_path):
    async with aiofiles.open("demo/log_rec.txt", "a") as f:
        await f.write(f'folder_track_path {folder_track_path}\n')
        await f.write(f'sil_pickle_path {sil_path}\n')
        await f.write(f"embedding_path {embedding_path}\n")
        await f.write('-------------\n')

async def log_rec_dict(item, embedding_path):
    async with aiofiles.open("demo/log_rec_dict.txt", "a") as f:
        await f.write(f"'{item}':'{embedding_path}',\n")



import logging

# Configure logging
logging.basicConfig(filename="demo/log_error.log", level=logging.ERROR)

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
async def segment_video(folder_track_path, session):
    url = "http://10.0.68.103:2002/segment-no-video"
    payload = {'folder_track_path': folder_track_path, 'frame_skip_num': '4'}
    response_json = await fetch_with_retries(session, url, payload)
    sil_pickle_path = response_json["result"]["sil_pickle_path"]
    await log_segment(folder_track_path, sil_pickle_path)
    return folder_track_path, sil_pickle_path

# Extract embedding
async def extract_embed(folder_track_path, sil_path, session):
    url = "http://10.0.68.103:2003/extract-sil-function"
    payload = {'sil_pickle_path': sil_path}
    response_json = await fetch_with_retries(session, url, payload)
    embedding_path = response_json["result"]["embedding_path"]
    await log_rec(folder_track_path, sil_path, embedding_path)
    return embedding_path

# Process a single video
async def process_video(item, session, sem):
    async with sem:
        try:
            folder_track_path, sil_path = await segment_video(item, session)
            embedding_path = await extract_embed(folder_track_path, sil_path, session)
            await log_rec_dict(item, embedding_path)
            print(f"Processed video {item} -> Embedding path: {embedding_path}")
            return embedding_path
        except asyncio.TimeoutError:
            logging.error(f"Timeout processing {item}")
            print(f"Timeout processing {item}")
            return None
        except ClientError as e:
            logging.error(f"Client error processing {item}: {e}")
            print(f"Client error processing {item}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error processing {item}: {e}")
            print(f"Unexpected error processing {item}: {e}")
            return None

# Process list of videos
async def process_video_list(video_list, session):
    sem = asyncio.Semaphore(10)  # Limit to 10 concurrent tasks
    tasks = [process_video(item, session, sem) for item in video_list]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# Main entry point
async def main(video_list):
    timeout = aiohttp.ClientTimeout(total=1200)  # Adjust as needed
    connector = aiohttp.TCPConnector(limit=10)  # Limit concurrent connections
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        results = await process_video_list(video_list, session)
    return results

if __name__ == "__main__":
    min_frame_sequence = 10
    folder_track = "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/TrackingResult"
    ls = []
    for filename in os.listdir(folder_track):
        video_folder = os.path.join(folder_track, filename)
        for filename2 in os.listdir(video_folder):
            object_folder = os.path.join(video_folder, filename2)
            if len(os.listdir(object_folder)) < min_frame_sequence:
                continue
            ls.append(object_folder)
    ls = ["/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/TrackingResult/5652104598115489538 (1)/004", 
          "/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/OpenGait/demo/output/TrackingResult/C0103/002"]
    video_list = ls
    # Clear log files
    # for log_file in ["demo/log_rec_dict.txt", "demo/log_rec.txt", "demo/log_segment.txt", "demo/log_error.txt"]:
    #     with open(log_file, "w") as f:
    #         pass
    
    # Run the asynchronous processing for all videos
    try:
        results = asyncio.run(main(video_list))
    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
        print(f"An error occurred during processing: {e}")
    
    # Optionally, handle results
    successful = [res for res in results if res is not None]
    print(f"Successfully processed {len(successful)} out of {len(video_list)} videos.")
