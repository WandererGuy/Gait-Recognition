import requests

# Define the URL and the data
track_url = "http://10.0.68.103:8010/track"  # Replace with your FastAPI server's URL if different
data = {
    "probe_video_path": "./demo/output/InputVideos/probe1.mp4"
}

seg_url = "http://10.0.68.103:8011/segment"  # Replace with your FastAPI server's URL if different
# Send the POST request
track_response = requests.post(track_url, json=data)
track_result = track_response.json()["track_result"]

# # Send the POST request
# seg_response = requests.post(seg_url, json=track_result)
# seg_result = seg_response.json()["seg_result"]