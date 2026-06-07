import subprocess
import os

video_path = "C:/Users/User/.gemini/antigravity/brain/5755ff54-b826-44d5-99e7-db5a41985575/Scene2_1.mp4"
out_dir = "C:/Users/User/.gemini/antigravity/brain/5755ff54-b826-44d5-99e7-db5a41985575/.tempmediaStorage"
os.makedirs(out_dir, exist_ok=True)

out_path = f"{out_dir}/extracted_scene_2_1_12s.png"
cmd = f'ffmpeg -y -ss 12 -i "{video_path}" -vframes 1 -q:v 2 "{out_path}"'
subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("12s frame extracted!")
