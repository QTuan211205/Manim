import os
import time

video_path = "D:/ML/Lab1/media/videos/scene_2_1/480p15/Scene2_1.mp4"
img_path = "C:/Users/User/.gemini/antigravity/brain/5755ff54-b826-44d5-99e7-db5a41985575/.tempmediaStorage/extracted_lowres_15s.png"

if os.path.exists(video_path):
    print("Video modified time:", time.ctime(os.path.getmtime(video_path)))
else:
    print("Video does not exist!")

if os.path.exists(img_path):
    print("Image modified time:", time.ctime(os.path.getmtime(img_path)))
else:
    print("Image does not exist!")
