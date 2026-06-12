# Manim Scenes - Beyond Decoding

Repository này chứa mã nguồn [Manim Community Edition](https://www.manim.community/) để dựng các scene cho video **"Beyond Decoding: Meta-Generation Algorithms for Large Language Models"**.

Nội dung chính được tổ chức theo chương và scene trong thư mục `content/`.

## Cấu Trúc Dự Án

```text
.
├── content/
│   ├── chapter<N>/
│   │   ├── scene_<N>.<M>/
│   │   │   ├── scene_<N>_<M>.py      # Code tạo scene Manim
│   │   │   ├── script.md             # Kịch bản/nội dung thuyết minh nếu có
│   │   │   ├── assets/               # Tài nguyên riêng của scene nếu có
│   │   │   └── media/                # Output render của scene nếu render từ thư mục scene
│   │   └── chapter<N>_concat.txt     # Danh sách file để ghép video chương nếu có
│   └── images/                       # Tài nguyên hình ảnh dùng chung nếu có
├── slide/                            # Tài liệu, slide tham khảo
├── subtitle/                         # Phụ đề
├── full_video_script.md              # Kịch bản tổng thể
├── scripts/                          # Script hỗ trợ render/ghép video nếu có
└── README.md
```

Trong đó:

| Thành phần | Quy ước tổng quát | Ví dụ |
| --- | --- | --- |
| Thư mục chapter | `content/chapter<N>/` | `content/chapter3/` |
| Thư mục scene | `content/chapter<N>/scene_<N>.<M>/` | `content/chapter3/scene_3.1/` |
| File code tạo scene | `content/chapter<N>/scene_<N>.<M>/scene_<N>_<M>.py` | `content/chapter3/scene_3.1/scene_3_1.py` |
| Class Manim | `Scene<N>_<M>` | `Scene3_1` |
| Output khi render từ thư mục scene | `content/chapter<N>/scene_<N>.<M>/media/videos/scene_<N>_<M>/<quality>/` | `content/chapter3/scene_3.1/media/videos/scene_3_1/480p15/` |

## Cài Đặt

Cài Python, FFmpeg và Manim CE:

```bash
pip install manim
```

Nếu dùng virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install manim
```

Trên Windows, lệnh kích hoạt môi trường ảo thường là:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Render Scene

Render một scene bằng cách đi vào đúng thư mục scene rồi chạy `manim` với file Python và class tương ứng.

Mẫu lệnh tổng quát:

```bash
cd content/chapter<N>/scene_<N>.<M>
manim -pql scene_<N>_<M>.py Scene<N>_<M>
```

Ví dụ render nhanh scene 3.1:

```bash
cd content/chapter3/scene_3.1
manim -pql scene_3_1.py Scene3_1
```

Render chất lượng cao:

```bash
manim -pqh scene_3_1.py Scene3_1
```

Các flag thường dùng:

| Flag | Ý nghĩa |
| --- | --- |
| `-p` | Mở video sau khi render xong |
| `-ql` | Render nhanh chất lượng thấp, thường ra `480p15` |
| `-qm` | Render chất lượng trung bình |
| `-qh` | Render chất lượng cao, thường ra `1080p60` |

## Đường Dẫn Scene Được Tạo

Khi render từ trong thư mục scene, Manim tạo output theo cấu trúc:

```text
content/chapter<N>/scene_<N>.<M>/media/videos/scene_<N>_<M>/<quality>/Scene<N>_<M>.mp4
```

Ví dụ:

```text
content/chapter3/scene_3.1/media/videos/scene_3_1/480p15/Scene3_1.mp4
content/chapter3/scene_3.1/media/videos/scene_3_1/1080p60/Scene3_1.mp4
```

Nếu render từ thư mục khác, Manim có thể tạo `media/` tại thư mục đang chạy lệnh. Để output nằm cạnh scene, nên luôn `cd` vào thư mục scene trước khi render.

## Kiểm Tra Nhanh

Kiểm tra cú pháp Python cho một scene:

```bash
python -m py_compile content/chapter<N>/scene_<N>.<M>/scene_<N>_<M>.py
```

Ví dụ:

```bash
python -m py_compile content/chapter3/scene_3.1/scene_3_1.py
```

## Quy Ước Khi Thêm Scene Mới

Khi thêm scene mới, giữ đồng bộ tên thư mục, file và class:

```text
content/chapter4/scene_4.2/scene_4_2.py
```

```python
class Scene4_2(Scene):
    ...
```

Nếu scene dùng text hoặc TeX, giữ cấu hình thư mục tạm để tránh lỗi quyền ghi cache:

```python
import os
import tempfile
from manim import config

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
```

Không commit các file sinh ra tự động như `__pycache__/`, `media/`, `partial_movie_files/` hoặc output render tạm, trừ khi cần lưu một bản mẫu có chủ đích.

## Tài Nguyên Liên Quan

- `full_video_script.md`: kịch bản tổng thể của video.
- `slide/`: slide và tài liệu tham khảo.
- `subtitle/`: phụ đề.
- `scripts/`: script hỗ trợ render hoặc xử lý video nếu có.
