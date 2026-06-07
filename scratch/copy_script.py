import shutil

src = r"d:\ML\Lab1\full_video_script.md"
dst = r"C:\Users\User\.gemini\antigravity\brain\5755ff54-b826-44d5-99e7-db5a41985575\full_video_script.md"

shutil.copy(src, dst)
print("Successfully copied full_video_script.md to brain folder.")
