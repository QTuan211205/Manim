import subprocess
import os

video_path = "D:/ML/Lab1/media/videos/scene_2_1/480p15/Scene2_1.mp4"
out_dir = "C:/Users/User/.gemini/antigravity/brain/5755ff54-b826-44d5-99e7-db5a41985575/.tempmediaStorage"
os.makedirs(out_dir, exist_ok=True)

timestamps = [12, 15, 35]
for t in timestamps:
    out_path = f"{out_dir}/extracted_lowres_{t}s.png"
    cmd = f'ffmpeg -y -ss {t} -i "{video_path}" -vframes 1 -q:v 2 "{out_path}"'
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"{t}s frame extracted to {out_path}!")
