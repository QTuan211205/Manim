# Hướng Dẫn Cài Đặt và Chạy Dự Án Manim (Beyond Decoding)

Dự án này chứa mã nguồn [Manim (Community Edition)](https://www.manim.community/) để dựng các phân cảnh hoạt họa (visualizations) cho bài báo **"Beyond Decoding: Meta-Generation Algorithms for Large Language Models"** (gồm các Chương từ 1 đến 5).

---

## 1. Yêu Cầu Hệ Thống & Cài Đặt Phần Mềm

Để chạy được các kịch bản Manim trong dự án này trên hệ điều hành Windows, bạn cần cài đặt **Python**, **FFmpeg** (để xuất video), và thư viện **Manim**.

### Bước 1: Cài đặt Python
* Tải và cài đặt **Python (phiên bản khuyên dùng: 3.9 đến 3.12)** từ trang chủ [python.org](https://www.python.org/downloads/).
* **QUAN TRỌNG:** Trong quá trình cài đặt, hãy tích chọn ô **"Add Python to PATH"** trước khi nhấn Install.

### Bước 2: Cài đặt FFmpeg (Bắt buộc để Manim biên dịch video)
Manim cần FFmpeg để xử lý và xuất các tệp video (`.mp4`).
* **Cách 1 (Nhanh nhất qua winget):** Mở CMD/PowerShell và chạy:
  ```powershell
  winget install Gyan.FFmpeg
  ```
* **Cách 2 (Qua Chocolatey):** Nếu bạn sử dụng Chocolatey:
  ```powershell
  choco install ffmpeg
  ```
* **Cách 3 (Qua Scoop):** Nếu bạn sử dụng Scoop:
  ```powershell
  scoop install ffmpeg
  ```
* **Cách 4 (Cài đặt thủ công):**
  1. Tải FFmpeg bản build sẵn cho Windows từ [ffmpeg.org](https://ffmpeg.org/download.html).
  2. Giải nén thư mục và copy đường dẫn đến thư mục `bin` (ví dụ: `C:\ffmpeg\bin`).
  3. Thêm đường dẫn này vào biến môi trường **PATH** của hệ thống (System Environment Variables).

### Bước 3: Cài đặt thư viện Manim
Mở PowerShell/Terminal của bạn và chạy lệnh cài đặt Manim CE:
```powershell
pip install manim
```
*Lưu ý: Lệnh này cũng tự động cài đặt các thư viện bổ trợ cần thiết như NumPy, SciPy, và Pillow.*

---

## 2. Cấu Trúc Thư Mục Dự Án

```text
D:\ML\Lab1\
├── chapter1/                     # Chương 1: Giới thiệu & Vai trò của Test-time Compute
│   ├── scene_1.1/                # Phân cảnh 1.1: Giới thiệu chung (Beyond Decoding)
│   ├── scene_1.2/                # Phân cảnh 1.2: Mô phỏng Auto-regressive Generation
│   ├── scene_1.3/                # Phân cảnh 1.3: So sánh Standard Decoding & Test-Time Compute
│   └── scene_1.4/                # Phân cảnh 1.4: Bản chất tạo chuỗi cho mọi tác vụ (Sequence Generation)
├── chapter2/                     # Chương 2: Token-Level Generators (Bộ tạo mức Token)
│   ├── scene_2.1/                # Phân cảnh 2.1: Các khái niệm cơ bản (Decoding as Search)
│   ├── scene_2.2/                # Phân cảnh 2.2: Thuật toán Greedy & Beam Search
│   ├── scene_2.3/                # Phân cảnh 2.3: Phân bố xác suất & Nhiệt độ (Temperature)
│   ├── scene_2.4/                # Phân cảnh 2.4: Các kỹ thuật Sampling (Top-k, Top-p)
│   └── scene_2.5/                # Phân cảnh 2.5: Constrained Decoding (Giải mã có ràng buộc)
├── chapter3/                     # Chương 3: Meta-Generation Algorithms (Thuật toán Meta-Generation)
│   ├── scene_3.1/                # Phân cảnh 3.1: Tổng quan về Meta-Generators (Hệ điều hành LLM OS)
│   ├── scene_3.2/                # Phân cảnh 3.2: Các thuật toán chọn mẫu nâng cao (Best-of-N, Voting...)
│   ├── scene_3.3/                # Phân cảnh 3.3: Lập luận nhiều bước & Verifiers (Outcome/Process Verifiers)
│   └── scene_3.4/                # Phân cảnh 3.4: Bản đồ thiết kế thuật toán sinh (Design Space of Generators)
├── chapter4/                     # Chương 4: Search & Planning (Tìm kiếm và Lập kế hoạch nâng cao)
│   ├── scene_4.1/                # Phân cảnh 4.1: Tìm kiếm trên cây Monte Carlo (MCTS)
│   ├── scene_4.2/                # Phân cảnh 4.2: Tối ưu hóa suy luận (Inference Optimization)
│   └── scene_4.3/                # Phân cảnh 4.3: Luồng lập kế hoạch Llama-style & Kết luận
├── chapter5/                     # Chương 5: Lời Kết & Thảo Luận
│   └── scene_5.1/                # Phân cảnh 5.1: Panel Discussion & Outro
├── media/                        # Thư mục chứa hình ảnh/video đầu ra sau khi render
├── slide/                        # Chứa các tài liệu, slides gốc của bài giảng
├── subtitle/                     # Chứa các tệp phụ đề (.srt) tương ứng
├── full_video_script.md          # Kịch bản chi tiết thuyết minh và lời thoại cho toàn bộ video
└── README.md                     # Hướng dẫn này
```

---

## 3. Hướng Dẫn Biên Dịch (Render) Video

Mỗi phân cảnh trong các chương là một Class Manim kế thừa từ `Scene`. Để render, bạn di chuyển (`cd`) vào thư mục chứa file Python đó và thực hiện lệnh biên dịch.

### Các tham số cấu hình biên dịch thông dụng:
* `-p`: Tự động mở video sau khi render xong (Play).
* `-ql`: Biên dịch chất lượng thấp (Low Quality - 480p, 15 FPS) giúp xem nhanh và kiểm tra giao diện.
* `-qh`: Biên dịch chất lượng cao (High Quality - 1080p, 60 FPS) phục vụ cho sản xuất/xuất bản.

### Danh sách lệnh chạy chi tiết cho từng Scene:

| Phân Cảnh | Lệnh Biên Dịch Nhanh (Xem thử) | Lệnh Biên Dịch Chất Lượng Cao (Xuất bản) |
| :--- | :--- | :--- |
| **Scene 1.1** | `manim -pql scene_1_1.py Scene1_1` | `manim -pqh scene_1_1.py Scene1_1` |
| **Scene 1.2** | `manim -pql scene_1_2.py Scene1_2` | `manim -pqh scene_1_2.py Scene1_2` |
| **Scene 1.3** | `manim -pql scene_1_3.py Scene1_3` | `manim -pqh scene_1_3.py Scene1_3` |
| **Scene 1.4** | `manim -pql scene_1_4.py Scene1_4` | `manim -pqh scene_1_4.py Scene1_4` |
| **Scene 2.1** | `manim -pql scene_2_1.py Scene2_1` | `manim -pqh scene_2_1.py Scene2_1` |
| **Scene 2.2** | `manim -pql scene_2_2.py Scene2_2` | `manim -pqh scene_2_2.py Scene2_2` |
| **Scene 2.3** | `manim -pql scene_2_3.py Scene2_3` | `manim -pqh scene_2_3.py Scene2_3` |
| **Scene 2.4** | `manim -pql scene_2_4.py Scene2_4` | `manim -pqh scene_2_4.py Scene2_4` |
| **Scene 2.5** | `manim -pql scene_2_5.py Scene2_5` | `manim -pqh scene_2_5.py Scene2_5` |
| **Scene 3.1** | `manim -pql scene_3_1.py Scene3_1` | `manim -pqh scene_3_1.py Scene3_1` |
| **Scene 3.2** | `manim -pql scene_3_2.py Scene3_2` | `manim -pqh scene_3_2.py Scene3_2` |
| **Scene 3.3** | `manim -pql scene_3_3.py Scene3_3` | `manim -pqh scene_3_3.py Scene3_3` |
| **Scene 3.4** | `manim -pql scene_3_4.py Scene3_4` | `manim -pqh scene_3_4.py Scene3_4` |
| **Scene 4.1** | `manim -pql scene_4_1.py Scene4_1` | `manim -pqh scene_4_1.py Scene4_1` |
| **Scene 4.2** | `manim -pql scene_4_2.py Scene4_2` | `manim -pqh scene_4_2.py Scene4_2` |
| **Scene 4.3** | `manim -pql scene_4_3.py Scene4_3` | `manim -pqh scene_4_3.py Scene4_3` |
| **Scene 5.1** | `manim -pql scene_5_1.py Scene5_1` | `manim -pqh scene_5_1.py Scene5_1` |

---

## 4. Giải Quyết Một Số Lỗi Thường Gặp (Troubleshooting)

### 1. Lỗi phân quyền ghi tệp (Access is Denied) trên Windows
Các tệp text và công thức của Manim mặc định ghi vào thư mục temp hoặc cache của hệ thống. Để khắc phục, toàn bộ mã nguồn của dự án này đã thiết lập chuyển hướng thư mục tạm vào bộ nhớ dùng chung của Windows:
```python
import os
import tempfile
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
```
Nếu bạn vẫn gặp lỗi phân quyền, hãy đảm bảo terminal của bạn đang chạy ở quyền User bình thường và không bị khóa bởi phần mềm diệt virus.

### 2. Lỗi không tìm thấy file khóa `config.lock` khi chạy Git
Nếu bạn gặp thông báo lỗi kiểu như:
`error: could not lock config file D:/ML/Lab1/.git/config: File exists`
Hãy đóng hoàn toàn VS Code và chạy lệnh sau trong PowerShell thường để xóa tệp khóa bị kẹt:
```powershell
Remove-Item -Force D:\ML\Lab1\.git\config.lock
```

### 3. Lỗi Dubious Ownership (Quyền sở hữu không an toàn) của Git
Nếu VS Code không thể `push` hoặc `pull` code và báo lỗi ownership, hãy mở PowerShell thông thường (hoặc terminal trong VS Code) và chạy lệnh:
```powershell
git config --global --add safe.directory D:/ML/Lab1
```

### 4. Font chữ hiển thị toán học hoặc ký tự tiếng Việt bị lỗi ô vuông
Dự án sử dụng font chữ mặc định hệ thống là **`Segoe UI`** để đảm bảo hiển thị đúng dấu tiếng Việt và các ký hiệu toán học như tỷ lệ thuận ($\propto$), suy ra ($\to$). Nếu gặp lỗi ô vuông, hãy đảm bảo hệ điều hành Windows của bạn đã cài đặt font `Segoe UI` (font mặc định đi kèm Windows).
