# import os 
# pre = '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD'
# for filename in os.listdir(pre):
#     for filename2 in os.listdir(os.path.join(pre, filename)):
#         print ("'" + os.path.join(pre, filename, filename2) + "',")
        
# pre = '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau SS'
# for filename in os.listdir(pre):
#         print ("'" + os.path.join(pre, filename) + "',")



# import requests

# url = "http://10.0.68.103:2001/tracking"

# video_paths=(
# '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 4 ngay 24-3-2021/5167526383877495248.mp4',
# '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 1/C0103.MP4',
# '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 3 ngay 22-11-2020/8300278661057155957.mp4',
# '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 3 ngay 22-11-2020/7180747282665697279.mp4',
# '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 5 ngay 30-11-2020/5234757553247363443.mp4',
# '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 2 ngay 02-11-2020/8328534836514339442.mp4',
# '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau GD/Doi tuong 2 ngay 02-11-2020/5652104598115489538 (1).mp4',
# '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau SS/di vao 01h28p.mp4',
# '/home/ai-ubuntu/hddnew/Manh/GAIT_RECOG/dang_di_sample/Mau SS/di ra 03h13p.mp4'    # Add more image paths here
# )
# with open ("output_log.txt", "a") as file:
#     for video in video_paths:
        
#         payload = {'video_path': video}
#         files=[

#         ]
#         headers = {}

#         response = requests.request("POST", url, headers=headers, data=payload, files=files)
#         file.write(video)
#         file.write('\n')
#         file.write(response.text)
#         file.write('\n')
#         file.write('-----------------------------------------------------------\n')


## script to send message 