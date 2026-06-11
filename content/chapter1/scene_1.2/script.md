# KỊCH BẢN CHI TIẾT - PHÂN CẢNH 1.2: BA LÀN SÓNG MỞ RỘNG (SCALING PARADIGM)
*Thời lượng dự kiến: ~4 phút (03:00 - 07:00 trong video)*

---

### Phân cảnh 1.2.1: Hệ trục tọa độ 3D ảo & Làn sóng Pre-training (03:00 - 04:15)
*   **Hình ảnh (Manim):**
    *   Hệ trục tọa độ 3D ảo hiện lên mượt mà từ tâm điểm gốc (Origin).
    *   **Trục X (Màu tím):** Phát sáng rực rỡ với nhãn *"X: Huấn luyện sơ khởi (Pre-training Compute)"*.
    *   Công thức định luật tỉ lệ thuận Chinchilla hiện lên góc trên bên trái:
        $$L(N, D) = E + \frac{A}{N^\alpha} + \frac{B}{D^\beta}$$
    *   Hiển thị điểm **Base LLM (GPT-3)** nằm xa trên trục X.
*   **Lời thoại (Voiceover):**
    > "Để hiểu rõ bước chuyển mình quan trọng này, chúng ta cần nhìn nhận sự phát triển của các mô hình ngôn ngữ lớn qua một không gian ba chiều của việc mở rộng quy mô (scaling).
    > 
    > Làn sóng mở rộng đầu tiên, nằm trên trục hoành X, tập trung vào việc mở rộng lượng tính toán dùng để huấn luyện sơ khởi một mô hình – còn gọi là Pre-training Scaling. 
    > 
    > Định luật tỉ lệ thuận Chinchilla chỉ ra rằng hiệu năng của mô hình (được đo bằng sai số Test Loss $L$) sẽ giảm một cách có dự đoán theo luật lũy thừa khi ta tăng kích thước tham số mô hình $N$ và số lượng dữ liệu huấn luyện $D$. Quy luật này đã dẫn lối cho sự ra đời của các mô hình nền tảng mạnh mẽ như GPT-3."

---

### Phân cảnh 1.2.2: Làn sóng Post-training (04:15 - 05:30)
*   **Hình ảnh (Manim):**
    *   **Trục Y (Màu xanh lá):** Hướng thẳng đứng đi lên sáng bừng với nhãn *"Y: Tinh chỉnh sau huấn luyện (Post-training)"*.
    *   Công thức chuyển đổi hành vi hiện lên bên cạnh:
        $$\text{SFT} \to \text{RLHF / DPO}$$
    *   Mô hình dịch chuyển từ điểm **GPT-3** hướng lên trên theo trục Y để tạo thành điểm **Chat LLM (GPT-4 / LLaMA-Chat)**, kết nối bằng nét đứt màu xám.
*   **Lời thoại (Voiceover):**
    > "Tuy nhiên, chỉ huấn luyện sơ khởi thôi là chưa đủ. Một mô hình nền tảng thô chưa thể trò chuyện hay hỗ trợ con người một cách tối ưu. 
    > 
    > Đó là lúc làn sóng thứ hai xuất hiện dọc theo trục tung Y: tinh chỉnh sau huấn luyện – hay Post-training Scaling. 
    > 
    > Bằng cách sử dụng tinh chỉnh có giám sát (SFT) trên các cặp câu hỏi - câu trả lời chất lượng cao, kết hợp với học tăng cường từ phản hồi của con người (RLHF hoặc DPO), chúng ta căn chỉnh hành vi của mô hình để biến chúng thành những trợ lý AI cực kỳ hữu ích và an toàn như GPT-4 hay Claude."

---

### Phân cảnh 1.2.3: Làn sóng Test-time Compute (05:30 - 07:00)
*   **Hình ảnh (Manim):**
    *   **Trục Z (Màu xanh neon):** Hướng xéo xuống góc 45 độ (mô phỏng chiều sâu không gian) rực sáng với nhãn *"Z: Tính toán khi suy luận (Test-time Compute)"*.
    *   Công thức tính xác suất thành công của Best-of-N xuất hiện góc dưới bên phải:
        $$P(\text{correct}) = 1 - (1 - p)^N$$
    *   Mô hình dịch chuyển xéo theo hướng trục Z để tạo ra điểm **Reasoning LLM (o1 / DeepSeek-R1)**, nối từ GPT-4 bằng nét đứt màu xám. Điểm này phát sáng vàng rực.
*   **Lời thoại (Voiceover):**
    > "Nhưng đến một giới hạn nào đó, việc huấn luyện các mô hình lớn hơn hay tinh chỉnh thêm dữ liệu bắt đầu gặp phải những rào cản vật lý cực kỳ tốn kém. Đồng thời, các trợ lý AI thông thường vẫn gặp khó khăn lớn trước những bài toán logic phức tạp.
    > 
    > Đây chính là lúc chúng ta bước vào làn sóng thứ ba – trục Z của hệ tọa độ: Mở rộng tính toán tại thời điểm suy luận (Test-time Scaling). 
    > 
    > Thay vì bắt mô hình trả lời ngay lập tức, chúng ta cấp thêm tài nguyên tính toán để nó tự suy nghĩ, lập luận, tạo ra nhiều phương án và chọn lọc lời giải tốt nhất. Việc lấy mẫu thử $N$ lần giúp xác suất tìm được câu trả lời chính xác tiệm cận đến 1. Đây cũng chính là bí quyết giúp những mô hình như OpenAI o1 hay DeepSeek-R1 tạo nên cú hích lớn trong năng lực suy luận của AI hiện nay."
