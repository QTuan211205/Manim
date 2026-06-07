# KỊCH BẢN CHI TIẾT & PHÂN CẢNH VIDEO (DỊCH SONG SONG WORD-FOR-WORD TOÀN BỘ VIDEO 120 PHÚT)
## VƯỢT QUA GIỚI HẠN GIẢI MÃ: THUẬT TOÁN META-GENERATION CHO LLM
*Bản dịch đầy đủ, giải thích chi tiết toàn bộ các khái niệm cốt lõi dựa trên NeurIPS 2024 Tutorial*

---

## 🎬 CHƯƠNG 1: KỶ NGUYÊN MỞ RỘNG TÍNH TOÁN (SCALING LAWS)
*Thời lượng: ~15 phút (00:00 - 15:00 trong subtitle gốc | Người trình bày: Sean Welleck)*

### Phân cảnh 1.1: Giới thiệu chung & Vai trò của Test-Time Compute (00:00 - 02:00)
*   **Trực quan hình ảnh (3B1B Style):**
    *   Màn hình tối màu xám đen (`#111111`).
    *   Tiêu đề lớn xuất hiện bằng hiệu ứng `Write` chậm rãi: **"VƯỢT QUA GIỚI HẠN GIẢI MÃ: THUẬT TOÁN META-GENERATION CHO LLM"** (Màu xanh dương nhạt).
    *   Phụ đề tiếng Anh xuất hiện mờ dần ở dưới: *"Beyond Decoding: Meta-Generation Algorithms for LLMs"*.
    *   Màn hình chuyển sang mô phỏng một mạng Neural đơn giản với các lớp nút (nodes) liên kết nhấp nháy truyền tín hiệu. Khi các token đầu vào (input tokens) đi vào, các đường liên kết mờ nhấp nháy ánh sáng vàng truyền qua lớp ẩn, và ở lớp đầu ra, từng từ được sinh ra tuần tự từng bước: `"Taylor"` -> `"Swift"` -> `"is"` -> `"a"` -> `"singer"` -> `"songwriter"`.
*   **Lời thoại Voiceover (Dịch chi tiết):**
    > "Xin chào các bạn, chào mừng các bạn đã quay trở lại với kênh. Trong video ngày hôm nay, chúng ta sẽ cùng nhau tìm hiểu và giải thích một chủ đề cực kỳ nóng hổi và quan trọng trong thế giới AI hiện đại: đó là các thuật toán suy luận (inference algorithms), khái niệm hệ điều hành LLM (LLM OS), và đặc biệt là các thuật toán Meta-Generation dành cho các mô hình ngôn ngữ lớn. Về cốt lõi, nội dung ngày hôm nay sẽ xoay quanh các thuật toán giúp tạo ra và tối ưu hóa kết quả đầu ra bằng cách sử dụng một mô hình ngôn ngữ.
    > 
    > Vậy thì tại sao bạn nên quan tâm đến chủ đề này? Hiện nay, rất nhiều nhà nghiên cứu và kỹ sư AI đang tập trung phát triển và tối ưu hóa khái niệm gọi là 'năng lực tính toán tại thời điểm chạy' (test-time compute) – tức là việc phân bổ thêm tài nguyên tính toán sau khi mô hình đã được huấn luyện xong – nhằm cải thiện hiệu suất của toàn bộ hệ thống sinh văn bản. Và đây cũng chính là trọng tâm mà chúng ta sẽ cùng phân tích kỹ lượng.
    > 
    > Bản thân các mô hình ngôn ngữ đang phát triển với tốc độ kinh ngạc. Mỗi ngày trôi qua, chúng lại sở hữu thêm những khả năng mới, từ giải các bài toán Olympic toán học phức tạp cho đến việc viết code thực tế ngay trong cơ sở mã của bạn. Về cơ bản, bất kỳ tác vụ nào có thể biểu diễn dưới dạng một chuỗi ký tự tuần tự, các mô hình ngôn ngữ đều có thể hỗ trợ đắc lực."

### Phân cảnh 1.2: Ba làn sóng mở rộng (Scaling Waves) (02:00 - 06:00)
*   **Trực quan hình ảnh (3B1B Style):**
    *   Một hệ trục tọa độ 3D ảo hiện lên mượt mà trên lưới tọa độ mờ.
    *   **Trục X (Pre-training Compute - Màu tím):** Tăng kích thước tham số mô hình $N$ và tập dữ liệu $D$. Hiện đồ thị hàm Loss giảm dần theo quy luật Chinchilla/Kaplan: $Loss \propto N^{-\alpha}$. Hiển thị các chấm điểm đại diện cho GPT-2, GPT-3.
    *   **Trục Y (Post-training Compute - Màu xanh lá):** Tinh chỉnh, các nhãn "SFT", "RLHF" sáng lên, mô tả việc tinh chỉnh mô hình qua các cặp dữ liệu câu hỏi - câu trả lời. GPT-4 dịch chuyển từ GPT-3 lên trên theo chiều dọc.
    *   **Trục Z (Test-time Compute - Màu xanh neon):** Trục hướng dọc sâu rực sáng. Vẽ đồ thị hiệu năng tăng dần theo số lượng token suy luận (giống đồ thị hiệu năng dòng o1/R1).
*   **Lời thoại Voiceover (Dịch chi tiết):**
    > "Khi chúng ta suy nghĩ về sự tiến bộ của các mô hình ngôn ngữ, chúng ta có thể nhìn nhận nó từ góc độ mở rộng quy mô (scale). Đây chính là phần nền tảng để hiểu tại sao ngành AI phải dịch chuyển từ việc phóng to mô hình sang việc tối ưu hóa thuật toán khi suy luận.
    > 
    > Làn sóng mở rộng đầu tiên tập trung vào việc mở rộng lượng tính toán được sử dụng để huấn luyện sơ khởi một mô hình (pre-train). Đây là luật mở rộng giai đoạn huấn luyện sơ khởi (Pre-training Compute Scaling Law). Quy luật lũy thừa (Power Law) chỉ ra rằng hiệu năng của mô hình (được đo bằng Test Loss) sẽ cải thiện tỷ lệ thuận với lượng compute huấn luyện, kích thước tham số (N) và số lượng token huấn luyện (D). Càng nhiều tài nguyên huấn luyện sơ khởi, mô hình càng thông minh.
    > 
    > Tuy nhiên, việc huấn luyện sơ khởi này vẫn chưa đủ để giúp các mô hình ngôn ngữ thực hiện được tất cả các tác vụ phức tạp mà chúng ta mong muốn. Vì vậy, đã có một làn sóng mở rộng thứ hai tập trung vào giai đoạn sau huấn luyện (Post-training Scaling). Bằng cách tinh chỉnh mô hình thông qua tinh chỉnh có giám sát (SFT - Supervised Fine-Tuning) trên các cặp dữ liệu chất lượng cao và học tăng cường từ phản hồi của con người (RLHF - Reinforcement Learning from Human Feedback), chúng ta tạo ra những trợ lý AI cực kỳ hữu ích và biết vâng lời.
    > 
    > Nhưng làn sóng này vẫn chưa chứng minh được sự đầy đủ cho tất cả các tác vụ nặng đòi hỏi suy luận logic sâu sắc. Do đó, hiện tại, lĩnh vực này đang trải qua một sự dịch chuyển thứ ba, tập trung vào việc mở rộng tính toán tại thời điểm suy luận (Test-time Scaling hay Inference-time Compute Scaling). Ý tưởng cốt lõi ở đây là: thay vì bắt mô hình đưa ra câu trả lời ngay lập tức, chúng ta phân bổ thêm tài nguyên tính toán cho mô hình "suy nghĩ" ngay tại thời điểm chạy để nâng cao độ chính xác của kết quả đầu ra."

### Phân cảnh 1.3: Cách thức mở rộng Test-Time Compute & Compound AI System (06:00 - 08:30)
*   **Trực quan hình ảnh (3B1B Style):**
    *   Màn hình chia làm 3 phần trực quan hóa 3 phương án:
    *   1. **Sinh thêm token (Chain of Thought):** Show câu hỏi toán. Phía dưới, hiển thị một chuỗi các ô màu xanh lá cây chứa các bước lập luận ("Suy nghĩ 1" $\to$ "Suy nghĩ 2" $\to$ "Suy nghĩ 3") trước khi trỏ đến ô kết quả cuối cùng.
    *   2. **Gọi mô hình nhiều lần (Parallel sampling):** Hoạt họa sinh song song hàng ngàn luồng ứng viên lập trình (AlphaCode), đi qua bộ lọc (Filter) kiểm tra tính đúng đắn và chọn ra code chạy được.
    *   3. **Kết hợp công cụ ngoài (Compound AI):** Vẽ mô hình LLM tương tác với một "Hộp công cụ" (như Trình thông dịch Python, Máy tính) bằng các mũi tên nhấp nháy.
*   **Lời thoại Voiceover (Dịch chi tiết):**
    > "Làm thế nào để chúng ta thực sự bắt LLM dành thêm compute tại thời điểm suy luận? Có ba cách phổ biến:
    > 
    > Thứ nhất, cho mô hình sinh thêm các token lập luận trung gian. Đây chính là phương pháp Chain of Thought nổi tiếng. Thay vì trả lời ngay đáp án bằng 1 token, mô hình sinh hàng trăm token suy nghĩ trong đầu, tự mở đường đi đến lời giải đúng.
    > 
    > Thứ hai, gọi mô hình nhiều lần để tạo ra nhiều phương án trả lời khác nhau, sau đó lọc và chọn lấy kết quả tốt nhất. Ví dụ như hệ thống AlphaCode đã sinh hàng triệu chương trình thử nghiệm trước khi chọn ra đáp án cuối cùng.
    > 
    > Thứ ba, kết hợp mô hình với các công cụ bên ngoài như máy tính hay trình biên dịch để chuyển giao phần tính toán nặng nhọc sang các công cụ có độ tin cậy tuyệt đối."

### Phân cảnh 1.4: Khung lý thuyết Generator và Meta-Generator (08:30 - 10:00)
*   **Trực quan hình ảnh (3B1B Style):**
    *   Vẽ hộp màu xanh dương dán nhãn **Generator ($g$)** nhận đầu vào $x$ và xuất ra $y$ theo công thức $y \sim g(y \mid x; p_\theta, \phi)$ ở trên hộp.
    *   Vẽ hộp lớn màu xám bao quanh hộp xanh dương, dán nhãn **Meta-Generator ($G$)**. Bên trong hộp lớn vẽ các mũi tên lặp, một hộp con màu vàng là **Evaluator** (Bộ đánh giá). Show luồng dữ liệu đi qua luồng đánh giá lặp lại nhiều lần.
*   **Lời thoại Voiceover (Dịch chi tiết):**
    > "Video này sẽ cung cấp cho các bạn một khung khái niệm rõ ràng để kết hợp ba yếu tố trên thành một hệ thống tạo văn bản hoàn chỉnh.
    > 
    > Trước hết, một Generator (Bộ sinh cơ bản) đề cập đến bất kỳ thuật toán nào nhận vào một chuỗi tiền tố và mô hình ngôn ngữ để trả về một chuỗi đầu ra. Nếu bạn từng sử dụng các API LLM thông thường, đó chính là một Generator. Trong phần đầu tiên, chúng ta sẽ đi qua các thuật toán truyền thống để sinh một chuỗi đơn lẻ với mô hình ngôn ngữ.
    > 
    > Sau đó, chúng ta coi các thuật toán cơ bản đó như một chiếc hộp đen (black box). Từ đó, chúng ta thiết kế các chiến lược cấp cao hơn để điều phối các Generator này, kết hợp thông tin từ mô hình đánh giá hoặc công cụ ngoài. Đó chính là Meta-Generator (Bộ điều phối cấp cao). Một ví dụ đơn giản là bạn gọi API nhiều lần, sau đó chọn ra kết quả tốt nhất bằng một bộ đánh giá riêng biệt. Nếu thiết kế Meta-generator đúng cách, chúng ta có thể nâng cao hiệu suất tác vụ bằng cách tăng lượng mẫu sinh ra.
    > 
    > Nội dung này sẽ được chia làm bốn phần chính: Phần 1 là Kỷ nguyên mở rộng tính toán; Phần 2 là Bộ sinh cơ bản (Primitive Generators); Phần 3 là Bộ điều phối cấp cao (Meta-Generation Strategies); và Phần 4 là Hiệu năng hệ thống (Systems Efficiency). Cuối cùng, chúng ta sẽ đúc rút từ phiên thảo luận nhóm (panel session) chất lượng của các chuyên gia hàng đầu.
    > 
    > Bây giờ, hãy cùng bắt đầu ngay với Phần II về Bộ sinh cơ bản."

### Phân cảnh 2.1: Cơ chế tự hồi quy & Tự sinh Token (Autoregressive Generation) (10:00 - 16:20)
*   **Bảng Kịch bản Chi tiết (Detailed Storyboard Table):**

| Thời gian | Trực quan hình ảnh (3Blue1Brown Style) | Lời thoại Voiceover (Thuyết minh chi tiết) |
| :--- | :--- | :--- |
| **10:00 - 10:30** | **Mở đầu Chương 2 & Lưới Từ vựng (Vocabulary Grid):**<br>- Màn hình tối đen `#111111`. Tiêu đề **"CHƯƠNG II: BỘ SINH CƠ BẢN"** viết ra mượt mà và thu nhỏ lên góc trên.<br>- Xuất hiện một lưới tọa độ lớn chứa $10 \times 10$ ô vuông nhỏ màu xám nhạt ở trung tâm màn hình, đại diện cho **Không gian từ vựng (Vocabulary Space)**.<br>- Hiệu ứng camera phóng to vào 3 ô vuông bất kỳ. Khi phóng to, số Token ID hiện lên cùng ký tự chữ tương ứng:<br>  - Ô `23910` hiển thị chữ `"Tay"`<br>  - Ô `1048` hiển thị chữ `"lor"` | Chào mừng các bạn đến với Chương hai: Bộ sinh cơ bản – *Primitive Generators*.<br><br>Trước khi đi sâu vào thuật toán, chúng ta cần hiểu cách mô hình nhìn nhận ngôn ngữ. Toàn bộ ngôn ngữ đối với mô hình được biểu diễn bằng một không gian từ vựng khổng lồ, thường chứa khoảng năm mươi nghìn từ và mảnh ghép ký tự độc lập, gọi là các token.<br><br>Mỗi token được gán một chỉ số ID số học duy nhất. Ví dụ, tên riêng "Taylor" có thể được tách thành hai token ghép là *"Tay"* và *"lor"*, mỗi phần tương ứng với một ô trong bản đồ từ vựng của mô hình. |
| **10:30 - 11:20** | **So sánh các phương pháp Token hóa (Tokenization):**<br>- Hiển thị chuỗi văn bản gốc ở trên cùng: `"Taylor Swift is"`<br>- Xuất hiện 3 dòng hộp so sánh trực quan các cách phân tách cấu trúc ngữ pháp:<br>  - Dòng 1: **Cấp độ từ (Word-level):** `["Taylor"]`, `["Swift"]`, `["is"]` (3 hộp màu xanh biển). Giải thích nhược điểm: Từ vựng quá lớn hoặc gặp lỗi OOV.<br>  - Dòng 2: **Cấp độ ký tự (Character-level):** `["T"]`, `["a"]`, `["y"]`, `["l"]`... (15 hộp nhỏ màu xám).<br>  - Dòng 3: **Cấp độ BPE (Byte-Pair Encoding):** `["Taylor"]`, `[" Swift"]`, `[" is"]` (3 hộp phát sáng xanh lá). | Để biến văn bản thành các token này, hệ thống sử dụng các bộ Tokenizer khác nhau.<br><br>Hãy so sánh ba phương pháp tách từ. Cách thứ nhất là tách cấp độ Từ. Mặc dù dễ hiểu, cách này khiến bộ từ vựng phình to vô hạn và bất lực trước các từ mới chưa từng học.<br><br>Cách thứ hai là tách cấp độ Ký tự. Cách này giảm thiểu từ vựng, nhưng lại kéo dài chuỗi dữ liệu một cách kinh khủng và làm mất đi các liên kết ngữ nghĩa nguyên khối.<br><br>Do đó, các LLM hiện đại sử dụng giải pháp lai Byte-Pair Encoding – viết tắt là BPE. BPE gộp các ký tự phổ biến xuất hiện cùng nhau thành một token riêng, ví dụ như *"Taylor"*, *" Swift"*, *" is"*, tạo ra sự cân bằng hoàn hảo giữa hiệu năng lưu trữ và tính ngữ nghĩa. |
| **11:20 - 12:00** | **Dòng thông tin Self-Attention:**<br>- Vẽ các hộp token BPE nằm ngang: `["Taylor"]`, `[" Swift"]`, `[" is"]`. Các hộp màu xanh biển nhạt.<br>- Phía trên các hộp, xuất hiện các đường cong màu vàng nhạt nối từ `["Taylor"]`, `[" Swift"]` dồn tụ về hộp cuối cùng là `[" is"]`, có đầu mũi tên vàng chỉ hướng mượt mà.<br>- Hàng loạt hạt sáng nhỏ (glowing particles) chuyển động mượt mà chạy dọc theo các đường cong này đổ về từ `[" is"]`. Khi các hạt tụ về từ cuối cùng, hộp phát sáng rực rỡ.<br>- Phía trên xuất hiện công thức xác suất cốt lõi:<br>$$p_\theta(x_t \mid x_{<t})$$<br>- Highlight các ký hiệu tương ứng với các luồng thông tin vừa di chuyển. | Khi văn bản đầu vào được nạp vào, mạng neural không chỉ xử lý các từ một cách cô lập. Thông qua cơ chế tự chú ý – *Self-Attention*, mô hình sẽ thiết lập các đường kết nối ngữ nghĩa giữa tất cả các từ trong quá khứ.<br><br>Hãy hình dung các luồng thông tin ngữ cảnh giống như các hạt năng lượng chuyển động dọc theo các kết nối attention này, tập hợp toàn bộ ý nghĩa từ các từ đi trước để đưa về từ hiện tại.<br><br>Quá trình tính toán phức tạp này được gói gọn trong công thức toán học cốt lõi: $p$ chỉ số $\theta$ của $x_t$ với điều kiện là $x$ nhỏ hơn $t$. Đây là phân phối xác suất có điều kiện dự báo cho token tiếp theo $x_t$ dựa trên toàn bộ lịch sử tiền tố $x$ nhỏ hơn $t$. |
| **12:00 - 12:50** | **Mặt nạ nhân quả (Causal Attention Mask):**<br>- Xuất hiện một ma trận vuông kích thước $4 \times 4$ ở trung tâm màn hình, đại diện cho ma trận Attention giữa 4 từ đầu vào: `["Taylor"]`, `[" Swift"]`, `[" is"]`, `[" an"]`. Hàng và cột đều được dán nhãn bằng 4 từ này.<br>- Trên ma trận, nửa tam giác trên (Upper Triangular) chứa các ô (1,2), (1,3)... chuyển thành màu đỏ sẫm và hiện ký hiệu âm vô cùng $-\infty$ (Mặt nạ Mask).<br>- Nửa tam giác dưới (Lower Triangular) bao gồm đường chéo chính lần lượt hiện các ô màu xanh lá kèm dấu checkmark biểu thị các kết nối hợp lệ. | Tuy nhiên, có một chi tiết kỹ thuật vô cùng quan trọng: Tại sao mô hình này lại được gọi là mô hình ngôn ngữ *nhân quả* hay mô hình ngôn ngữ *một chiều*?<br><br>Đó là bởi vì khi tính toán Attention, mô hình tuyệt đối không được phép "nhìn trộm" các từ ở tương lai. Để thực hiện ràng buộc này, một **mặt nạ nhân quả** – *Causal Attention Mask* – được áp dụng.<br><br>Hãy hình dung ma trận Attention biểu diễn mối quan hệ giữa bốn token đầu tiên. Nửa tam giác phía trên của ma trận tương ứng với việc các từ trong quá khứ nhìn về tương lai. Các giá trị này sẽ bị gán bằng điểm số âm vô cùng, khiến chúng bị triệt tiêu hoàn toàn.<br><br>Chỉ có nửa tam giác phía dưới, bao gồm các từ hiện tại nhìn về quá khứ và chính nó, là được giữ lại. Đây là cấu trúc ma trận tam giác dưới – nền tảng đảm bảo tính nhân quả trong LLM. |
| **12:50 - 13:40** | **Biến đổi Softmax (Logits -> Probabilities):**<br>- Vẽ 4 cột đứng đại diện cho giá trị Logits thô đầu ra của mô hình: `"an"` (Logit $2.5$), `"a"` (Logit $0.5$), `"the"` (Logit $1.6$), `"best"` (Logit $-0.8$).<br>- Phía trên xuất hiện công thức Softmax:<br>$$\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}}$$<br>- **Bước 1: Áp dụng số mũ $e^{z_i}$**: Các cột co giãn kích thước theo giá trị lũy thừa: $e^{2.5} \approx 12.18$, $e^{0.5} \approx 1.65$...<br>- **Bước 2: Tính tổng và Chia**: Chuẩn hóa, các cột co lại tạo thành phân phối xác suất: $0.63$, $0.09$, $0.26$, $0.02$. | Nhưng làm sao mạng neural chuyển đổi các điểm số thô thành các xác suất thực tế này? Đầu ra thô của LLM là các giá trị logit, có thể nhận bất kỳ giá trị thực âm hay dương nào.<br><br>Để biến chúng thành một phân phối xác suất hợp lệ, mô hình sử dụng hàm **Softmax**.<br><br>Đầu tiên, hàm Softmax lấy lũy thừa cơ số tự nhiên $e$ mũ logit. Phép toán này biến mọi giá trị âm thành dương, và phóng đại các điểm số cao.<br><br>Sau đó, chúng ta tính tổng tất cả các lũy thừa này làm mẫu số, rồi chia từng giá trị lũy thừa riêng lẻ cho tổng chung. Kết quả là chúng ta thu được một phân phối xác suất chuẩn hóa tuyệt đẹp, nơi mọi phần tử đều dương và tổng xác suất của toàn bộ từ vựng đạt đúng một trăm phần trăm. |
| **13:40 - 15:00** | **Vòng lặp tự hồi quy 4 bước (Autoregressive Loop):**<br>- Trái màn hình: Hộp chứa câu tiền tố ban đầu. Phải màn hình: Khung phân phối xác suất chứa 4 cột từ vựng.<br>- **Bước 1 (t=1):** Context `"Taylor Alison Swift is"`. Bảng bên phải hiện các cột xác suất. Chữ `"an"` cao nhất ($0.13$). Chữ `"an"` nhấp nháy và bay từ bên phải sang chèn vào cuối câu bên trái.<br>- **Bước 2 (t=2):** Context tự động cập nhật thêm chữ `"an"`. Bảng xác suất bên phải thay đổi. Cột chữ `"American"` cao nhất ($0.82$) bay sang nối vào câu bên trái.<br>- **Bước 3 (t=3):** Context thêm `"American"`, sinh ra `"singer"` ($0.65$) bay sang trái.<br>- **Bước 4 (t=4):** Context thêm `"singer"`, sinh tiếp dấu phẩy `","` ($0.75$) bay sang. | Quá trình sinh văn bản thực tế là một vòng lặp liên hồi. Hãy cùng xem mô hình tự giải mã bốn bước liên tiếp.<br><br>Tại bước một, tiền tố là *"Taylor Alison Swift is"*. Mô hình tính toán phân phối và từ *"an"* đạt điểm cao nhất. Token *"an"* được chọn và chèn vào câu đầu vào.<br><br>Ngay lập tức, bước hai bắt đầu. Với tiền tố mới kết thúc bằng *"an"*, mô hình tính toán lại phân phối xác suất từ vựng, chọn ra từ *"American"* có xác suất tám mươi hai phần trăm và nối vào câu.<br><br>Bước ba, tiền tố dài hơn, mô hình dự đoán ra từ *"singer"* và cập nhật vào câu. Bước bốn, mô hình sinh tiếp dấu phẩy để chuẩn bị nối tiếp danh từ ghép. Mỗi token sinh ra đều trở thành một phần của quá khứ để định hình nên tương lai của chuỗi văn bản. |
| **15:00 - 15:40** | **Bùng nổ tổ hợp cấp số nhân (Fractal Search Tree):**<br>- Xóa màn hình bên dưới. Vẽ nút gốc `"Taylor Swift is"`. Nhánh ra 4 hướng con. Mỗi nhánh con đẻ tiếp 3 nhánh cháu. Vẽ các đường nối màu xám mảnh.<br>- Hiệu ứng camera bắt đầu zoom out (thu nhỏ) liên tục ra xa. Cây quyết định tự động nhân bản rẽ nhánh liên tục ở các cấp dưới (Fractal tree generation).<br>- Ở góc dưới màn hình, hiển thị công thức tổ hợp tổ kén:<br>$$V \to V^2 \to V^3 \to \dots \to V^t$$<br>- Thế số thực tế bên dưới: $50,000^1 \to 50,000^2 \to 50,000^3 \approx 1.25 \times 10^{14}$ đường đi tiềm năng. | Vì mỗi bước sinh chúng ta đều có quyền lựa chọn các từ khác nhau, quá trình giải mã thực chất là việc đi tìm một đường đi tối ưu trên một cây quyết định tìm kiếm khổng lồ.<br><br>Nhưng không gian tìm kiếm này lớn đến mức nào? Ở bước đầu tiên, ta có $V$ lựa chọn. Bước hai, ta có $V$ mũ hai. Bước ba là $V$ mũ ba. Với kích thước từ vựng năm mươi nghìn từ, chỉ sau ba bước giải mã đơn giản, tổng số chuỗi tiềm năng đã bùng nổ lên tới một trăm hai mươi lăm nghìn tỷ đường đi khác nhau!<br><br>Sự bùng nổ tổ hợp cấp số nhân này khiến việc duyệt qua toàn bộ cây để tìm ra chuỗi hoàn hảo nhất là điều hoàn toàn bất khả thi về mặt tính toán. |
| **15:40 - 16:20** | **Đề cương phân loại giải mã:**<br>- Zoom cây quyết định biến mất.<br>- Xuất hiện 3 hộp lớn: Tối ưu hóa (Xanh dương), Lấy mẫu (Xanh lá), Ràng buộc (Cam).<br>- Từng hộp lần lượt sáng lên kèm nội dung công thức tương ứng. Chữ `"y thuộc C"` hiển thị mượt mà không lỗi font. | Do đó, các thuật toán giải mã ra đời để điều hướng thông minh trên không gian tìm kiếm vô hạn này. Chúng được chia làm ba trường phái lớn.<br><br>Một là Tối ưu hóa – tập trung tìm kiếm các đường đi có xác suất tích lũy lớn nhất. Hai là Lấy mẫu – đưa vào sự ngẫu nhiên có kiểm soát để tạo ra sự tự nhiên như con người. Và ba là Ràng buộc cấu trúc – ép buộc mô hình tuân thủ quy tắc lập trình.<br><br>Tiếp theo, chúng ta sẽ phân tích sâu nhóm giải thuật Tối ưu hóa, bắt đầu từ Giải mã tham lam và Tìm kiếm chùm. |
### Phân cảnh 2.2: Tối ưu hóa trong Giải mã — Tham lam vs. Tìm kiếm chùm (Greedy vs. Beam Search) (20:00 - 24:00)

| Thời gian | Trực quan hình ảnh (3Blue1Brown Style) | Lời thoại Voiceover (Thuyết minh chi tiết) |
| :--- | :--- | :--- |
| **20:00 - 20:30** | **Mục tiêu MAP (Maximum A Posteriori):**<br>- Màn hình tối `#111111`. Xuất hiện tiêu đề: **"Tối ưu hóa trong Giải mã (Decoding as Optimization)"** ở trên cùng.<br>- Ở trung tâm, viết ra công thức tối ưu hóa MAP:<br>$$\arg\max_{x} p_\theta(x)$$<br>  - Dùng `Brace` bên dưới $x$ ghi chú: *"Chuỗi token đầu ra hoàn chỉnh"*. Chú thích bên dưới $p_\theta(x)$ ghi: *"Xác suất của chuỗi"*.<br>- Dọn dẹp màn hình chuẩn bị chuyển sang Giải mã Tham lam. | Khi chúng ta tiếp cận việc sinh văn bản như một bài toán tối ưu hóa, mục tiêu cao nhất là đi tìm một chuỗi từ có xác suất lớn nhất. Trong toán học, mục tiêu này được gọi là giải mã cực đại hóa xác suất hậu nghiệm – Maximum A Posteriori, viết tắt là MAP.<br><br>Hãy cùng xem làm thế nào chúng ta có thể tìm ra chuỗi từ tối ưu này trên thực tế. |
| **20:30 - 21:50** | **Giải mã Tham lam (Greedy Decoding) & Tính Cận thị:**<br>- Xuất hiện công thức của giải mã Tham lam ở góc trái:<br>$$x_t = \arg\max_{w \in V} p_\theta(w \mid x_{<t})$$<br>- Trực quan hóa cây quyết định từ tiền tố `"Taylor Swift is"` (nhánh trái: Greedy, nhánh phải: Non-greedy):<br>- Vẽ nhánh **Greedy Path** bên trái:<br>  - Bước 1 chọn `"a"` với xác suất $0.13$.<br>  - Bước 2 chọn `"former"` với xác suất $0.03$.<br>  - Bước 3 chọn `"contestant"` với xác suất $0.003$.<br>  - Bước 4 chọn `"on"` với xác suất $0.02$.<br>  - Tính xác suất tích lũy: $0.13 \times 0.03 \times 0.003 \times 0.02 \approx 1.97 \times 10^{-7}$.<br>- Vẽ nhánh **Non-greedy Path** bên phải:<br>  - Bước 1 chọn `"a"` với xác suất $0.13$.<br>  - Bước 2 chọn `"singer"` với xác suất $0.012$ (thấp hơn `"former"` ở thời điểm đó).<br>  - Bước 3 chọn `","` với xác suất $0.26$.<br>  - Bước 4 chọn `"song"` với xác suất $0.21$.<br>  - Tính xác suất tích lũy: $0.13 \times 0.012 \times 0.26 \times 0.21 \approx 8.52 \times 10^{-5}$.<br>- So sánh 2 kết quả: Nhánh bên phải lớn gấp **430 lần** nhánh Tham lam bên trái!<br>- Hộp nhánh tham lam chuyển màu đỏ kèm nhãn `"Cận thị (Shortsighted)"`. Nhánh bên phải phát sáng màu xanh lá `"Tối ưu hơn"`. | Phương pháp đơn giản nhất để giải bài toán này là Giải mã tham lam. Ở mỗi bước đi, thuật toán chỉ quan tâm đến lựa chọn tốt nhất ngay trước mắt: chọn token có xác suất cao nhất tại thời điểm đó.<br><br>Nhưng giải mã tham lam rất "cận thị". Việc luôn chọn từ tốt nhất ở hiện tại có thể dẫn chúng ta vào một ngõ cụt đầy những từ vô nghĩa và xác suất cực thấp ở phía sau.<br><br>Hãy so sánh hai chuỗi văn bản thực tế được sinh ra sau tiền tố "Taylor Swift is". Thuật toán tham lam chọn từ *"former"* ở bước hai vì nó có xác suất cao nhất tại thời điểm đó ($0.03$ so với $0.012$ của *"singer"*). Tuy nhiên, đường đi này dẫn tới một kết cục có xác suất tích lũy cực kỳ thấp.<br><br>Trong khi đó, nếu chấp nhận chọn từ *"singer"* có xác suất thấp hơn ở bước hai, mô hình lại mở ra các bước đi tiếp theo có xác suất cực cao là dấu phẩy và từ *"song"*. Kết quả là chuỗi không tham lam có tổng xác suất lớn gấp hơn bốn trăm lần chuỗi tham lam. |
| **21:50 - 23:20** | **Thuật toán Tìm kiếm Chùm (Beam Search, K=2):**<br>- Vẽ cây quyết định với độ rộng chùm $K=2$.<br>- **Bước 1 (t=1):** Gốc `"Taylor Swift is"`. Rẽ ra nhiều nhánh: `"a" (0.13)`, `"the" (0.06)`, `"an" (0.03)`, `"to" (0.0004)`. Khung chùm màu vàng bao bọc `"a"` và `"the"`. Các từ còn lại mờ đi và biến mất. Sidebar xếp hạng hiện danh sách và gạch cắt tỉa.<br>- **Bước 2 (t=2):**<br>  - Mở rộng `"a"` thành: `"former"` ($0.13 \times 0.023 = 0.0030$) và `"writer"` ($0.13 \times 0.023 = 0.0030$).<br>  - Mở rộng `"the"` thành: `"latest"` ($0.06 \times 0.067 = 0.0040$) và `"only"` ($0.06 \times 0.05 = 0.0030$).<br>  - Hiển thị cả 4 đường đi kèm xác suất tích lũy ở Sidebar.<br>  - Xếp hạng điểm số: Giữ lại hai chùm cao nhất là `"the latest"` (0.0040) và `"the only"` (0.0030). Hai nhánh xuất phát từ `"a"` (gồm cả đường đi của giải mã tham lam) bị cắt tỉa (pruning) hoàn toàn và mờ đi.<br>  - Highlight hai đường đi `"is the latest"` và `"is the only"` phát sáng màu xanh, chứng minh chùm đã tự động chuyển hướng khỏi sai lầm cận thị của giải mã tham lam. | Để giải quyết điểm yếu cận thị này mà không phải duyệt qua toàn bộ cây tìm kiếm khổng lồ, thuật toán Tìm kiếm chùm – *Beam Search* được áp dụng. Đây là một dạng thuật toán tìm kiếm theo chiều rộng nhưng giới hạn số lượng giả thuyết được giữ lại ở mỗi bước bằng tham số chùm K.<br><br>Hãy cùng mô phỏng từng bước hoạt động của Beam Search với độ rộng chùm K bằng hai.<br><br>Tại bước đầu tiên, thay vì chỉ giữ lại một từ tốt nhất là *"a"*, Beam Search giữ lại cả hai ứng viên hàng đầu là *"a"* và *"the"*. Các lựa chọn kém hơn sẽ bị loại bỏ ngay lập tức.<br><br>Ở bước tiếp theo, mô hình mở rộng cả hai hướng đi này, tạo ra bốn chuỗi tiềm năng. Chúng ta tính toán xác suất tích lũy cho cả bốn chuỗi này và xếp hạng chúng. Hai chuỗi có điểm số cao nhất là *"is the latest"* và *"is the only"* được giữ lại làm chùm mới. Các chuỗi bắt đầu bằng *"a"* bị cắt tỉa hoàn toàn.<br><br>Nhờ duy trì đồng thời K giả thuyết, Beam Search đã sửa sai thành công và chuyển hướng sang một tương lai tốt hơn mà thuật toán tham lam đã bỏ lỡ từ sớm. |
| **23:20 - 24:00** | **Đồ thị Đánh đổi K-Width & Tổng kết:**<br>- Vẽ đồ thị 2 trục Y: Trục xanh thể hiện BLEU (tăng nhanh rồi bão hòa), Trục đỏ thể hiện Compute (tăng tuyến tính).<br>- Nhấn mạnh: Beam Search với K = 1 chính là Giải mã Tham lam.<br>- Tóm tắt quy luật: Tăng $K$ tăng độ chính xác nhưng tăng chi phí tính toán tuyến tính. Cây quyết định biến mất chuẩn bị cho các cạm bẫy tiếp theo. | Để chọn ra K phù hợp, chúng ta phải đánh đổi giữa chất lượng và tài nguyên tính toán. Khi K bằng một, nó hoạt động giống hệt thuật toán tham lam. Khi K tăng lên, chất lượng chuỗi sinh ra sẽ tốt hơn, đổi lại mô hình sẽ tốn nhiều tài nguyên tính toán hơn một cách tuyến tính. Tuy nhiên, hiệu năng thường bão hòa ở K lớn.<br><br>Nhưng liệu việc tối đa hóa xác suất MAP này có luôn mang lại kết quả sinh tốt nhất hay không? Chúng ta sẽ cùng khám phá những cạm bẫy bất ngờ của việc tối ưu hóa xác suất trong phân cảnh tiếp theo. |

### Phân cảnh 2.3: Các cạm bẫy của giải mã MAP (24:00 - 28:00)

| Thời gian | Trực quan hình ảnh (3Blue1Brown Style) | Lời thoại Voiceover (Thuyết minh chi tiết) |
| :--- | :--- | :--- |
| **24:00 - 24:35** | **Lợi ích của giải mã MAP:**<br>- Màn hình tối `#111111`. Xuất hiện tiêu đề chính: **"Các cạm bẫy của Giải mã MAP (Pitfalls of MAP Decoding)"** ở trên cùng.<br>- Nhấn mạnh lợi ích của MAP: hoạt động tốt cho các tác vụ khép kín (closed-ended tasks).<br>- Hiện 2 hộp lớn: *"Dịch máy (Machine Translation)"* và *"Trả lời câu hỏi (Question Answering)"* với các nhánh kết nối từ tiêu đề phụ. | Mặc dù tối đa hóa xác suất, hay còn gọi là giải mã MAP, là phương pháp rất phổ biến, nhưng nó đi kèm với nhiều hạn chế nghiêm trọng. Trước khi đi sâu vào các cạm bẫy, ta cần thừa nhận rằng MAP hoạt động rất tốt trong các tác vụ khép kín, nơi có đáp án rõ ràng và giới hạn, ví dụ như dịch máy hoặc trả lời câu hỏi trực tiếp. |
| **24:35 - 25:25** | **Cạm bẫy 1 — Bẫy lặp (Repetition Traps):**<br>- Tiêu đề phụ: **"1. Bẫy lặp (Repetition Traps)"**.<br>- Xuất hiện hộp văn bản mô phỏng đầu ra lỗi của GPT-2 với kích thước chùm $32$:<br>- Chữ hiển thị từ từ, các cụm từ lặp đi lặp lại được highlight màu đỏ nhấp nháy: `singer-songwriter`, `songwriter-songwriter`...<br>- Xuất hiện hai hộp biện pháp khắc phục dưới dạng sơ đồ: *"Hình phạt lặp (Repetition Penalty)"* và *"Huấn luyện phi xác suất (Unlikelihood Training)"*. | Cạm bẫy đầu tiên và dễ nhận thấy nhất là Bẫy lặp. Các mô hình ngôn ngữ, đặc biệt là các thế hệ cũ, rất dễ rơi vào vòng lặp vô hạn của các cụm từ. Ví dụ ở đây, với kích thước chùm 32, GPT-2 bị mắc kẹt khi lặp liên tục các từ *"singer-songwriter"* và *"songwriter"*. <br><br>Để khắc phục, người ta sử dụng hình phạt lặp – tức là giảm trực tiếp điểm số của các từ đã xuất hiện trong logits lấy mẫu. Một cách khác triệt để hơn là huấn luyện phi xác suất, chủ động phạt mô hình khi nó sinh các token lặp lại ngay trong quá trình huấn luyện. |
| **25:25 - 26:20** | **Cạm bẫy 2 — Xu hướng chuỗi ngắn (Short Sequences):**<br>- Tiêu đề phụ: **"2. Xu hướng Chuỗi ngắn (Short Sequences)"**.<br>- Giải thích hiện tượng tích xác suất giảm dần một cách đơn điệu khi chuỗi dài ra.<br>- Trực quan hóa phép so sánh từ slide của tác giả bằng hộp màu đỏ:<br>$$p_\theta(	ext{"Taylor Swift is <eos>"}) > p_\theta(	ext{"Taylor Swift is an American singer-..."})$$<br>- Xuất hiện công thức chuẩn hóa độ dài log-xác suất trung bình:<br>$$\text{Score}(y) = \frac{1}{\lvert y \rvert} \sum_{t=1}^T \log p_\theta(y_t \mid y_{<t})$$ | Cạm bẫy thứ hai là Xu hướng chuỗi ngắn. Vì xác suất của chuỗi được tính bằng tích các giá trị từ 0 đến 1, nên khi chuỗi càng dài, xác suất của nó càng giảm dần một cách đơn điệu. Hệ quả là mô hình luôn có xu hướng ưu tiên các chuỗi cực kỳ ngắn hoặc kết thúc bằng token `<eos>` quá sớm.<br><br>Ví dụ, câu cực ngắn kết thúc bằng `<eos>` sẽ có xác suất toán học lớn hơn nhiều so với một câu dài đầy đủ thông tin. Để khắc phục điều này, người ta áp dụng phương pháp chuẩn hóa độ dài, chia tổng log-xác suất cho độ dài chuỗi để tính điểm trung bình cho mỗi token, giúp các chuỗi dài có cơ hội cạnh tranh công bằng. |
| **26:20 - 27:40** | **Cạm bẫy 3 — Tính không điển hình (Atypicality):**<br>- Tiêu đề phụ: **"3. Tính không điển hình (Atypicality)"**.<br>- Trực quan hóa thí nghiệm tư duy đồng xu lệch: $P[H] = 0.6$ và $P[T] = 0.4$.<br>- Minh họa chuỗi có xác suất đơn lẻ cao nhất khi tung 100 lần là toàn Ngửa: `H H H H ... H` với xác suất $0.6^{100} \approx 6.53 \times 10^{-23}$.<br>- Giải thích chi tiết toán học về Typical Set để làm rõ phần tác giả lướt qua:<br>  - Một chuỗi điển hình (e.g. 60 H - 40 T) có xác suất một chuỗi đơn lẻ là $0.6^{60} \times 0.4^{40} \approx 5.67 \times 10^{-29}$ (nhỏ hơn 1 triệu lần so với chuỗi toàn H).<br>  - Nhưng số lượng tổ hợp của chuỗi điển hình lại khổng lồ: $C(100, 60) \approx 1.37 \times 10^{28}$.<br>  - Kết quả là tổng xác suất của tập điển hình lên tới $77.7\%$, trong khi xác suất của chuỗi toàn H gần như bằng $0$.<br>- Hiện hộp giải thích liên hệ ngôn ngữ học: Chuỗi có xác suất cao nhất thường tẻ nhạt, ít thông tin và không điển hình cho cách nói tự nhiên của con người. | Cạm bẫy thứ ba và cũng là cạm bẫy thú vị nhất về mặt lý thuyết thông tin là Tính không điển hình. Hãy cùng làm một thí nghiệm tư duy: Nếu tung một đồng xu lệch có xác suất Ngửa là 0.6 và Sấp là 0.4 tổng cộng 100 lần. Chuỗi có xác suất đơn lẻ lớn nhất về mặt toán học chính là chuỗi toàn Ngửa, vì 0.6 lớn hơn 0.4.<br><br>Nhưng nếu bạn tung đồng xu 100 lần và nhận được 100 lần Ngửa liên tiếp, bạn sẽ cực kỳ kinh ngạc. Vì kết quả này hoàn toàn không điển hình cho một đồng xu chỉ lệch nhẹ. Thực tế ta kỳ vọng có khoảng 60 lần Ngửa và 40 lần Sấp.<br><br>Tại sao lại như vậy? Hãy nhìn vào toán học: Xác suất của một chuỗi điển hình 60 Ngửa - 40 Sấp đơn lẻ chỉ khoảng $5.67 \times 10^{-29}$, nhỏ hơn chuỗi toàn Ngửa tới 1 triệu lần. Tuy nhiên, số lượng chuỗi có cấu trúc 60 Ngửa - 40 Sấp lại cực kỳ lớn, lên tới $1.37 \times 10^{28}$ chuỗi. Nhân lại, tổng xác suất để nhận được một kết quả điển hình lên tới gần 78 phần trăm. Trong ngôn ngữ cũng vậy, chuỗi từ có xác suất MAP lớn nhất thực chất lại là chuỗi tẻ nhạt nhất, ít lượng thông tin nhất và không hề tự nhiên so với cách nói điển hình của con người. |
| **27:40 - 28:00** | **Tổng kết & Lời khuyên của Tác giả:**<br>- Nhấn mạnh kết luận: Cực đại hóa xác suất thuần túy (MAP) không mang lại kết quả tự nhiên.<br>- Hiện hộp kết luận: Sử dụng MAP xấp xỉ (như chùm hẹp) hoạt động tốt hơn MAP chính xác.<br>- Giới thiệu phương pháp Lấy mẫu (Sampling) là hướng giải quyết cốt lõi để sinh văn bản tự nhiên. | Tóm lại, việc tối đa hóa xác suất một cách chính xác không phải là cái đích tối ưu để sinh văn bản tự nhiên. Trong thực tế, các giải thuật MAP xấp xỉ như tìm kiếm chùm hẹp lại hoạt động tốt hơn. Và để thực sự tạo ra văn bản tự nhiên và phong phú như con người, chúng ta cần chuyển dịch sang một trường phái hoàn toàn mới: Lấy mẫu - Sampling, nội dung chúng ta sẽ tìm hiểu ngay sau đây. |

### Phân cảnh 2.4: Lấy mẫu & Truncation (Top-k vs. Top-p & Nhiệt độ) (28:00 - 32:00)
*   **Hình ảnh (3B1B Style):**
    *   **Lấy mẫu tổ tiên & Đuôi nặng (Ancestral Sampling & Heavy Tail):**
        *   Hiển thị công thức lấy mẫu tổ tiên: $y_t \sim p_\theta(\cdot | x, y_{<t})$ và công thức phân rã chuỗi xác suất: $p_\theta(y) = \prod p_\theta(y_t | y_{<t})$.
        *   Biểu đồ cột xác suất từ vựng (is, ,, and, has, here, actor, award, Beyoncé) minh họa đuôi nặng (heavy tail). Hoạt họa bộ quét lựa chọn ngẫu nhiên rơi vào token xác suất thấp `"Beyoncé"`.
        *   Hiển thị so sánh 3 đoạn văn bản thực tế (Slide 53-54) chứng minh nhược điểm:
            *   *Greedy (Repetitive):* Văn bản bị lặp vô hạn `"It's a very sad day... sad day... sad day..."`.
            *   *Ancestral (Incoherent):* Văn bản bị mất nhất quán sang chủ đề khác do bốc phải token rác ở đuôi: `"...female songstress, Beyoncé."`.
            *   *Top-k (Acceptable):* Văn bản mạch lạc, chấp nhận được: `"Taylor Swift is a writer for IGN..."`.
    *   **Bảng các phương pháp Truncation (Slide 55):**
        *   Hiển thị bảng tóm tắt 5 phương pháp cắt đuôi và chiến lược ngưỡng của chúng: Top-k, Top-p, Epsilon, Eta, Min-p.
    *   **Nhiệt độ ($\tau$):**
        *   Hiển thị công thức soft-max có nhiệt độ: $\text{softmax}(z, \tau)_i = \exp(z_i / \tau) / \sum \exp(z_j / \tau)$.
        *   Thanh Slider nhiệt độ chạy động từ $0.2 \to 2.0$ làm thay đổi trực tiếp độ nhọn của các cột biểu đồ: $\tau = 0.2$ (cực nhọn/greedy), $\tau = 2.0$ (cực phẳng/đồng đều).
        *   Hiển thị bảng so sánh Pro/Con của Nhiệt độ (Slide 59): High $\tau \ge 1$ (Diverse (+) nhưng Incoherent (-)) vs. Low $\tau < 1$ (Coherent (+) nhưng Repetitive (-)).
    *   **Nhược điểm Top-k (Flat vs Sharp - Slide 57):**
        *   *Trường hợp Phân phối Phẳng (Flat) "My name":* Các cột từ vị trí $1$ đến $k+5$ đều có chiều cao tương đương nhau. Hoạt họa đường cắt K = 5 tô đỏ cắt đi các từ tiềm năng ở vị trí $K+1, K+2$ (như "said", "in") có xác suất gần bằng từ ở vị trí K.
        *   *Trường hợp Phân phối Dốc (Sharp) "Taylor Swift is":* Chỉ có 2-3 cột đầu tiên là cao vọt, từ cột thứ 4 trở đi xẹp sát đáy. Hoạt họa đường cắt K = 5 cho thấy đường cắt lấy thêm rất nhiều token rác ở phần đuôi có xác suất cực thấp gần như bằng 0.
    *   **Top-p (Nucleus) - Giải pháp Ngưỡng động (Slide 58):**
        *   Vùng phủ màu xanh lá tự động co giãn kích thước tùy theo độ dốc của phân phối để tổng diện tích đạt đúng giá trị $p$ (ví dụ 0.90), tạo ra một ngưỡng cắt linh hoạt và động (dynamic threshold). Cột Sharp chỉ lấy 4 từ, cột Flat lấy toàn bộ.
    *   **Bảng Code mẫu & Frameworks (Slide 61-62):**
        *   Bảng code `sampling_implementations.py` đầy đủ bao gồm cả dòng Epsilon: `indices, weights = vocab_size, probs * (probs > epsilon)`.
        *   Hiển thị code thực tế sử dụng các thư viện tích hợp (Slide 62): vLLM (`SamplingParams(temperature=0.8, top_p=0.95)`) và HuggingFace (`model.generate(...)`).
    *   **Lý do phân phối có đuôi nặng (Slide 63-65):**
        *   Hiển thị slide giải thích 3 nguyên nhân cốt lõi: 1. Under-training (Huấn luyện chưa đủ), 2. Mode-seeking (Cross-entropy phạt nặng lỗi thiếu xác suất), 3. Low-rank constraints (Hạn chế về hạng biểu diễn của LLM).
*   **Lời thoại Voiceover (Dịch chi tiết từ phụ đề):**
    > "Bây giờ chúng ta sẽ chuyển sang phương pháp Lấy mẫu (Sampling) – cách thức thống trị hiện nay. Lấy mẫu cơ bản nhất là Lấy mẫu tổ tiên (Ancestral Sampling), tức là bốc ngẫu nhiên token tiếp theo trực tiếp từ phân phối của mô hình. 
    > 
    > Tuy nhiên, lấy mẫu tổ tiên thuần túy có một nhược điểm chí mạng: nó rất dễ gặp hiện tượng đuôi nặng (Heavy tail). Hãy nhìn vào biểu đồ, các token ở phần đuôi dù có xác suất đơn lẻ rất thấp, nhưng khi cộng dồn lại, chúng có tổng xác suất rất lớn. Do đó mô hình cực kỳ dễ bốc phải một từ vô nghĩa và làm lệch lạc toàn bộ câu văn.
    > 
    > Hãy so sánh ba đoạn văn bản thực tế trên màn hình: Phương pháp Greedy giải mã tham lam dẫn đến cạm bẫy lặp từ vô hạn tẻ nhạt. Phương pháp Ancestral lại dẫn đến sự mất nhất quán vô nghĩa khi chọn phải từ 'Beyoncé' ở phần đuôi. Chỉ có Truncation - cắt đuôi phân phối mới giúp chúng ta đạt được văn bản chấp nhận được. Tác giả giới thiệu 5 chiến lược cắt đuôi chính gồm Top-k, Top-p, Epsilon, Eta và Min-p như bảng tóm tắt trên.
    > 
    > Để điều chỉnh độ tập trung của phân phối trước khi cắt đuôi, chúng ta dùng Nhiệt độ (Temperature Sampling). Hệ số nhiệt độ $\tau$ chia trực tiếp cho logits trong hàm Softmax. Như thanh slider mô phỏng, nhiệt độ cao làm phân phối phẳng hơn, tăng độ đa dạng nhưng dễ mất nhất quán; nhiệt độ thấp làm phân phối nhọn hơn, tăng độ tự tin nhưng dễ dẫn đến lặp từ.
    > 
    > Kỹ thuật cắt đuôi đơn giản nhất là Top-K – chỉ giữ lại đúng K token cao nhất để lấy mẫu. Tuy nhiên, Top-K có nhược điểm lớn ở hai thái cực phân phối: Khi phân phối phẳng như câu 'My name', nhiều từ đồng nghĩa có xác suất ngang nhau, Top-K sẽ cắt bỏ các từ rất tiềm năng ở ngay sau vị trí K. Ngược lại, khi phân phối dốc như câu 'Taylor Swift is', chỉ có 2-3 từ đầu là có nghĩa, Top-K lại lấy thừa rất nhiều từ rác ở đuôi dù xác suất của chúng gần như bằng không.
    > 
    > Để giải quyết triệt để vấn đề này, Top-P (hay Nucleus Sampling) ra đời để tạo ra một ngưỡng cắt động. Thay vì cố định số lượng từ K, Top-P sử dụng tổng xác suất tích lũy. Phạm vi lấy mẫu sẽ tự động co giãn dựa trên độ dốc của phân phối để đảm bảo tổng xác suất của các token được chọn đạt đúng giá trị p (ví dụ 90%).
    > 
    > Đoạn mã lập trình thực tế của các phương pháp này được thể hiện trong script `sampling_implementations.py` bao gồm cả bộ lọc Epsilon. Trong thực tế, các framework hiện đại như vLLM và HuggingFace đã tích hợp sẵn các tham số này một cách tối ưu.
    > 
    > Về mặt lý thuyết, tại sao phân phối của LLM lại luôn bị đuôi nặng? Có ba nguyên nhân chính: Thứ nhất là do mô hình chưa được huấn luyện đủ (Under-training). Thứ hai là do hàm phạt Cross-entropy có tính chất Mode-seeking, phạt rất nặng các lỗi ước lượng thiếu xác suất. Và thứ ba là do các giới hạn hạng ma trận biểu diễn (Low-rank constraints) vốn có của LLM. Việc hiểu rõ bản chất này giúp chúng ta thiết kế các thuật toán lấy mẫu tốt hơn."

### Phân cảnh 2.5: Sampling Adapters & Giải mã ràng buộc (32:00 - 40:00)
*   **Hình ảnh (3B1B Style):**
    *   **Sampling Adapters (Contrastive Decoding):**
        *   Hiển thị hai biểu đồ phân phối xác suất xếp chồng hoặc song song: Phân phối của mô hình Chuyên gia (Expert - lớn, thông minh) và Phân phối của mô hình Phản chuyên gia (Anti-expert - nhỏ, lặp).
        *   Hiển thị công thức log: $\log P_{CD}(y \mid x) \propto \log P_{expert}(y \mid x) - \alpha \log P_{anti-expert}(y \mid x)$ và công thức tỷ lệ xác suất.
        *   Hoạt họa quá trình thay đổi $\alpha$ và "trừ" trực tiếp chiều cao của các cột xác suất. Các token lặp lại và vô nghĩa bị kéo tụt xuống 0, trong khi các token đặc trưng thông minh nhô cao nổi bật.
        *   So sánh văn bản sinh ra giữa hai chế độ để làm nổi bật tác dụng chống lặp và tăng độ sắc bén.
    *   **Constrained Decoding (Giải mã ràng buộc JSON):**
        *   Hiển thị lược đồ JSON Schema ở bên góc: `{"name": "string", "birth year": "int"}`.
        *   Vẽ Máy trạng thái hữu hạn (DFA State Machine) dạng đồ thị gồm các nút tròn kết nối bằng các mũi tên chuyển trạng thái đại diện cho từng thành phần cú pháp JSON (State 0 -> State 1 -> State 2 -> State 6 -> State 4 -> State 7 -> State 8).
        *   Vẽ bảng từ vựng (Vocabulary Table) ở bên phải. Hoạt họa quá trình lọc: các token không hợp lệ theo DFA bị tô đỏ, gạch ngang, logits chuyển thành $-\infty$ và xác suất sụt giảm về 0%; các token hợp lệ được tô xanh và tái chuẩn hóa xác suất.
        *   Tích lũy chuỗi JSON sinh ra ở dưới đáy màn hình tương ứng với các nút DFA sáng xanh lá lần lượt qua 6 bước cụ thể.
    *   **Side Effects of Constrained Decoding (Tác dụng phụ - Slide 82):**
        *   Hiển thị slide so sánh 2 tác động phụ:
            *   *Generation speedup:* Tăng tốc độ sinh (hộp xanh lá phát sáng khi hệ thống tự điền các đoạn mã chỉ có một lối đi duy nhất).
            *   *Reduced performance:* Giảm hiệu năng do lệch ranh giới tokenizer (hộp cam cảnh báo).
    *   **Token Boundary Bias & Token Healing:**
        *   Minh họa chuỗi prompt định mẫu `"The URL is http:"`.
        *   Vẽ các mảnh ghép (puzzle blocks) đại diện cho phân đoạn token của tokenizer: `[The]` `[ URL]` `[ is]` `[ http]` `[:]`.
        *   Chỉ ra lỗi khi ghép nối độc lập mảnh tiếp theo `[//]` vì mô hình pretrain chỉ quen thuộc với token nguyên khối `[http://]`. Show tia sét đỏ hoặc biểu tượng cảnh báo lệch ranh giới rập rình.
        *   **Token Healing**: Hoạt họa tua ngược (rewind) tokenizer lại 1 bước, rút mảnh `[:]` ra để prompt dừng lại ở `"http"`. Áp đặt ràng buộc tiền tố cho token tiếp theo phải bắt đầu bằng `":"`.
        *   Hiển thị hộp Candidates chứa các lựa chọn từ từ vựng: `s://` (bị loại bỏ và gạch đỏ) và `://` (được tô xanh và chọn).
        *   Mô hình chọn được token nguyên khối tối ưu `[://]`. Ghép nối các mảnh ghép hoàn chỉnh `[The]` `[ URL]` `[ is]` `[ http]` `[://]` phát sáng xanh lá dịu nhẹ biểu thị ranh giới được chữa lành hoàn hảo.
        *   Hiển thị giải pháp thay thế: *"Alternative fix: Tokenizer regularization during training [Kudo, 2018]"*.
*   **Lời thoại Voiceover (Dịch chi tiết từ phụ đề):**
    > "Bên cạnh các phương pháp cắt đuôi phân phối như Top-K hay Top-P, chúng ta còn có các Bộ điều chỉnh lấy mẫu (Sampling Adapters) để tinh chỉnh phân phối xác suất một cách thông minh hơn. Điển hình nhất trong số đó là kỹ thuật Giải mã tương phản – Contrastive Decoding.
    > 
    > Hãy hình dung việc kết hợp hai bộ não: một mô hình lớn đóng vai trò chuyên gia – Expert, thông minh nhưng đôi khi vẫn lặp lại các cụm từ sáo rỗng; và một mô hình nhỏ đóng vai trò phản chuyên gia – Anti-expert, đại diện cho những lỗi lặp tẻ nhạt và hành vi cẩu thả của mô hình.
    > 
    > Bằng cách lấy phân phối xác suất của mô hình lớn trừ đi phân phối của mô hình nhỏ trong miền logarithm – như công thức các bạn đang thấy trên màn hình – chúng ta có thể triệt tiêu hoàn toàn các token lặp lại và vô nghĩa. Những cột xác suất rác bị kéo tụt xuống, nhường chỗ cho những lựa chọn sáng tạo và sắc bén của mô hình chuyên gia nổi bật lên ở đỉnh phân phối.
    > 
    > Một thách thức lớn khác khi đưa mô hình vào các hệ thống phần mềm thực tế là làm thế nào để chúng giao tiếp một cách đáng tin cậy. Chúng ta không thể để mô hình sinh văn bản tự do khi hệ thống yêu cầu một cấu trúc dữ liệu nghiêm ngặt như JSON hay SQL. Đây là lúc giải thuật Giải mã ràng buộc – Constrained Decoding vào cuộc.
    > 
    > Ý tưởng cốt lõi là biên dịch lược đồ định dạng – ví dụ như JSON Schema – thành một máy trạng thái hữu hạn DFA. Máy trạng thái này hoạt động song song với quá trình giải mã, kiểm soát nghiêm ngặt từng ký tự được sinh ra. Tại mỗi bước sinh token tiếp theo, DFA sẽ duyệt qua toàn bộ từ vựng và chỉ ra các token nào đáp ứng đúng cú pháp.
    > 
    > Đối với tất cả các token vi phạm cấu pháp, hệ thống sẽ thực hiện một bộ lọc cứng: gán điểm số logits của chúng về giá trị âm vô cùng ($-\infty$). Điều này làm cho xác suất của chúng sau hàm Softmax sụt giảm tuyệt đối về 0%. Mô hình chỉ được phép lựa chọn trong số các token hợp lệ còn lại. Hãy cùng quan sát quá trình sinh chuỗi JSON này từng bước qua hoạt ảnh máy trạng thái... [Dành khoảng 30-40 giây chờ hoạt ảnh chạy qua 6 bước]... Bằng cách này, chúng ta đảm bảo 100% dữ liệu đầu ra luôn khớp chính xác với cấu trúc lập trình mong muốn mà không lo bị lỗi phân tích cú pháp.
    > 
    > Mặc dù vậy, việc áp đặt các ràng buộc cứng này cũng mang lại các tác dụng phụ hai mặt. Một mặt, nó có thể tăng tốc độ sinh (Generation speedup) vì khi chỉ có một đường đi hợp lệ duy nhất, hệ thống có thể tự động điền mà không cần LLM tính toán. Mặt khác, nó lại làm giảm hiệu năng lập luận của mô hình (Reduced performance) do cơ chế phân tách từ của Tokenizer bị ảnh hưởng. Hiện tượng này được gọi là Lệch ranh giới token – Token Boundary Bias.
    > 
    > Hãy xem xét ví dụ khi prompt của bạn bị ép buộc kết thúc bằng chuỗi ký tự `"The URL is http:"`. Vì ranh giới prompt bị dừng ngay tại dấu hai chấm, Tokenizer bắt buộc phải cắt chữ thành các mảnh ghép độc lập: mảnh `[ http]` và mảnh `[:]`. Để viết tiếp địa chỉ web, mô hình buộc phải sinh token tiếp theo bắt đầu bằng hai dấu gạch chéo `[//]`. Nhưng trong hàng ngàn gigabyte dữ liệu huấn luyện, mô hình hầu như chỉ nhìn thấy token nguyên khối `[http://]` chứ rất hiếm khi gặp chuỗi cắt rời `[http] + [:] + [//]`. Sự lệch pha ranh giới này khiến mô hình bị bối rối và dễ sinh ra các token rác sau đó.
    > 
    > Giải thuật Chữa lành Token – Token Healing xử lý vấn đề này một cách cực kỳ tinh tế. Hệ thống sẽ chủ động tua ngược tokenizer lại một bước, loại bỏ token `[:]` cuối cùng để prompt dừng ở chữ `"http"`. Sau đó, ở bước sinh tiếp theo, hệ thống áp đặt một ràng buộc tiền tố: token mới được sinh ra bắt buộc phải bắt đầu bằng ký tự dấu hai chấm `":"`.
    > 
    > Từ hộp từ vựng, hệ thống lọc ra các ứng viên: token `s://` bị loại bỏ vì không khớp tiền tố, còn token nguyên khối `://` được lựa chọn để khớp khít hoàn hảo vào chuỗi. Bên cạnh Token Healing ở giai đoạn suy luận, chúng ta cũng có một giải pháp thay thế khác là áp dụng Tokenizer Regularization trong quá trình huấn luyện [Kudo, 2018] để tăng độ bền bỉ của mô hình trước các ranh giới lệch."


---

## 🎬 CHƯƠNG 3: BỘ ĐIỀU PHỐI CẤP CAO (META-GENERATION STRATEGIES)
*Thời lượng: ~45 phút (40:00 - 01:25:00 trong subtitle gốc | Người trình bày: Sean Welleck)*

### Phân cảnh 3.1: Các mô hình đánh giá và kỹ thuật Chaining (40:00 - 50:00)
*   **Hình ảnh (3B1B Style):**
    *   **Giới thiệu Bộ điều phối cấp cao (Meta-Generation Introduction):**
        *   Hiển thị một khối hộp xám đậm lớn đại diện cho "Base Generator (Chương 2)". Hoạt họa các token đầu vào $x$ đi vào và token đầu ra $y$ đi ra khỏi hộp đen.
        *   Bao bọc bên ngoài bằng một khung màu xanh dương sáng nhãn "Meta-Generation Controller (Chương 3)" để biểu thị tầng điều khiển vĩ mô không can thiệp trọng số.
    *   **Outcome-based Reward Model (Evaluator / Verifier):**
        *   Vẽ các khối biểu thị câu hỏi $x$ và các cặp câu trả lời: câu đúng màu xanh lá (nhãn $\checkmark$) và câu sai màu đỏ (nhãn $\times$).
        *   Các câu này chảy tuần tự vào khối trung tâm "Classifier Block". Classifier chấm điểm và xuất ra điểm số phần thưởng trực quan $R(x,y) \in [0, 1]$ dạng thanh hiển thị tỉ lệ phần trăm.
        *   Làm nổi bật nhãn "Outcome-based: Chỉ đánh giá tại thời điểm kết thúc chuỗi văn bản" bằng chữ màu vàng để người xem chú ý.
    *   **Kỹ thuật Chaining & Chain of Thought (CoT):**
        *   Trình bày biểu đồ so sánh hai luồng suy luận: Direct Generation ($x \to$ Generator $\to$ $y$ - kết quả sai) vs. Chaining ($x \to$ Generator $\to$ suy nghĩ trung gian $z \to$ Generator $\to$ $y$ - kết quả đúng).
        *   Vẽ hoạt ảnh băng ghi Turing Machine (Scratchpad Memory Tape) gồm một chuỗi ô dài dịch chuyển trái phải chứa các token trung gian $z$, tượng trưng cho bộ nhớ phụ tăng khả năng lập luận biểu đạt (expressiveness).
    *   **Quy trình Self-Ask & Gọi công cụ (Tool Use):**
        *   Hiển thị câu hỏi ví dụ thực tế: *"Khi nào tổng thống Mỹ sinh cùng năm với Taylor Swift qua đời?"*
        *   Vẽ sơ đồ luồng dữ liệu (Flowchart) tự hỏi gồm 3 bước:
            1. Sinh câu hỏi phụ 1: *"Taylor Swift sinh năm nào?"* $\to$ gọi Search Tool $\to$ trả về `"1989"`.
            2. Sinh câu hỏi phụ 2: *"Tổng thống Mỹ nào sinh năm 1989 và đã qua đời?"* $\to$ gọi Search Tool $\to$ trả về `"Không có"`.
            3. Sinh câu trả lời tổng hợp: `"Không có tổng thống Mỹ nào..."`.
        *   Hoạt họa ánh sáng chạy dọc các đường mũi tên kết nối giữa Generator và khối công cụ Search/Calculator.
    *   **Tổng quan phân loại chiến lược mô hình (Preview Slide):**
        *   Hiển thị bảng phân loại 4 nhóm tiếp cận của Chương 3 dưới dạng lưới 2x2:
            1. Chaining & CoT (Chuỗi hóa): Phân rã lập luận logic đa bước. Sinh các token z làm băng đệm.
            2. Parallel (Sinh song song): Best-of-N, Majority Voting, MBR.
            3. Tree Search (Tìm kiếm trên cây): Duyệt cây ToT, MCTS, Backtracking. Sử dụng PRM đánh giá từng bước lập luận.
            4. Self-Correction (Tự sửa lỗi): Mô hình tự chỉnh sửa bản nháp qua feedback ngoại sinh/nội sinh.
*   **Lời thoại Voiceover (Dịch chi tiết từ phụ đề):**
    > "Chào mừng các bạn đến với Chương 3: Bộ điều phối cấp cao – hay Meta-Generation Strategies. Trong suốt chương 2, chúng ta đã tìm hiểu sâu về các phương pháp sinh token ở cấp độ thấp, điều chỉnh logits hoặc ranh giới token. Ở Chương 3, chúng ta sẽ nâng tầm nhìn lên một mức độ vĩ mô hơn.
    > 
    > Hãy coi toàn bộ các giải thuật sinh ở chương 2 như một chiếc hộp đen – Base Generator. Chúng ta sẽ không can thiệp vào bên trong chiếc hộp này hay thay đổi các trọng số của mô hình. Thay vào đó, chúng ta sẽ thiết kế một bộ điều phối cấp cao bao bọc bên ngoài, sử dụng các thuật toán điều phối để hướng dẫn và kiểm soát luồng sinh chữ.
    > 
    > Để làm được điều này một cách hiệu quả, thành phần nền tảng đầu tiên chúng ta cần là một Mô hình phần thưởng đánh giá kết quả – Outcome-based Reward Model, hay còn gọi là Evaluator hoặc Verifier.
    > 
    > Khác với mô hình ngôn ngữ thông thường sinh từ tự nhiên, Evaluator được huấn luyện dưới dạng một bộ phân loại. Nó nhận đầu vào là câu hỏi và toàn bộ câu trả lời hoàn chỉnh được sinh ra, sau đó chấm một điểm số phần thưởng biểu thị độ chính xác hoặc chất lượng của câu trả lời đó. Cần nhấn mạnh rằng, điểm số này chỉ được tính ở điểm cuối cùng của văn bản. Evaluator không biết và không quan tâm mô hình đã lập luận thế nào ở giữa chừng, mà chỉ đánh giá kết quả cuối cùng.
    > 
    > Dựa trên Evaluator và Base Generator, chiến lược điều phối cấp cao đầu tiên và kinh điển nhất là Chuỗi hóa – Chaining.
    > 
    > Hãy tưởng tượng khi đối mặt với một bài toán toán học hay lập luận logic phức tạp, nếu ta yêu cầu mô hình sinh ngay đáp án cuối cùng chỉ sau một bước xử lý – gọi là Direct Generation – tỷ lệ sai sót sẽ rất cao. Điều này là do giới hạn về mặt kiến trúc tính toán của mô hình Transformer trong một bước sinh đơn lẻ.
    > 
    > Kỹ thuật Chaining giải quyết điều này bằng cách phân rã bài toán lớn thành các bước sinh tuần tự. Mô hình sẽ sinh ra các bước lập luận trung gian – ký hiệu là z – trước khi sinh ra đáp án cuối cùng y. Đây chính là bản chất của phương pháp Chain of Thought nổi tiếng.
    > 
    > Về mặt khoa học máy tính, các token lập luận trung gian này hoạt động giống như một bộ nhớ băng ghi – hay scratchpad – tương tự như băng ghi của máy Turing. Việc viết ra các suy nghĩ trung gian giúp tăng khả năng biểu đạt của hệ thống, cho phép mô hình có không gian tính toán để lưu trữ và cập nhật trạng thái lập luận qua từng bước.
    > 
    > Để tối ưu hóa hơn nữa, chúng ta có thể thiết kế các cấu trúc chuỗi phức tạp hơn, tiêu biểu là mô hình tự hỏi – Self-Ask, kết hợp với khả năng gọi công cụ bên ngoài.
    > 
    > Hãy cùng quan sát một ví dụ thực tế. Khi nhận câu hỏi phức tạp: 'Khi nào tổng thống Mỹ sinh cùng năm với Taylor Swift qua đời?', mô hình sẽ không cố gắng trả lời ngay. Thay vào đó, bộ điều phối sẽ kích hoạt tiến trình Self-Ask:
    > 
    > Đầu tiên, mô hình tự đặt câu hỏi phụ thứ nhất: 'Taylor Swift sinh năm nào?'. Câu hỏi này được chuyển hướng sang công cụ Tìm kiếm. Công cụ trả về dữ liệu: 'Năm 1989'.
    > 
    > Tiếp theo, mô hình dùng thông tin này để tự đặt câu hỏi phụ thứ hai: 'Tổng thống Mỹ nào sinh năm 1989 và đã qua đời?'. Công cụ tìm kiếm trả về: 'Không có tổng thống Mỹ nào sinh năm 1989'.
    > 
    > Cuối cùng, mô hình tổng hợp thông tin từ các bước trung gian để đưa ra kết luận chính xác. Quy trình này không chỉ làm giảm ảo giác của mô hình mà còn biến một bài toán lập luận đa bước phức tạp thành các bài toán con đơn giản có sự hỗ trợ của các công cụ tính toán chính xác.
    > 
    > Như vậy, chúng ta đã đi qua phương pháp điều phối đầu tiên là Chaining và kỹ thuật Self-Ask. Nhìn tổng quan, các chiến lược Meta-Generation trong Chương 3 này sẽ được chia làm 4 nhóm chính: thứ nhất là Chaining và Chain of Thought – chuỗi lập luận tuần tự sử dụng bộ nhớ băng ghi; thứ hai là các giải thuật song song – như Best-of-N, Majority Voting hay Minimum Bayes Risk mà chúng ta sẽ tìm hiểu ở phân cảnh tiếp theo; thứ ba là Tìm kiếm trên cây và quay lui – cho phép mô hình đi tìm đường đi tối ưu và sửa sai giữa chừng bằng mô hình PRM; và cuối cùng là các kỹ thuật Tinh chỉnh và Tự sửa lỗi – nơi mô hình tự sửa bản nháp thông qua các nguồn phản hồi bên trong hoặc bên ngoài."

### Phân cảnh 3.2: Giải thuật sinh song song (Best-of-N, Voting, MBR) (50:00 - 01:02:00)
*   **Hình ảnh (3B1B Style):**
    *   **Best-of-N:** 5 luồng văn bản song song chạy ra từ prompt gốc. Một biểu tượng cán cân (Reward Model) cân đo điểm số cho từng luồng: Luồng 1 đạt 0.1, Luồng 2 đạt 0.9 (được chọn). Hiện nhãn "Reward Hacking" cảnh báo.
    *   **Majority Voting / Self-Consistency:** 
        *   Hiện công thức toán học về hội tụ biên rộng (Marginalization) dạng LaTeX nổi bật ở giữa màn hình:
        $$\arg\max_y \sum_{z} P(y, z \mid X)$$
        *   Trong đó, ký tự $z$ (chuỗi suy nghĩ trung gian - CoT) phát sáng màu xanh lá cây, và ký tự $y$ (câu trả lời cuối cùng) phát sáng màu vàng.
    *   **Minimum Bayes Risk (MBR):** Một ma trận tương đồng $2D$ giữa các câu trả lời ngữ nghĩa (Utility). Công thức MBR hiện lên: $\arg\max_{y} \sum_{j} U(y, y^{(j)})$.
*   **Lời thoại Voiceover (Dịch chi tiết từ phụ đề):**
    > "Chiến lược thứ hai là Sinh song song (Parallel Generation).
    > 
    > Ý tưởng cơ bản nhất là Best-of-N (hay Rejection Sampling): chúng ta sinh song song $N$ câu trả lời hoàn chỉnh độc lập, dùng mô hình phần thưởng đánh giá từng câu và chọn câu có điểm Reward cao nhất. Tuy nhiên, Best-of-N rất dễ bị cạm bẫy 'lừa bộ chấm điểm' (Reward Hacking) – nơi mô hình tìm ra các câu trả lời có điểm đánh giá rất cao nhưng thực tế lại sai hoặc vô nghĩa.
    > 
    > Để khắc phục, chúng ta sử dụng các thuật toán biểu quyết. Đơn giản nhất là Đa số biểu quyết (Majority Voting / Self-Consistency) – biểu quyết theo số đông dựa trên tần suất đáp án cuối cùng xuất hiện nhiều nhất.
    > 
    > Đi xa hơn là Biểu quyết có trọng số (Weighted Voting), dùng điểm của Reward Model làm trọng số biểu quyết. Bản chất toán học của quá trình này là phép tính tổng biên (Marginalization) qua toàn bộ các chuỗi suy nghĩ trung gian $z$ để chọn ra đáp án cuối cùng $y$ có xác suất biên lớn nhất, giúp tăng độ chính xác theo định lý giới hạn.
    > 
    > Ngoài ra, chúng ta còn có thuật toán Rủi ro Bayes tối thiểu (Minimum Bayes Risk - MBR). Thay vì đếm tần suất trùng khớp thô sơ, MBR tính toán ma trận độ tương đồng ngữ nghĩa giữa các đáp án sinh ra và chọn ra câu trả lời có rủi ro thấp nhất – tức là câu trả lời có độ tương đồng lớn nhất với tất cả các câu trả lời còn lại."

### Phân cảnh 3.3: Tìm kiếm trên cây và Quay lui (Tree Search & Backtracking) (01:02:00 - 01:15:00)
*   **Hình ảnh (3B1B Style):**
    *   Một cây quyết định lớn. Nút gốc là câu hỏi toán. Các nút con biểu diễn các bước lập luận trung gian.
    *   Các nút con được dán điểm bởi Process-based Reward Model (PRM): nút tốt được tô viền xanh lá (điểm 0.95), nút tồi tô viền đỏ (điểm 0.20).
    *   Hoạt ảnh thuật toán tìm kiếm duyệt qua cây. Khi đi vào nút đỏ (0.20), đường đi chuyển sang màu đỏ rực, co lại và quay ngược lại nút cha (Backtracking), sau đó mở rộng sang nhánh xanh lá (0.95).
*   **Lời thoại Voiceover (Dịch chi tiết từ phụ đề):**
    > "Các phương pháp song song sinh toàn bộ chuỗi từ đầu đến cuối rồi mới đánh giá. Nhưng nếu mô hình phạm sai lầm ngay từ bước đầu tiên, toàn bộ tính toán phía sau sẽ bị lãng phí. Điều này dẫn chúng ta đến giải pháp thứ ba: Tìm kiếm trên cây quyết định (Tree Search).
    > 
    > Ở đây, chúng ta phân rã lời giải thành một cây quyết định, nơi mỗi nút đại diện cho một bước lập luận hoặc một câu văn. Thay vì chấm điểm ở cuối đường đi, chúng ta sử dụng Mô hình phần thưởng tiến trình (Process-based Reward Model - PRM). PRM được huấn luyện để chấm điểm từng bước một, dự đoán xem từ trạng thái hiện tại có dẫn đến câu trả lời đúng hay không.
    > 
    > Khi chạy các thuật toán như Tree of Thoughts (ToT) hay Monte Carlo Tree Search (MCTS), chúng ta có thể điều phối tài nguyên tính toán dựa trên điểm số này. Nếu một hướng đi bị PRM đánh giá thấp, thuật toán sẽ thực hiện Quay lui (Backtracking), rút lui về trạng thái trước đó để thử một hướng đi triển vọng hơn. Kỹ thuật này cực kỳ hiệu quả trong các bài toán chứng minh toán học và lập trình."

### Phân cảnh 3.4: Tinh chỉnh và Tự sửa lỗi (Refinement & Self-Correction) (01:15:00 - 01:25:00)
*   **Hình ảnh (3B1B Style):**
    *   **Phần 1: Phản hồi ngoại sinh (Extrinsic Feedback Loop):**
        *   Hai khối hộp: `LLM Generator` (màu xanh dương) ở bên trái và `Rust Compiler` (màu đỏ gạch) ở bên phải.
        *   Mũi tên chạy từ LLM sang Compiler truyền đi `Bản nháp 1` chứa lỗi Borrow Checker (`let y = s; println!("{}", s);` làm di chuyển quyền sở hữu của `s`).
        *   Compiler chuyển màu đỏ sẫm báo lỗi `error[E0382]: borrow of moved value: 's'`. Hộp báo lỗi di chuyển theo mũi tên cong phản hồi ngược lại LLM.
        *   LLM sinh ra `Bản nháp 2` đã sửa lỗi (`let y = &amp;s;` sử dụng tham chiếu). Bản nháp này gửi lại sang Compiler.
        *   Compiler chuyển màu xanh lá rực rỡ và hiển thị dấu tích xanh lá cây (`get_checkmark`) báo hiệu biên dịch thành công.
    *   **Phần 2: Phản hồi nội sinh dạng Prompt & Cạm bẫy Nhiễu phản hồi (Noisy Feedback):**
        *   LLM Generator nhận câu hỏi đơn giản: `Prompt: Hãy giải 17 + 25 = ?`. Bản nháp ban đầu sinh ra kết quả đúng: `42`.
        *   Tiếp theo, LLM được yêu cầu tự phản biện: `Prompt tự đánh giá: Câu trả lời trên đã đúng chưa?`.
        *   Mô hình rơi vào cạm bẫy ảo giác phản hồi (Feedback Hallucination): `Chưa đúng, 17+25 phải bằng 32`. LLM xuất ra câu trả lời cuối cùng bị phá hỏng: `32`.
        *   Ở bên phải, vẽ Ma trận Tự sửa lỗi (Confusion Matrix) 2x2:
            *   Hàng 1 (Nháp Đúng): Đúng -> Đúng (85%), Đúng -> Sai (15% - Ảo giác phản hồi, khoanh viền đỏ dày).
            *   Hàng 2 (Nháp Sai): Sai -> Đúng (35%), Sai -> Sai (65%).
        *   Dưới đáy màn hình, xuất hiện dòng chữ cảnh báo nhấp nháy màu đỏ: `PHẢN HỒI NỘI SINH QUÁ NHIỄU (NOISY FEEDBACK)`.
    *   **Phần 3: Huấn luyện Bộ tự sửa lỗi (Trained Corrector) & Giải thuật SCoRe:**
        *   Hiển thị công thức mục tiêu học tinh chỉnh chính sách sửa lỗi: $p_\theta(\text{better\_correction} \mid \text{bad\_draft})$ trong khung viền xanh.
        *   Khối hộp bên trái (màu đỏ): `Behavior Collapse (Sụp đổ hành vi)` - mô hình bỏ qua feedback, chất lượng sửa đổi giảm sút và mất khả năng cũ dưới học tăng cường (RL) thông thường.
        *   Khối hộp bên phải (màu xanh lá): `Giải pháp SCoRe (Google DeepMind)` - huấn luyện trên vết sửa đổi nhiều bước và dùng KL Regularization để ổn định hóa chính sách RL.
    *   **Phần 4: Tổng kết Phân cảnh 3.4:**
        *   Bảng so sánh 3 cột (Phương pháp, Cơ chế phản hồi, Đặc trưng / Cạm bẫy) và 3 hàng tóm tắt toàn bộ ưu/nhược điểm của các cơ chế Tinh chỉnh.
*   **Lời thoại Voiceover (Dịch chi tiết từ phụ đề):**
    > "Chào mừng các bạn đến với chiến lược điều phối cấp cao cuối cùng của chương ba: Tinh chỉnh và Tự sửa lỗi – *Refinement & Self-Correction*. 
    > 
    > Ý tưởng cốt lõi ở đây rất trực quan: khi mô hình sinh ra một bản nháp đầu tiên chưa hoàn hảo, thay vì chấp nhận ngay kết quả đó, chúng ta yêu cầu mô hình chỉnh sửa và tự sửa lỗi bản nháp của chính mình.
    > 
    > Hiệu năng của quá trình tự sửa lỗi này phụ thuộc hoàn toàn vào chất lượng và nguồn gốc của tín hiệu phản hồi. Chúng ta phân chia thành hai loại phản hồi chính: Phản hồi ngoại sinh (Extrinsic Feedback) và Phản hồi nội sinh (Intrinsic Feedback).
    > 
    > Đầu tiên là Phản hồi ngoại sinh – *Extrinsic Feedback*. Đây là cơ chế mô hình tương tác trực tiếp với một môi trường hoặc công cụ kiểm chứng khách quan bên ngoài, ví dụ điển hình nhất là một Trình biên dịch Code – Compiler.
    > 
    > Hãy quan sát sơ đồ vòng lặp compiler này. Mô hình LLM Generator sinh ra bản nháp code Rust đầu tiên. Nhưng mô hình đã phạm một sai lầm rất phổ biến trong Rust: gán biến `y = s` làm di chuyển quyền sở hữu của chuỗi `s`, sau đó lại cố gắng in ra `s`.
    > 
    > Khi gửi đoạn code này sang Rust Compiler, trình biên dịch ngay lập tức phát hiện ra lỗi và trả lời bằng một thông báo lỗi Borrow Checker chi tiết. Thông tin lỗi khách quan này được nạp ngược lại vào prompt của LLM. Nhờ chỉ dẫn lỗi rõ ràng từ trình biên dịch, LLM nhanh chóng sửa đổi mã nguồn thành `let y = &amp;s;` để mượn tham chiếu. Khi gửi lại lần hai, Rust Compiler báo biên dịch thành công. Cơ chế này đạt độ tin cậy tuyệt đối và cải thiện rõ rệt chất lượng code.
    > 
    > Nhưng chuyện gì xảy ra nếu chúng ta không có một công cụ kiểm chứng bên ngoài? Đó là lúc chúng ta phải dựa vào Phản hồi nội sinh – *Intrinsic Feedback*, tức là bắt mô hình tự đánh giá và sửa lỗi dựa trên tri thức nội tại của nó.
    > 
    > Đây là một cạm bẫy cực lớn, thường được gọi là cạm bẫy Nhiễu phản hồi – *Noisy Feedback*. Hãy cùng xem một ví dụ thực tế. Khi hỏi bài toán cộng đơn giản '17 cộng 25 bằng bao nhiêu?', bản nháp đầu tiên của LLM đưa ra kết quả đúng là 42.
    > 
    > Tuy nhiên, khi chúng ta đưa thêm một bước tự đánh giá: 'Câu trả lời trên đã đúng chưa?', mô hình thường rơi vào hiện tượng Ảo giác phản hồi – *Feedback Hallucination*. Do không có công cụ đối chiếu khách quan, mô hình tự nghi ngờ bản thân và lập luận sai lệch rằng 17 cộng 25 phải bằng 32, rồi tự hủy hoại đáp án đúng ban đầu để chuyển sang đáp án sai.
    > 
    > Sự nhiễu loạn này được thể hiện rõ nét qua ma trận Confusion Matrix của quá trình tự sửa lỗi. Khi bản nháp ban đầu của mô hình đã đúng, xác suất mô hình giữ nguyên đáp án chỉ là 85%, đồng nghĩa với việc có tới 15% trường hợp mô hình tự sửa đúng thành sai do ảo giác phản hồi. Ngược lại, khi bản nháp ban đầu sai, mô hình chỉ sửa đúng được 35%, còn lại 65% vẫn tiếp tục sai. 
    > 
    > Vì vậy, phản hồi nội sinh dựa trên prompt thông thường như phương pháp Self-Refine là cực kỳ nhiễu và thường làm giảm hiệu năng tổng thể của các tác vụ lập luận logic.
    > 
    > Để giải quyết triệt để sự nhiễu loạn này, thay vì chỉ sử dụng prompt thông thường, chúng ta có thể Huấn luyện (Fine-tune) mô hình để trở thành một Bộ sửa lỗi chuyên nghiệp – *Trained Corrector*. Mục tiêu toán học là tối đa hóa xác suất có điều kiện của một câu trả lời tốt hơn khi biết bản nháp lỗi đi trước, ký hiệu là $p_\theta(\text{better} \mid \text{bad\_draft})$.
    > 
    > Nhưng việc huấn luyện RLHF hoặc học tăng cường (RL) thông thường cho tác vụ tự sửa lỗi này lại vấp phải hiện tượng Sụp đổ hành vi – *Behavior Collapse*. Mô hình học tăng cường rất nhanh chóng rơi vào trạng thái lờ đi tín hiệu phản hồi, hoặc chất lượng sửa lỗi bị sụt giảm nghiêm trọng, làm mất đi các năng lực lập luận cơ bản đã học.
    > 
    > Để khắc phục, Google DeepMind đã đề xuất giải thuật **SCoRe**. SCoRe giải quyết triệt để hiện tượng sụp đổ hành vi bằng hai cải tiến lớn: huấn luyện chính sách sửa đổi trên các vết dữ liệu nhiều bước thực tế, và sử dụng hàm phạt ràng buộc KL Regularization để giữ cho mô hình sửa đổi không đi quá xa so với chính sách cơ sở ban đầu, từ đó ổn định hóa quá trình huấn luyện RL và tạo ra năng lực tự sửa lỗi thực thụ.
    > 
    > Để tổng kết lại toàn bộ Chương 3.4, chúng ta có thể nhìn vào bảng so sánh ba cơ chế. Phản hồi ngoại sinh từ compiler có độ tin cậy tuyệt đối nhưng chỉ giới hạn trong lập trình và toán học. Phản hồi nội sinh dạng Prompt dễ triển khai nhưng cực kỳ nhiễu và dễ làm hỏng đáp án đúng. Và cuối cùng, Phản hồi nội sinh dạng huấn luyện bằng thuật toán SCoRe mang lại độ ổn định cao hơn nhờ các ràng buộc tối ưu, mở ra hướng đi đầy triển vọng cho các hệ thống Agent tự sửa lỗi thông minh trong tương lai."

---

## 🎬 CHƯƠNG 4: HIỆU NĂNG HỆ THỐNG (SYSTEMS EFFICIENCY)
*Thời lượng: ~30 phút (01:25:00 - 01:55:00 trong subtitle gốc | Người trình bày: Hailey Schoelkopf)*

### Phân cảnh 4.1: Điểm nghẽn phần cứng & Bản chất của KV Cache (01:25:00 - 01:35:00)
*   **Hình ảnh (3B1B Style):**
    *   **Sơ đồ Khối Phần cứng:** GPU Core (các nhân tính toán màu cam, xếp dạng lưới nhỏ, nhấp nháy phát sáng) đại diện cho sức mạnh tính toán (Compute capacity - FLOPS). VRAM Memory (khối lớn màu xanh dương chứa các ngăn nhớ) đại diện cho nơi lưu trữ mô hình và KV cache. Một cây cầu nối hẹp màu xám nhạt (Memory Bus) kết nối hai thực thể, biểu diễn băng thông bộ nhớ (Memory Bandwidth - GB/s).
    *   **Công thức Cường độ Số học (Arithmetic Intensity):**
        $$\text{Arithmetic Intensity} = \frac{\text{Tổng số phép tính (FLOPs)}}{\text{Tổng số byte đọc/ghi (Bytes)}}$$
    *   **Prefill Stage (Compute-bound):** 
        *   Một tập hợp nhiều token đầu vào (Prompt) được đẩy song song. Phép tính là nhân ma trận-ma trận (GEMM): $Q \times K^T$ và nhân với $V$.
        *   Hình ảnh các khối dữ liệu ma trận xếp chồng di chuyển dày đặc qua cây cầu, sau đó nạp vào GPU Core. Lõi GPU phát sáng cam đậm liên tục biểu thị hiệu suất sử dụng lõi tính toán đạt gần tối đa (100%).
        *   Hiển thị công thức cường độ số học cho Prefill: với chiều dài prompt $T$ và kích thước ẩn $d$, số phép tính là $O(T \cdot d^2)$ trong khi lượng bộ nhớ tải trọng số là $O(d^2)$. Cường độ số học tỷ lệ thuận với $T$ (rất cao).
        *   Hiển thị nhãn lớn: **"COMPUTE-BOUND (Nghẽn năng lực tính toán)"** màu xanh ngọc.
    *   **Decode Stage (Memory-bound):** 
        *   Chỉ sinh một token mới tại mỗi bước. Phép tính là nhân ma trận-vector (GEMV).
        *   GPU Core đứng im, nguội lạnh (màu cam mờ). Cây cầu hẹp hiển thị một khối trọng số khổng lồ (Model Weights - hàng chục GB) đang được kéo lê rất chậm chạp từ VRAM sang GPU, trong khi ở GPU chỉ xử lý một vector token nhỏ xíu.
        *   Hiển thị công thức cường độ số học cho Decode: cả số phép tính và lượng byte tải đều là $O(d^2)$, cường độ số học chỉ xấp xỉ 1 FLOP/byte, cực kỳ thấp so với ngưỡng phần cứng (thường cần >100 FLOP/byte để tận dụng hết GPU).
        *   Hiển thị nhãn lớn: **"MEMORY-BOUND (Nghẽn băng thông bộ nhớ)"** màu đỏ cảnh báo nhấp nháy.
    *   **Bản chất và cơ chế của KV Cache:**
        *   **Không dùng KV Cache:** Mô hình phải tính lại Attention cho tất cả các token từ đầu đến cuối tại mỗi bước sinh. Show hình các vector khóa và giá trị cũ liên tục bị tính toán lại một cách lãng phí, GPU Core nóng lên và VRAM bị tải lại liên tục.
        *   **Có dùng KV Cache:** Một bảng grid lưu trữ Key-Value của các token trước đó trong VRAM. Tại mỗi bước sinh, vector Key-Value của token mới vừa sinh được ghép (append) thêm vào grid này. Show hoạt ảnh vector mới trượt gọn gàng vào hàng cuối của KV Cache Grid, bỏ qua toàn bộ việc tính lại các token cũ.
*   **Lời thoại (Voiceover):**
    > "Chào mừng các bạn đến với Chương 4: Hiệu năng hệ thống (Systems Efficiency). Trong chương này, chúng ta sẽ bước từ thế giới lý thuyết thuật toán sang thực tế phần cứng để hiểu cách vận hành các hệ thống AI quy mô lớn một cách tiết kiệm và nhanh nhất.
    > 
    > Điểm mấu chốt đầu tiên ta cần làm quen là cấu trúc vật lý của một GPU. Một GPU thông thường gồm hai thành phần chính: Lõi tính toán GPU Core (nơi thực hiện hàng trăm nghìn phép nhân cộng mỗi giây) và Bộ nhớ VRAM (nơi lưu trữ hàng chục gigabyte trọng số của mô hình). Kết nối giữa chúng là một xa lộ bộ nhớ hay còn gọi là Memory Bandwidth. Điểm nghẽn lớn nhất trong suy luận AI thường không nằm ở tốc độ tính toán của lõi GPU, mà nằm ở tốc độ truyền tải dữ liệu qua xa lộ này.
    > 
    > Để lượng hóa điều này, các kỹ sư sử dụng khái niệm 'Cường độ Số học' (Arithmetic Intensity), được định nghĩa bằng tỷ số giữa số lượng phép tính FLOPs thực hiện chia cho số byte dữ liệu cần đọc hoặc ghi qua xa lộ bộ nhớ. Mỗi dòng GPU đều có một điểm cân bằng phần cứng. Nếu cường độ số học của thuật toán cao hơn điểm cân bằng này, thuật toán sẽ bị giới hạn bởi tốc độ tính toán của lõi (gọi là Compute-bound). Ngược lại, nếu cường độ số học thấp, lõi GPU sẽ phải nhàn rỗi chờ đợi dữ liệu nạp từ VRAM, thuật toán bị giới hạn bởi xa lộ băng thông (gọi là Memory-bound).
    > 
    > Hãy đối chiếu điều này với hai giai đoạn cốt lõi của suy luận LLM: giai đoạn Prefill và giai đoạn Decode.
    > 
    > Giai đoạn thứ nhất là Prefill, diễn ra khi chúng ta bắt đầu nạp toàn bộ prompt đầu vào. Ở đây, mô hình xử lý song song toàn bộ T token đầu vào cùng một lúc. Phép toán chủ đạo là nhân ma trận với ma trận. Do xử lý song song nhiều token, chúng ta chỉ cần tải trọng số mô hình từ VRAM lên GPU một lần duy nhất và tái sử dụng nó cho tất cả các token trong prompt. Nhờ vậy, số phép tính thực hiện rất lớn so với lượng dữ liệu bộ nhớ phải nạp. Cường độ số học ở giai đoạn này rất cao, đẩy GPU rơi vào trạng thái Compute-bound. Lõi tính toán được tận dụng tối đa năng lực phần cứng.
    > 
    > Tuy nhiên, mọi thứ thay đổi hoàn toàn khi ta bước sang giai đoạn Decode – tức là bước sinh từng token tuần tự tiếp theo. Trong Decode, tại mỗi bước ta chỉ xử lý đúng 1 token mới sinh ở bước trước. Phép toán chủ đạo biến thành nhân ma trận với vector. Hãy tưởng tượng: để thực hiện phép toán cho token đơn lẻ này, GPU vẫn buộc phải tải toàn bộ hàng chục Gigabyte trọng số của mô hình từ VRAM qua xa lộ bộ nhớ chỉ để nhân với một vector kích thước nhỏ. Cường độ số học lúc này giảm xuống cực kỳ thấp, chỉ xấp xỉ 1 FLOP trên mỗi byte dữ liệu tải. Kết quả là, lõi GPU Core vô cùng mạnh mẽ nhưng phải đứng im nhàn rỗi tới 95% thời gian để chờ đợi dữ liệu trọng số được kéo lê qua xa lộ bộ nhớ hẹp. Giai đoạn Decode là Memory-bound điển hình.
    > 
    > Để giảm thiểu điểm nghẽn bộ nhớ này, chúng ta cần tránh tối đa việc tính toán lặp lại. Ở thuật toán Attention nguyên bản, để sinh token thứ T, ta phải tính toán lại tích của tất cả T-1 token trước đó. Việc này đòi hỏi tải lại bộ nhớ và tính toán lặp vô cùng lãng phí.
    > 
    > Giải pháp tối ưu chính là Bộ nhớ đệm Key-Value – hay KV Cache. Thay vì tính lại tất cả từ đầu, chúng ta lưu trữ sẵn các vector Key và Value của các token cũ vào một vùng nhớ đệm trong VRAM. Ở mỗi bước Decode tiếp theo, mô hình chỉ tính toán vector Key và Value cho duy nhất một token mới sinh, sau đó ghép nối thêm vào bảng KV Cache có sẵn. Cơ chế này loại bỏ hoàn toàn các phép toán lặp trên các token cũ, chuyển đổi toàn bộ khối lượng tính toán phức tạp thành một phép cập nhật gia tăng đơn giản, giúp tăng tốc độ sinh từ của bước Decode lên gấp hàng chục lần."

### Phân cảnh 4.2: Giải mã đầu cơ (Speculative Decoding) (01:35:00 - 01:45:00)
*   **Bảng Kịch bản Chi tiết & Storyboard (3Blue1Brown Style):**


| Thời gian | Trực quan hình ảnh (3Blue1Brown Style) | Lời thoại Voiceover (Thuyết minh chi tiết) |
| :--- | :--- | :--- |
| **00:00 - 01:00** | **Mở đầu & Tiêu đề chính:**<br>- Màn hình tối màu xám đen `#111111`. Tiêu đề chương viết ra mượt mà: **"Chương 4: Hiệu năng hệ thống (Systems Efficiency)"**.<br>- Tiêu đề phụ: **"Phần 4.2: Giải mã đầu cơ (Speculative Decoding)"** (Màu cam ấm).<br>- Phóng to nhẹ và dọn màn hình, chuẩn bị ôn lại điểm nghẽn của giai đoạn Decode thông thường. | Chào mừng các bạn đã quay trở lại. Trong phần trước, chúng ta đã hiểu được điểm nghẽn chí mạng của giai đoạn Decode: đó là tình trạng nghẽn băng thông bộ nhớ - *Memory-bound*.<br><br>Để sinh ra từng token tiếp theo, GPU Core cực kỳ mạnh mẽ buộc phải đứng im nhàn rỗi tới chín mươi lăm phần trăm thời gian, chỉ để chờ đợi hàng chục Gigabyte trọng số của mô hình lớn được kéo lê qua xa lộ băng thông hẹp từ VRAM.<br><br>Vậy câu hỏi đặt ra là: Có cách nào để chúng ta phá vỡ giới hạn vật lý này, sinh ra nhiều token hơn mà không phải liên tục tải toàn bộ trọng số của mô hình lớn cho mỗi token đơn lẻ hay không? Câu trả lời chính là kỹ thuật Giải mã đầu cơ – *Speculative Decoding*. |
| **01:00 - 02:30** | **Sự kết hợp giữa Draft Model & Target Model:**<br>- Vẽ hộp màu cam bên trái: **Draft Model (Mô hình nháp - Nhỏ)**, ví dụ mô hình 1 tỷ tham số ($1B$).<br>- Vẽ hộp màu xanh dương bên phải: **Target Model (Mô hình đích - Lớn)**, ví dụ mô hình 70 tỷ tham số ($70B$).<br>- Animate so sánh kích thước: Hộp màu xanh dương khổng lồ, hộp màu cam rất nhỏ gọn.<br>- Hiển thị băng thông nạp bộ nhớ: vẽ xa lộ truyền tải từ VRAM vào GPU cho 2 mô hình. Draft Model đi qua cực nhanh (băng thông thông thoáng), Target Model đi qua rất chậm chạp. | Ý tưởng cốt lõi của giải mã đầu cơ là sự kết hợp nhịp nhàng giữa hai bộ não có kích thước hoàn toàn chênh lệch: một mô hình nháp nhỏ – *Draft Model* – và một mô hình đích lớn – *Target Model*.<br><br>Mô hình nháp nhỏ, ví dụ chỉ có một tỷ tham số, có kích thước bộ nhớ rất bé. Việc tải trọng số của nó từ VRAM vào lõi GPU diễn ra cực kỳ nhanh chóng. Nhờ đó, nó có thể sinh ra các token với tốc độ rất cao.<br><br>Trong khi đó, mô hình đích lớn, ví dụ lên tới bảy mươi tỷ tham số, tuy vô cùng thông minh nhưng tốc độ tải trọng số cực kỳ chậm do dung lượng lớn.<br><br>Thay vì bắt mô hình lớn sinh từng chữ một cách chậm chạp, chúng ta sẽ cho mô hình nhỏ chạy trước để "đoán mò" và sinh ra một chuỗi token nháp. Sau đó, mô hình lớn chỉ việc kiểm tra và phê duyệt song song toàn bộ chuỗi nháp đó trong một lượt chạy duy nhất. |
| **02:30 - 04:00** | **Băng chuyền Draft Generation (K=5):**<br>- Vẽ một đường băng chuyền (conveyor belt) chạy từ trái sang phải.<br>- Draft Model (Màu cam) liên tục nhả ra $5$ ô token đặt trên băng chuyền: `["Hôm", "nay", "trời", "rất", "nắng"]`. Mỗi ô cách nhau đều đặn, màu cam nổi bật.<br>- Hiệu ứng các token xuất hiện cực kỳ nhanh và mượt mà trên băng chuyền. | Hãy cùng trực quan hóa quá trình này. Đầu tiên, chúng ta cấu hình một tham số chùm nháp, ký hiệu là K bằng năm. Nghĩa là, chúng ta yêu cầu mô hình nháp sinh nhanh năm token tiếp theo liên tiếp.<br><br>Hãy quan sát băng chuyền chuyển động nhanh này. Mô hình nháp liên tục nhả ra năm token ứng viên: *"Hôm"*, *"nay"*, *"trời"*, *"rất"*, *"nắng"*. Vì mô hình nháp rất nhỏ, năm token này được sinh ra trong một cái nháy mắt.<br><br>Tuy nhiên, vì mô hình nhỏ kém thông minh hơn, chúng ta không thể tin tưởng hoàn toàn vào kết quả của nó. Một hoặc vài token trong chuỗi này có thể sai lệch hoặc không tối ưu so với mô hình lớn. Do đó, chúng ta cần chuyển toàn bộ băng chuyền ứng viên này sang mô hình đích lớn để kiểm tra tính đúng đắn. |
| **04:00 - 05:30** | **Kiểm tra song song (Target Verification):**<br>- Cả 5 token màu cam đi vào hộp **Target Model (Màu xanh dương)** cùng một lúc.<br>- Show hoạt ảnh prefill song song: Target Model chỉ cần nạp model weights $70B$ từ VRAM đúng một lần duy nhất, sau đó tính toán attention và xác suất cho cả 5 vị trí song song.<br>- Cường độ số học vọt lên cao, GPU Core sáng rực rỡ thể hiện trạng thái Compute-bound hiệu quả. | Đây chính là điểm kỳ diệu nhất của giải mã đầu cơ. Mô hình lớn nhận cả năm token ứng viên này cùng một lúc và chạy một bước kiểm tra song song duy nhất.<br><br>Thay vì chạy tự hồi quy năm bước tuần tự chậm chạp, mô hình lớn thực hiện một bước xử lý song song giống như giai đoạn Prefill. Chúng ta chỉ cần nạp trọng số mô hình lớn từ VRAM lên GPU một lần duy nhất, nhưng lại tính toán và kiểm tra được phân phối xác suất cho cả năm vị trí cùng lúc.<br><br>Cơ chế này đẩy cường độ số học của mô hình lớn lên cao, giúp lõi tính toán GPU Core hoạt động hết công suất và giải phóng hệ thống khỏi điểm nghẽn băng thông bộ nhớ. |
| **05:30 - 07:00** | **Thuật toán Chấp nhận / Từ chối (Rejection Sampling):**<br>- Trên màn hình xuất hiện công thức Speculative Sampling:<br>$$\text{Xác suất chấp nhận } x = \min\left(1, \frac{P_{target}(x)}{P_{draft}(x)}\right)$$<br>- Minh họa bằng biểu đồ cột xác suất tại vị trí thứ 4:<br>  - Draft Model dự đoán chữ `"rất"` với xác suất $P_{draft}(\text{"rất"}) = 0.8$.<br>  - Target Model dự đoán chữ `"rất"` chỉ có xác suất $P_{target}(\text{"rất"}) = 0.2$, nhưng lại ưu tiên chữ `"mưa"` với xác suất $P_{target}(\text{"mưa"}) = 0.7$.<br>- Hệ thống quyết định từ chối (reject) chữ `"rất"`. | Làm thế nào để mô hình lớn quyết định chấp nhận hay từ chối một token nháp để đảm bảo chất lượng văn bản đầu ra không bị suy giảm?<br><br>Chúng ta sử dụng một thuật toán gọi là Lấy mẫu đầu cơ – *Speculative Sampling*, dựa trên nguyên lý của Rejection Sampling trong xác suất thống kê. Công thức toán học các bạn đang thấy trên màn hình đảm bảo rằng phân phối xác suất của văn bản đầu ra cuối cùng sẽ giống hệt như thể nó được sinh ra hoàn toàn bởi mô hình lớn.<br><br>Hãy xem xét vị trí thứ tư trên băng chuyền. Mô hình nháp tự tin đưa ra từ *"rất"* với xác suất tám mươi phần trăm. Tuy nhiên, mô hình lớn sau khi kiểm tra nhận thấy từ *"rất"* chỉ có xác suất hai mươi phần trăm trong ngữ cảnh này, trong khi nó muốn chọn từ *"mưa"* với xác suất bảy mươi phần trăm.<br><br>Áp dụng công thức tỷ lệ xác suất, hệ thống quyết định từ chối từ *"rất"* của mô hình nháp để bảo toàn tính logic và độ chính xác của câu văn. |
| **07:00 - 08:30** | **Hiệu ứng Laser Cut & Sửa đổi:**<br>- Băng chuyền 5 token hiện lại.<br>- Vị trí 1 (`"Hôm"`), 2 (`"nay"`), 3 (`"trời"`) chuyển sang màu xanh lá cây rực rỡ (chấp nhận).<br>- Vị trí 4 (`"rất"`) và 5 (`"nắng"`) chuyển sang màu đỏ.<br>- Một đường laser màu đỏ tươi quét từ trên xuống cắt đứt băng chuyền ngay trước vị trí thứ 4.<br>- Các token đỏ bị vỡ vụn và biến mất.<br>- Target Model chèn chữ `"mưa"` (Màu xanh dương phát sáng) vào vị trí thứ 4.<br>- Kết quả: sinh được 4 token chất lượng cao (`"Hôm nay trời mưa"`) trong chỉ một lượt chạy duy nhất của mô hình lớn. | Khi một token nháp bị từ chối, tất cả các token nháp tiếp theo ở phía sau nó trên băng chuyền cũng lập tức mất đi giá trị và bị loại bỏ.<br><br>Hãy quan sát hiệu ứng cắt laser này. Ba token đầu tiên *"Hôm"*, *"nay"*, *"trời"* được chấp nhận và đổi sang màu xanh lá. Đường laser màu đỏ cắt đứt băng chuyền ngay tại vị trí thứ tư. Hai token *"rất"* và *"nắng"* bị loại bỏ hoàn toàn.<br><br>Tại vị trí bị cắt đứt này, mô hình lớn không chỉ từ chối mà còn trực tiếp bù đắp bằng cách sinh ra token sửa đổi tối ưu nhất của nó, đó chính là từ *"mưa"*. <br><br>Kết quả là, chỉ trong một lượt chạy duy nhất của mô hình lớn, hệ thống đã sinh ra thành công chuỗi gồm bốn token chính xác: *"Hôm nay trời mưa"*. Chúng ta có được tốc độ sinh cực nhanh mà chất lượng văn bản vẫn được bảo đảm tuyệt đối của mô hình bảy mươi tỷ tham số. |
| **08:30 - 09:30** | **Tốc độ thực tế & Đánh đổi:**<br>- Tạo bảng so sánh hiệu năng của Speculative Decoding vs. Standard Decoding.<br>- Show timeline: Speculative Decoding đạt tốc độ nhanh gấp **2x đến 3x lần** so với giải mã thông thường.<br>- Nhắc nhở hạn chế: nếu Draft Model quá tệ hoặc lệch pha với Target Model, tỷ lệ chấp nhận thấp, tia laser sẽ cắt sớm (ví dụ cắt ngay vị trí 1), khiến hệ thống tốn thêm chi phí chạy mô hình nhỏ vô ích. | Trong thực tế vận hành hệ thống, giải mã đầu cơ mang lại hiệu quả tăng tốc đáng kinh ngạc, thường từ hai đến ba lần tốc độ sinh chữ thông thường mà không cần thay đổi phần cứng hay làm giảm chất lượng mô hình.<br><br>Tuy nhiên, hiệu năng này phụ thuộc rất lớn vào sự ăn ý giữa hai mô hình. Nếu mô hình nháp quá kém chất lượng hoặc dự đoán sai lệch nhiều so với mô hình lớn, tỷ lệ chấp nhận sẽ cực kỳ thấp. Khi đó, tia laser sẽ liên tục cắt bỏ chuỗi nháp từ sớm, khiến hệ thống tốn thêm tài nguyên chạy mô hình nháp một cách vô ích.<br><br>Tóm lại, giải mã đầu cơ là một giải pháp thiết kế thuật toán đỉnh cao giúp chúng ta lách qua điểm nghẽn băng thông phần cứng để mở rộng năng lực tính toán khi suy luận.<br><br>Trong phần tiếp theo, chúng ta sẽ tìm hiểu thêm các tối ưu hóa khác liên quan đến chia sẻ tiền tố của bộ nhớ đệm KV Cache. Cảm ơn các bạn đã theo dõi. |

### Phân cảnh 4.3: Tối ưu hóa tiền tố dùng chung (Shared Prefix Optimizations) (01:45:00 - 01:55:00)
*   **Trực quan hình ảnh (3B1B Style):**
    *   **Bước 1: Trực quan hóa sự lãng phí bộ nhớ đệm KV Cache:**
        *   Màn hình tối `#111111`. Tiêu đề **"Phần 4.3: Tối ưu hóa tiền tố dùng chung (Shared Prefix Optimizations)"** viết ra mượt mà và thu nhỏ lên góc trên.
        *   Vẽ 3 khối hộp Prompt đại diện cho 3 luồng yêu cầu song song (Best-of-N). Mỗi khối hộp chứa phần tiền tố chung dài: `[System Prompt (1000 tokens)]` (Tô màu xám nhạt).
        *   Mô phỏng bộ nhớ VRAM của GPU dưới dạng các ô nhớ lớn. Khi các luồng chạy, 3 bản sao KV Cache của phần `System Prompt` được ghi vào 3 vị trí khác nhau trong VRAM.
        *   Xuất hiện nhãn đỏ nhấp nháy cảnh báo: `"Wasted VRAM (Lãng phí bộ nhớ VRAM)"` kèm biểu tượng cảnh báo.
    *   **Bước 2: Cơ chế PagedAttention (vLLM):**
        *   Vẽ bảng ánh xạ bộ nhớ đệm (Mapping Table) ở trung tâm. Bên trái là các khối KV Cache logic (Logical Blocks) của các luồng yêu cầu khác nhau. Phía bên phải là một trang bộ nhớ vật lý duy nhất (Physical Page) trong VRAM.
        *   Hoạt họa các mũi tên ánh xạ nhấp nháy trỏ từ các Logical Blocks về cùng một Physical Page chứa phần tiền tố dùng chung.
        *   Nhãn phát sáng xanh lá hiện lên: `"Shared Physical Block (Dùng chung bộ nhớ vật lý)"` và `"Batch Size tăng lên"`.
    *   **Bước 3: RadixAttention (SGLang) & Cây Radix Tree:**
        *   Vẽ một cấu trúc Cây Radix (Radix Tree) đa cấp:
            *   Nút gốc (Root): `[System Prompt (1000 tokens)]` (Màu xanh dương nhạt).
            *   Các nút con cấp 1: `[Few-shot Examples (500 tokens)]` (Màu xanh lá cây nhạt).
            *   Các nút con cấp 2: Các câu hỏi khác nhau `[Question A]`, `[Question B]` (Màu vàng nhạt).
            *   Các nút lá (Leaves): `[Answer A1]`, `[Answer A2]`, `[Answer B1]`.
        *   Khi luồng yêu cầu mới được gửi đến, một hạt sáng chạy dọc theo các nút từ Root xuống các nút con để kiểm tra sự tồn tại của tiền tố dùng chung.
        *   Hoạt họa cơ chế dọn dẹp bộ nhớ đệm LRU (Least Recently Used): Khi bộ nhớ GPU đầy, nút lá ít được truy cập nhất (ví dụ `[Answer B1]`) chuyển sang màu đỏ và biến mất (eviction), giải phóng bộ nhớ cho yêu cầu mới, trong khi các nút tiền tố ở gốc vẫn được lưu giữ an toàn.
    *   **Bước 4: Cơ chế tăng tốc Hydragen:**
        *   So sánh 2 công thức tính toán Attention trên màn hình:
            *   **Truyền thống (Matrix-Vector - Nghẽn bộ nhớ):**
                $$q_i K^T \quad \text{cho các luồng } i$$
                Mô tả các luồng phải tải đi tải lại KV Cache của tiền tố $K$ từ VRAM vào các bộ xử lý nhiều lần một cách chậm chạp.
            *   **Hydragen (Matrix-Matrix - Tối ưu phần cứng):**
                $$Q K^T$$
                Gộp tất cả các vector truy vấn $q_i$ thành ma trận $Q$ và nhân với ma trận $K^T$ của tiền tố dùng chung. KV Cache của tiền tố chỉ được tải vào các thanh ghi của bộ xử lý GPU đúng một lần duy nhất.
            *   Mũi tên chỉ vào công thức và hiện chữ: `"Leverage Tensor Cores (Tận dụng Tensor Cores)"`.
        *   Vẽ đồ thị so sánh hiệu năng (Thông lượng - Throughput vs. Batch Size):
            *   Đường màu đỏ: vLLM (tốc độ trung bình).
            *   Đường màu xanh lá: Hydragen (tốc độ cao vọt khi batch size lớn).
            *   Đường đứt nét màu xanh dương: Giới hạn trên lý thuyết (Upper Bound - không tốn chi phí attention).
    *   **Bước 5: Kỹ thuật loại bỏ Token (Token Dropping - Slide 192-193):**
        *   Hiển thị công thức tính kích thước KV Cache lên màn hình:
            $$Size = (batch * n_{ctx}) * (2 * n_{layer} * n_{heads} * head_{dim}) * n_{bytes}$$
        *   Minh họa chuỗi token của một request dưới dạng hàng ngang các ô nhớ liên tục. Mỗi ô hiển thị điểm số Attention động nhấp nháy.
        *   Các ô có điểm Attention thấp sẽ đổi sang màu đỏ mờ dần và bị đẩy ra khỏi cache (evict), tượng trưng cho việc loại bỏ các token ít quan trọng để tiết kiệm không gian.
        *   Tham số ngữ cảnh $n_{ctx}$ trong công thức co nhỏ lại trực quan.
        *   Hiện hộp nhãn cảnh báo màu cam: `"Hạn chế: Hành vi mô hình dễ bị mất ngữ cảnh (brittle) nếu loại bỏ nhầm token quan trọng hoặc đổi chủ đề."`
    *   **Bước 6: Kỹ thuật Lượng tử hóa (Quantization - Slide 194):**
        *   Giữ nguyên công thức kích thước KV Cache, khoanh tròn màu vàng tham số $n_{bytes}$.
        *   Minh họa các ô nhớ ban đầu ghi chữ `"FP16 (2 Bytes)"` co nhỏ kích thước vật lý lại thành các ô ghi chữ `"INT8 (1 Byte)"` rồi `"INT4 (0.5 Bytes)"`.
        *   Tham số $n_{bytes}$ trong công thức giảm xuống trực quan, tổng dung lượng bộ nhớ giảm rõ rệt.
        *   Hiện nhãn xanh lá: `"Tăng Batch Size, tăng thông lượng (Throughput)"`.
    *   **Bước 7: Thay đổi kiến trúc mô hình (Architectural Modification - MQA/GQA - Slide 195):**
        *   Vẽ so sánh trực quan 3 cơ chế Attention:
            *   **MHA (Multi-Head Attention):** Vẽ 8 đầu Query (Q) màu xanh dương trỏ vào 8 đầu Key/Value (K/V) màu xanh lá riêng biệt (tỷ lệ 1:1).
            *   **MQA (Multi-Query Attention):** Vẽ 8 đầu Query (Q) đều trỏ chung vào duy nhất 1 đầu Key/Value (K/V) dùng chung (tỷ lệ 8:1).
            *   **GQA (Grouped-Query Attention):** Gom 8 đầu Query thành 4 cặp (mỗi cặp 2 đầu Q), mỗi cặp trỏ vào 1 đầu Key/Value (K/V) tương ứng (tỷ lệ 8:4).
        *   Khoanh tròn tham số $n_{heads}$ trong công thức KV Cache, chỉ ra rằng việc giảm số đầu Key/Value giúp giảm trực tiếp $n_{heads}$ và thu nhỏ đáng kể kích thước cache trong mô hình lớn mà không làm giảm nhiều chất lượng.
    *   **Bước 8: Tổng kết & Đánh giá hiệu năng Meta-generator (Slide 196-200):**
        *   Tạo bảng so sánh hiệu năng của các Meta-generator:
            | Thuật toán | Song song hóa (Parallelizable) | Chia sẻ tiền tố (Prefix-shareable) |
            | :--- | :---: | :---: |
            | **Chained (Chuỗi)** | ❌ (Tuần tự) | ❌ |
            | **Parallel (Song song)** |  (Tối đa) |  (Tốt) |
            | **Tree Search (Cây)** | ⚠️ (Bán song song) |  (Rất cao) |
            | **Refinement (Cải thiện)** | ❌ (Tuần tự) | ❌ |
        *   Xuất hiện dòng chữ kết luận phát sáng: `"Ngân sách token (Token budget) chỉ là sự đơn giản hóa! Cấu trúc câu nhắc (prompt) và cơ chế hệ thống quyết định hiệu năng thực tế."`
    *   **Bước 9: Hướng đi tương lai (Looking Ahead - Slide 201-205):**
        *   Hiển thị danh sách các hướng nghiên cứu đột phá:
            1. **Meta-generators lai (Hybrid Systems):** Phối hợp song song và cải thiện tuần tự (ví dụ bài báo AlphaVerus).
            2. **Học cách tự tìm kiếm (Learning to search):** Mô hình tự khám phá, quay lui (backtrack) và tự sửa lỗi khi suy luận.
            3. **Tối ưu hóa môi trường Agent:** Tương tác động và thu nhận phản hồi.
            4. **Phân bổ tính toán tối ưu (Compute Allocation):** Quyết định chi phí tính toán linh hoạt cho từng câu hỏi khó/dễ.
        *   Hiển thị bìa bài báo tổng quan trên tạp chí **TMLR 2024** và đường link URL trang web của tutorial để kết thúc chương 4.
*   **Lời thoại Voiceover (Dịch chi tiết và thuyết minh đầy đủ):**
    > "Chào mừng các bạn đến với phần cuối cùng của chương bốn: Tối ưu hóa tiền tố dùng chung – Shared Prefix Optimizations. Khi triển khai các thuật toán Meta-Generation thực tế như Best-of-N, Tree Search hay các hệ thống chatbot với prompt hệ thống dài, chúng ta sẽ bắt gặp một hiện tượng rất phổ biến: đó là sự trùng lặp và dư thừa dữ liệu tiền tố dùng chung trong các prompt. 
    > 
    > Vì các mô hình ngôn ngữ lớn hoạt động theo cơ chế tự hồi quy, các vector khóa và giá trị – tức là KV Cache – của các token đi trước hoàn toàn độc lập, không bị ảnh hưởng bởi bất kỳ token nào sinh ra sau chúng. Do đó, nếu chúng ta chạy nhiều luồng suy luận song song chia sẻ chung một tiền tố mà lại phải lưu trữ riêng biệt từng bản sao KV Cache cho từng luồng, bộ nhớ VRAM của GPU sẽ nhanh chóng bị quá tải và cạn kiệt. Để giải quyết bài toán này, các nhà nghiên cứu đã đề xuất ba giải pháp tối ưu hóa đột phá.
    > 
    > Giải pháp thứ nhất là PagedAttention, được giới thiệu trong thư viện vLLM. Thay vì phân bổ một vùng nhớ liên tục khổng lồ cho mỗi yêu cầu, PagedAttention chia nhỏ KV Cache thành các trang vật lý động trong VRAM, tương tự như cơ chế quản lý bộ nhớ ảo trong hệ điều hành máy tính. Điều này cho phép nhiều yêu cầu logic khác nhau cùng trỏ vào và chia sẻ chung một khối bộ nhớ vật lý chứa tiền tố hệ thống, giúp loại bỏ hoàn toàn sự dư thừa và giảm thiểu tối đa hiện tượng phân mảnh bộ nhớ.
    > 
    > Tuy nhiên, việc chia sẻ KV Cache không chỉ giới hạn ở một tầng tiền tố duy nhất. Trong thực tế, chúng ta thường gặp các cấu trúc chia sẻ phức tạp hơn nhiều. Ví dụ, một prompt hệ thống dài kết hợp với các ví dụ vài mẫu, rồi từ đó sinh ra nhiều nhánh câu hỏi khác nhau, và mỗi câu hỏi lại chạy song song Best-of-N. Đây là cấu trúc chia sẻ nhiều tầng.
    > 
    > Để tối ưu hóa cấu trúc này, giải pháp thứ hai ra đời: đó là RadixAttention trong thư viện SGLang. RadixAttention tổ chức toàn bộ bộ nhớ đệm KV Cache dưới dạng một cây tiền tố Radix Tree. Radix Tree sẽ theo dõi và ánh xạ các mối quan hệ phụ thuộc giữa các cụm token. Khi có một yêu cầu mới, hệ thống sẽ duyệt cây để tìm xem phần tiền tố nào đã có sẵn trong KV Cache và tái sử dụng ngay lập tức mà không cần tính toán lại. Khi bộ nhớ GPU đầy, RadixAttention sẽ tự động giải phóng bộ nhớ bằng cách thu hồi các khối KV Cache ít được sử dụng nhất theo thuật toán LRU – Least Recently Used.
    > 
    > Đi xa hơn nữa về mặt hiệu năng phần cứng, chúng ta có giải pháp thứ ba mang tên Hydragen. Các kỹ sư của Hydragen nhận thấy rằng, mặc dù các phương pháp trước đã lưu trữ tiền tố dùng chung đúng một lần trong VRAM, nhưng khi tính toán Attention cho các nhánh song song, GPU vẫn phải tải đi tải lại phần tiền tố này từ VRAM vào các bộ xử lý nhiều lần cho mỗi nhánh dưới dạng các phép nhân ma trận-vector độc lập.
    > 
    > Hydragen đã thay đổi hoàn toàn cuộc chơi bằng cách chỉ tải KV Cache của phần tiền tố dùng chung vào các thanh ghi của bộ xử lý GPU đúng một lần duy nhất. Sau đó, nó gộp tất cả các vector Query của các nhánh song song lại để thực hiện phép toán Attention trên phần tiền tố chung dưới dạng một phép nhân ma trận-ma trận duy nhất. Vì các GPU hiện đại như Tensor Cores được tối ưu hóa cực kỳ mạnh mẽ cho phép nhân ma trận-ma trận, Hydragen giúp tăng cường độ số học, tối ưu hóa phần cứng và mang lại thông lượng xử lý khổng lồ, đặc biệt là khi kích thước batch size lớn. Nhờ đó, chi phí tính toán Attention trên các tiền tố dùng chung gần như trở nên bằng không, giúp mở rộng quy mô của các hệ thống AI một cách đáng kinh ngạc.
    > 
    > Bây giờ, chúng ta hãy cùng đào sâu hơn về ý tưởng cắt giảm dung lượng bộ nhớ đệm KV Cache trong các trường hợp tổng quát, kể cả khi hệ thống không có cấu trúc tiền tố dùng chung nào. Làm thế nào để nén kích thước KV Cache một cách hiệu quả?
    > 
    > Nếu nhìn vào công thức tính toán dung lượng KV Cache trên màn hình: dung lượng này tỉ lệ thuận với kích thước batch, chiều dài ngữ cảnh n_ctx, số lượng lớp n_layer, số lượng đầu Attention n_heads, kích thước mỗi đầu head_dim, và số bytes đại diện cho kiểu dữ liệu n_bytes. Để tối ưu hóa, chúng ta có ba hướng tiếp cận cốt lõi.
    > 
    > Giải pháp đầu tiên là loại bỏ token – Token Dropping. Kỹ thuật này tác động trực tiếp vào tham số n_ctx. Dựa trên các thống kê trọng số Attention của các token trước đó, thuật toán sẽ dự đoán xem những token nào không còn quan trọng đối với các token sinh ra trong tương lai và tự động trục xuất chúng khỏi bộ nhớ đệm. Điểm hạn chế của phương pháp này là nếu ta loại bỏ nhầm token quan trọng hoặc khi nội dung trò chuyện thay đổi đột ngột, mô hình có thể bị mất ngữ cảnh, khiến quá trình sinh chữ trở nên kém ổn định.
    > 
    > Giải pháp thứ hai là lượng tử hóa bộ nhớ đệm – Quantization, tác động trực tiếp vào tham số n_bytes. Thay vì lưu trữ KV Cache dưới dạng số thực FP16 tốn 2 bytes cho mỗi phần tử, hệ thống sẽ lượng tử hóa chúng về các kiểu dữ liệu có độ rộng bit thấp hơn như INT8 hoặc thậm chí là INT4. Điều này giúp kích thước vật lý của mỗi vector co nhỏ lại rõ rệt, cho phép chúng ta tăng kích thước batch để khai thác tối đa năng lực xử lý của GPU.
    > 
    > Giải pháp thứ ba là tối ưu hóa từ cấu trúc mô hình – Architectural Modification. Điều này được thực hiện thông qua các cơ chế Attention cải tiến như Multi-Query Attention hoặc Grouped-Query Attention. Thay vì cơ chế Attention đa đầu truyền thống nơi mỗi đầu Query đi kèm một đầu Key và Value riêng biệt, Multi-Query Attention cho phép tất cả các đầu Query dùng chung một đầu Key/Value duy nhất. Còn Grouped-Query Attention chia các đầu Query thành các nhóm, mỗi nhóm dùng chung một đầu Key/Value. Sự thay đổi này giúp giảm mạnh số lượng đầu Key/Value cần lưu trữ, thu nhỏ tham số n_heads trong công thức KV Cache và tiết kiệm bộ nhớ cực kỳ đáng kể khi xử lý các chuỗi văn bản dài.
    > 
    > Để tổng kết lại toàn bộ chương này, chúng ta hãy cùng nhìn nhận xem những Meta-generator nào là tối ưu nhất cho hệ thống của mình. Những thuật toán hoạt động hiệu quả nhất luôn sở hữu hai đặc tính cốt lõi: khả năng chạy song song – Parallelizable giúp giảm đáng kể độ trễ và nâng cao thông lượng, và khả năng chia sẻ tiền tố – Prefix-shareable giúp tái sử dụng KV Cache của các khối văn bản tĩnh dùng chung.
    > 
    > Như vậy, việc chỉ đánh giá thuật toán dựa trên ngân sách token thô là một sự đơn giản hóa quá mức. Trong thực tế, cấu trúc của câu nhắc (prompt) và các kỹ thuật hệ thống bên dưới mới là những yếu tố quyết định hiệu năng thực tế. Hiểu rõ sự kết hợp giữa thuật toán và hệ thống phần cứng chính là chìa khóa để triển khai AI hiệu quả.
    > 
    > Hướng về tương lai, lĩnh vực nghiên cứu Meta-Generation đang đứng trước những cơ hội đột phá. Chúng ta sẽ chứng kiến sự kết hợp giữa các nguyên mẫu tìm kiếm và cải thiện để tạo ra các hệ thống lai tối ưu như AlphaVerus. Đồng thời, xu hướng dạy mô hình tự học cách tìm kiếm, tự sửa sai khi suy luận, việc thiết kế các môi trường hoạt động cho các Agent, và bài toán phân bổ tài nguyên suy luận Compute tối ưu cho từng tác vụ đều là những mặt trận nghiên cứu đầy hứa hẹn. Toàn bộ nội dung của tutorial này được đúc kết từ bài báo tổng quan của chúng tôi công bố trên tạp chí TMLR 2024. Cảm ơn sự quan tâm theo dõi của các bạn."

---

## 🎬 KẾT LUẬN & PHIÊN THẢO LUẬN PANEL (01:55:00 - 02:00:00)
*(Slide 206 - Kết thúc | Điều phối viên: Ilia Kulikov)*

### Phân cảnh 5.1: Tóm tắt nội dung & Diễn đàn thảo luận (Panel Session)
*   **Hình ảnh (3B1B Style):**
    *   Hệ trục tọa độ 3D ở Chương 1 xuất hiện lại.
    *   Các thành phần của video (Cây tìm kiếm, Máy trạng thái ràng buộc, Băng chuyền đầu cơ, Cây tiền tố KV Cache) bay về lắp ghép hoàn chỉnh xung quanh trục Z.
    *   Các khuôn mặt đại diện cho các chuyên gia từ OpenAI (Noam Brown), DeepMind (Rishabh Agarwal), Oxford (Jakob Foerster), CMU (Beidi Chen), AI2 (Nouha Dziri) xuất hiện trên màn hình chia nhỏ.
*   **Lời thoại Voiceover (Chuyển thể chi tiết từ đối thoại Panel):**
    > "Để kết luận, chúng ta đã đi qua một hành trình toàn diện: từ các bộ sinh cơ bản ở cấp độ token, đến các thuật toán Meta-Generation điều phối tìm kiếm và tự sửa sai, và cuối cùng là các tối ưu phần cứng hệ thống để vận hành chúng hiệu quả. Sau đây, chúng ta sẽ cùng tổng hợp các nhận định đắt giá từ phiên thảo luận nhóm (panel session) của các nhà nghiên cứu hàng đầu về tương lai của xu hướng này.
    > 
    > Một câu hỏi lớn được đặt ra: 'Liệu việc huấn luyện các mô hình lớn hơn trong tương lai có loại bỏ hoàn toàn nhu cầu về các giải thuật tìm kiếm Meta-Generation hay không?'
    > 
    > Tiến sĩ Nouha Dziri từ AI2 nhận định: Không. Các mô hình ngôn ngữ dù lớn đến đâu vẫn sẽ phải đối mặt với hai giới hạn cốt lõi: sự cộng dồn lỗi (snowballing of error - một lỗi nhỏ ban đầu sẽ làm lệch lạc toàn bộ suy luận phía sau) và sự khó khăn khi nhìn trước nhiều bước (look-ahead task). Do đó, các thuật toán Meta-Generation như tìm kiếm cây, quay lui và đánh giá tiến trình PRM sẽ luôn là lớp cấu trúc bổ sung thiết yếu để mở rộng khả năng của mô hình.
    > 
    > Nhà nghiên cứu Noam Brown từ OpenAI – người đứng sau dòng mô hình o1 – bổ sung thêm một góc nhìn kinh tế: 'Inference Compute là một ranh giới vô hạn.' Hiện nay chúng ta chỉ tốn một phần nhỏ của một xu cho mỗi câu hỏi thông thường. Nhưng đối với những bài toán quan trọng nhất của nhân loại như chứng minh giả thuyết Riemann hay phát hiện thuốc mới, người ta sẵn sàng trả hàng ngàn, thậm chí một triệu đô la cho một câu trả lời chính xác. Khoảng cách 8 cấp độ quy mô này chính là không gian khổng lồ để chúng ta tiếp tục mở rộng quy mô suy luận.
    > 
    > Về mặt hệ thống phần cứng, Tiến sĩ Beidi Chen từ CMU nhấn mạnh: Phần lớn phần cứng GPU hiện nay được thiết kế cho việc huấn luyện nặng và suy luận giá rẻ. Trong tương lai, khi chi phí suy luận chiếm phần lớn tổng chi phí vận hành AI, việc đồng thiết kế (co-design) giữa kiến trúc thuật toán tìm kiếm và phần cứng GPU sẽ mở ra những cơ hội tối ưu hóa khổng lồ để giảm giá thành suy luận xuống hàng chậm lần.
    > 
    > Tương lai của AI không chỉ nằm ở việc xây dựng các mô hình lớn hơn, mà nằm ở việc thiết kế các hệ thống thông minh biết cách suy nghĩ và phân bổ tài nguyên suy luận một cách tối ưu. Cảm ơn các bạn đã theo dõi video và đồng hành cùng tôi."
