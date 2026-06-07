import subprocess
import os

video_path = "D:/ML/Lab1/media/videos/scene_2_1/480p15/Scene2_1.mp4"
out_dir = "C:/Users/User/.gemini/antigravity/brain/5755ff54-b826-44d5-99e7-db5a41985575/.tempmediaStorage"
os.makedirs(out_dir, exist_ok=True)

for t in range(35, 60, 2):
    out_path = f"{out_dir}/extracted_end_{t}s.png"
    cmd = f'ffmpeg -y -ss {t} -i "{video_path}" -vframes 1 -q:v 2 "{out_path}"'
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        print(f"Extracted frame at {t}s!")
