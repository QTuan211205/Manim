# KỊCH BẢN FULL VIDEO - SOURCE-FAITHFUL
## Beyond Decoding: Meta-Generation Algorithms for Large Language Models

Nguồn bắt buộc:
- Slide PDF: `slide/neurips2024metageneration-tutorial-all.pdf` và text trích xuất `slide/pdf_text.txt`.
- Subtitle gốc: `subtitle/Subtitle-lab1-ml.txt` và bản sạch `subtitle/Subtitle-lab1-ml-clean.txt`.

Quy tắc biên soạn:
- Chỉ dùng nội dung, ví dụ, công thức và tên phương pháp có trong slide hoặc subtitle.
- Không thêm công thức ngoài, không thêm số liệu xác suất tự nghĩ, không thêm ví dụ ngoài nguồn.
- Visual chuyển thể theo phong cách 3Blue1Brown: nền tối, hình học, cây, luồng token, vùng màu, biểu đồ động. Visual chỉ minh họa lại nội dung nguồn, không thêm khái niệm mới.
- Video gốc theo subtitle dài khoảng 02:17:17. Target bản dựng: khoảng 130 phút, không dài hơn video gốc và lớn hơn 70% thời lượng gốc.
- Slides 215-245 là References. Không biến references thành phần giảng mới; nếu cần dùng trong video, hiển thị như credit/reference roll.

Nội dung cần loại khỏi các bản dựng cũ nếu không xuất hiện trong nguồn:
- Các ví dụ kỹ thuật tự tạo cho Scene 2.1 nếu không xuất hiện trong slide/subtitle.
- Các xác suất, bảng token, ví dụ câu, quote hoặc phát biểu panel không nằm trong subtitle/slide.
- Mọi công thức tự mở rộng từ ý tưởng của tác giả nhưng không có trong slide/subtitle.

---

## Tổng thời lượng và phân cảnh

| Phần | Slide | Thời lượng target |
|---|---:|---:|
| Chương 1: Giới thiệu và khung tutorial | 1-22 | 10:00 |
| Chương 2: Primitive generators | 23-87 | 36:00 |
| Chương 3: Meta-generators | 88-164 | 48:00 |
| Chương 4: Efficient meta-generation | 165-205 | 26:00 |
| Chương 5: Thảo luận Panel (Panel Session) | 206 | 07:00 |
| Tổng | 1-206 | ~127:00 |

---

## CHƯƠNG 1 - GIỚI THIỆU VÀ KHUNG TUTORIAL

### Scene 1.1 - Chủ đề tutorial và động cơ
**Thời lượng:** 00:00-02:00  
**Slide:** 1-4

**Visual 3Blue1Brown:**
- Nền tối, tiêu đề `Beyond Decoding: Meta-Generation Algorithms for Large Language Models` viết dần bằng nét sáng.
- Ba presenter hiện theo slide: Matthew Finlayson, Hailey Schoelkopf, Sean Welleck; ngày `December 11, 2024`.
- Dòng trung tâm: `Algorithms for generating outputs with a language model`.
- Hai ví dụ từ slide xuất hiện như icon: `Solving olympiad problems`, `Writing code`; dưới cùng là `Tasks framed as generating sequences`.

**Công thức/keyword được phép:** Không có công thức.

**Voiceover:**
> Chúng ta bắt đầu với chủ đề chính của video hôm nay: các thuật toán sinh đầu ra bằng mô hình ngôn ngữ, đặc biệt là các thuật toán meta-generation cho mô hình ngôn ngữ lớn (LLM). Lý do chủ đề này quan trọng là vì hiện nay, chúng ta đang tìm cách dùng thêm năng lực tính toán tại thời điểm chạy (test-time compute) – tức là sau khi mô hình đã được huấn luyện – để cải thiện chất lượng của toàn bộ hệ thống tạo văn bản.
>
> Mô hình ngôn ngữ có thể hỗ trợ nhiều tác vụ nếu tác vụ đó được biểu diễn dưới dạng sinh một chuỗi tuần tự: từ việc giải các bài toán Olympic phức tạp cho tới viết mã nguồn thực tế. Vì thế, chúng ta sẽ tập trung vào câu hỏi: khi đã có một mô hình ngôn ngữ, chúng ta nên gọi nó, điều khiển nó, và kết hợp nó với các thành phần khác như thế nào để sinh ra kết quả tốt nhất?
>
> Chúng ta cũng đặt chủ đề này trong bối cảnh các thuật toán suy luận (inference algorithms) và hệ điều hành LLM (LLM OS). Điều này có nghĩa là, chúng ta không chỉ xem mô hình ngôn ngữ như một bộ dự đoán token đơn lẻ, mà xem nó như một thành phần trong một hệ thống sinh hoàn chỉnh: nơi hệ thống có thể gọi mô hình nhiều lần, dùng công cụ bổ trợ, dùng bộ đánh giá (evaluators), và quyết định cách tiêu compute tại thời điểm sinh.

### Scene 1.2 - Ba hướng scale compute
**Thời lượng:** 02:00-04:20  
**Slide:** 5-7

**Visual 3Blue1Brown:**
- Dựng ba trục song song: `pretraining compute`, `post-training compute`, `test-time compute`.
- Trục pretraining: model lớn hơn, dataset lớn hơn; gắn `Scaling Laws for Neural Language Models [Kaplan et al., 2020]`.
- Trục post-training: các cặp `(input, output)` đi vào fine-tuning; gắn `Scaling Instruction-Finetuned Language Models [Chung et al., 2022]`.
- Trục test-time: mũi tên tăng compute tại generation time; gắn `Test-time compute vs. accuracy ([OpenAI, 2024])` và `[Now] Test-time scaling: increase compute at generation time` (Slide 7).

**Công thức/keyword được phép:** `pretraining compute`, `post-training compute`, `test-time compute`, `[Now] Test-time scaling: increase compute at generation time`.

**Voiceover:**
> Khi nhìn vào tiến bộ của các mô hình ngôn ngữ lớn, chúng ta có thể chia làm ba làn sóng scale. Làn sóng đầu tiên là scale pretraining compute: sử dụng mô hình lớn hơn và tập dữ liệu lớn hơn, với các quy luật scale (scaling laws) cho mô hình ngôn ngữ.
>
> Làn sóng thứ hai là post-training compute: thu thập các cặp input-output, rồi fine-tune mô hình để làm tốt hơn trên các tác vụ và có thể generalize sang tác vụ mới.
>
> Làn sóng hiện tại là test-time scaling. Ta giữ mô hình đã huấn luyện, nhưng thiết kế phương pháp dùng thêm compute tại inference hoặc generation time để tăng performance.
>
> Điểm quan trọng cần lưu ý là hai làn sóng đầu, dù rất quan trọng, vẫn chưa đủ cho mọi tác vụ mà chúng ta mong muốn ở mô hình ngôn ngữ. Vì thế, test-time scaling không thay thế pretraining hay post-training; nó là một chiều kích thước tính toán khác, được sử dụng sau khi mô hình đã tồn tại, ngay tại thời điểm hệ thống đang cần sinh câu trả lời.

### Scene 1.3 - Test-time compute được dùng như thế nào
**Thời lượng:** 04:20-07:20  
**Slide:** 8-13

**Visual 3Blue1Brown:**
- Ba panel hiện lần lượt.
- Panel 1: mô hình sinh thêm các token suy nghĩ màu xanh, gắn `Generate extra tokens` và `[Wei et al., 2022]`.
- Panel 2: nhiều output song song đi qua filter/cluster, gắn `Call generator multiple times`, `AlphaCode [Li et al., 2022]`, `Math`, `Agents`, `Chat`.
- Panel 3: language model kết nối với evaluator, code interpreter, search engine; gắn `Incorporate other models/tools` và `[Zaharia et al., 2024]`.

**Công thức/keyword được phép:** `Generate extra tokens`, `Call generator multiple times`, `Verifiers`, `code interpreters`, `search engines`.

**Voiceover:**
> Có ba cách chính để dùng test-time compute. Thứ nhất, chúng ta cho mô hình sinh thêm token, ví dụ như chain-of-thought: mô hình viết ra các bước suy nghĩ trung gian trước khi đưa ra câu trả lời cuối cùng.
>
> Thứ hai, chúng ta gọi generator nhiều lần. AlphaCode là ví dụ điển hình: hệ thống sinh ra rất nhiều chương trình ứng viên, rồi tiến hành lọc và gom nhóm để lấy một tập kết quả nhỏ hơn nhưng chất lượng hơn.
>
> Thứ ba, chúng ta chuyển từ một mô hình ngôn ngữ đơn lẻ sang một compound AI system (hệ thống AI phức hợp): ở đó mô hình có thể kết hợp với các bộ đánh giá (evaluators), kiểm định (verifiers), code interpreter, công cụ tìm kiếm hoặc công cụ bên ngoài. Đây chính là nền tảng để định nghĩa meta-generation.
>
> Khi sinh thêm token, mỗi token mới tương ứng với một lần chạy qua mạng neural (forward pass), nên bản thân việc sinh thêm token đã tiêu tốn tài nguyên tính toán. Với chain-of-thought, lượng compute đó dùng để tạo ra các token suy nghĩ trung gian. Với việc gọi lại nhiều lần (repeated calls), compute được dùng để tạo nhiều ứng viên. Còn với compound AI system, một phần gánh nặng tính toán có thể được chuyển giao cho các công cụ chuyên biệt đáng tin cậy như code interpreter hay công cụ tìm kiếm.

### Scene 1.4 - Generator và meta-generator
**Thời lượng:** 07:20-10:00  
**Slide:** 14-22

**Visual 3Blue1Brown:**
- Hộp `Generator` nhận input sequence và language model, trả output sequence.
- Hộp lớn `Meta-generator` bao quanh nhiều generator và một evaluator/tool.
- Bảng ba phần của tutorial hiện ở cuối: Primitive generators, Meta-generators, Efficient meta-generation.
- Hiển thị presenter và panel đúng theo slide 19-20.
- Kết bằng link resource: `cmu-l3.github.io/neurips2024-inference-tutorial`.

**Công thức/keyword được phép:** `Generator`, `Meta-generator`, `Greedy decoding`, `Temperature sampling`.

**Voiceover:**
> Generator là bất kỳ thuật toán nào nhận một input sequence và language model rồi sinh ra output sequence. Khi gọi một LLM API thông thường, ta có thể xem đó là một generator.
>
> Meta-generator là chiến lược cấp cao hơn: gọi generator nhiều lần, dùng external information, hoặc chọn output tốt nhất bằng một mô hình riêng. Lý do dùng meta-generator là để generate more nhằm cải thiện task performance, kết hợp nhiều mô hình như verifier hay retriever, và đưa thông tin bên ngoài như tools hay feedback vào generation.
>
> Nội dung chính của chúng ta gồm ba phần: primitive generators, meta-generators, và efficient meta-generation, tiếp theo là buổi thảo luận panel. Chúng ta cũng có thể truy cập các tài nguyên trực tuyến để xem slide, ví dụ code và danh sách tài liệu đọc thêm.
>
> Từ "primitive" ở đây không có nghĩa là các phương pháp này không quan trọng. Chúng ta có thể hiểu chúng là các primitives theo nghĩa building blocks – tức là những khối cơ bản để xây dựng các thuật toán meta-generation phức tạp hơn. Vì thế, trước khi nói về meta-generator, chúng ta phải hiểu cách một generator sinh ra một chuỗi đơn lẻ.

---

## CHƯƠNG 2 - PRIMITIVE GENERATORS

### Scene 2.1 - Token-level generation và decoding là search
**Thời lượng:** 10:00-16:30  
**Slide:** 23-31

**Visual 3Blue1Brown:**
- Mở với title `I. Primitive Generators` và subtitle `Generating one token at a time`.
- Chuỗi nguồn từ slide: `Taylor Alison Swift (born December 13, 1989) is`.
- Một hộp `LM` nhận prefix `x_<t` và xuất phân phối token: `an`, `a`, `the`, `best`, `one`, ... (định nghĩa `which defines a conditional distribution over tokens pθ[xt | x<t].` - Slide 26-29).
- Token `an` được chọn rồi prefix cập nhật thành `... is an`; phân phối tiếp theo gồm `American`, `actress`, `English`, `actor`, `award`, ...
- Chuyển sang cây quyết định từ slide 30 cho `Taylor Swift is` (phân tích `Prefix Continuation Prob.` ở Slide 34-36): các nhánh `the`, `a`, `writer`, `singer`, `and`, `song`, `producer`, ...
- Kết bằng outline slide 31: `Optimization`, `Sampling`, `Constrained generation, structured outputs`.

**Công thức/keyword được phép:**
```tex
p_\theta[x_t \mid x_{<t}]
```
`which defines a conditional distribution over tokens pθ[xt | x<t].`, `Prefix Continuation Prob.`.

**Voiceover:**
> Trong primitive generators, ta bắt đầu với token-level generation. Auto-regressive language modeling dùng causal language model, định nghĩa một phân phối có điều kiện trên token tiếp theo: `pθ[x_t | x_<t]`.
>
> Ở mỗi bước decoding, mô hình nhìn prefix `x_<t` và đưa ra phân phối cho token kế tiếp. Thuật toán decoding ở cấp token chủ yếu quan tâm đến việc chọn token tiếp theo như thế nào.
>
> Vì mỗi time-step đều yêu cầu một lựa chọn, decoding có thể được xem như search. Nhưng search để làm gì? Objective là gì? Và làm thế nào các lựa chọn cục bộ dẫn đến objective đó? Phần tiếp theo chia primitive generators thành ba hướng: optimization, sampling, và constrained generation hoặc structured outputs.
>
> Khi visual hóa scene này, điều quan trọng là người xem thấy sự khác biệt giữa language model và decoding algorithm. Language model cung cấp phân phối xác suất cho token tiếp theo; decoding algorithm mới là quy tắc quyết định lấy token nào từ phân phối đó. Cùng một mô hình có thể được dùng với greedy decoding, beam search, sampling, hoặc constrained decoding.
>
> Cây lựa chọn ở slide `Decoding is search` cho thấy vì sao vấn đề này không chỉ là lấy một token rồi dừng. Một lựa chọn local ở bước hiện tại sẽ thay đổi prefix, và prefix mới lại tạo ra phân phối mới cho bước sau. Do đó thuật toán decoding phải nối các lựa chọn local thành một sequence cuối cùng theo objective đã chọn.

### Scene 2.2 - MAP, greedy decoding và beam search
**Thời lượng:** 16:30-23:00  
**Slide:** 32-41

**Visual 3Blue1Brown:**
- Slide title `Decoding as optimization`.
- Hiển thị objective MAP ở trung tâm.
- Greedy decoding: mỗi bước chọn token có xác suất lớn nhất; dựng bảng đúng từ slide:
  - Greedy path: `Taylor Swift is an American singer . <eos>`; token probabilities: `0.80`, `0.02`, `0.05`, `1.0` (cumulative: `0.0008`).
  - Non-greedy path: `Taylor Swift is a singer , songwriter`; token probabilities: `0.13`, `0.90`, `0.26`, `0.80` (cumulative: `0.0243`).
- Beam search: vẽ cây width-limited BFS đúng nhánh slide 37-41, gồm:
  - Step 1: `"an"` (0.80), `"a"` (0.13), `"the"` (0.06), `"to"` (0.0004). Keeps `"an"` and `"a"`.
  - Step 2: `"an American"` (0.0160), `"an artist"` (0.0080), `"a singer"` (0.1170), `"a songwriter"` (0.1040). Keeps `"a singer"` and `"a songwriter"`, pruning `"an American"` (the greedy choice!).
- Nhãn bắt buộc: `GPT2, beam size 2`; `Beam search with beam size 1 is greedy decoding`; `width-limited BFS`; citations `[Freitag and Al-Onaizan, 2017]`, `[Shi et al., 2024]`.

**Công thức/keyword được phép:**
```tex
\arg\max_x p_\theta[x]
```
```tex
x_t = \arg\max_x p_\theta[x \mid x_{<t}]
```

**Voiceover:**
> MAP decoding tìm chuỗi có xác suất cao nhất theo mô hình: `arg max_x pθ[x]`. Hai thuật toán optimization phổ biến là greedy decoding và beam search, với các tài liệu tham khảo chính từ [Freitag and Al-Onaizan, 2017] và [Shi et al., 2024].
>
> Greedy decoding chọn token có xác suất cao nhất tại từng bước: `x_t = arg max_x pθ[x | x_<t]`. Nhưng giải mã tham lam không đảm bảo tìm được chuỗi có xác suất cao nhất (MAP). Slide minh họa một chuỗi greedy với các token prob `0.80` ("an"), `0.02` ("American"), `0.05` ("singer"), `1.0` ("<eos>") cho ra cumulative probability chỉ `0.0008`, trong khi một chuỗi non-greedy bắt đầu bằng xác suất thấp hơn `0.13` ("a") tiếp nối bởi `0.90` ("singer"), `0.26` (","), `0.80` ("songwriter") đạt cumulative probability lên tới `0.0243`, cao hơn giải pháp tham lam tới 30 lần!
>
> Beam search là thuật toán width-limited breadth-first search (BFS). Ở mỗi bước, nó giữ lại một số nhánh tốt nhất theo độ rộng beam size K, rồi tiếp tục mở rộng. Với GPT2 và beam size 2, ở bước 1 ta giữ lại "an" (0.80) và "a" (0.13). Ở bước 2, ta tính và so sánh cumulative scores của các nhánh con: "a singer" (0.117), "a songwriter" (0.104), "an American" (0.016), "an artist" (0.008). Beam search giữ lại "a singer" và "a songwriter", đồng thời cắt tỉa (prune) nhánh "an American" - vốn bắt đầu bằng lựa chọn tham lam tốt nhất! Lưu ý rằng khi beam size K = 1, beam search chính là greedy decoding.
>
> Subtitle giải thích greedy giống một lựa chọn cục bộ: ở mỗi bước nó chọn token tốt nhất ngay lúc đó. Điều này đơn giản và rẻ, nhưng không bảo đảm tối ưu toàn chuỗi, vì chuỗi tốt hơn có thể bắt đầu bằng một token không phải token tốt nhất tại bước đầu.
>
> Beam search là điểm trung gian giữa greedy và exhaustive search. Exhaustive search sẽ mở rộng quá nhiều khả năng nên không feasible với language model có hàng chục hoặc hàng trăm nghìn token trong vocabulary. Beam search giữ lại một beam hữu hạn, vì vậy nó vẫn search qua nhiều nhánh hơn greedy nhưng kiểm soát được chi phí bằng beam size.

### Scene 2.3 - Lợi ích và cạm bẫy của MAP
**Thời lượng:** 23:00-28:30  
**Slide:** 42-47

**Visual 3Blue1Brown:**
- Mở bằng `Benefits of MAP`: closed-ended tasks như translation và question answering.
- Ba warning cards chỉ rõ `Probability maximization causes decoding problems.` (Slide 43-47): `Repetition traps [Welleck et al., 2020]`, `Short sequences [Stahlberg and Byrne, 2019]`, `Atypicality [Meister et al., 2022]` và `than exact MAP [Meister et al., 2020] .`.
- Repetition: hiển thị đúng đoạn GPT2 beam size 32 về Taylor Swift lặp `singer-songwriter`, `songwriter-songwriter`, `song-writer-songwriter`.
- Short sequence: so sánh xác suất đúng từ slide: `Pr[Taylor Swift is <eos>] > Pr[Taylor Swift is an American singer-…]`; remedy: `length normalization`.
- Atypicality: đồng xu lệch `Pr[H]=0.6`, `Pr[T]=0.4`; outcome 100 heads là most likely nhưng atypical.
- Kết luận slide 47: approximate MAP, ví dụ narrow beam search, hoạt động tốt hơn exact MAP [Meister et al., 2020].

**Công thức/keyword được phép:**
```tex
Pr[H] = 0.6,\quad Pr[T] = 0.4
```
```tex
Pr[\text{Taylor Swift is <eos>}] > Pr[\text{Taylor Swift is an American singer-...}]
```
Citations: `[Welleck et al., 2020]`, `[Stahlberg and Byrne, 2019]`, `[Meister et al., 2022]`, `[Meister et al., 2020]`.

**Voiceover:**
> MAP decoding hoạt động tốt cho các tác vụ closed-ended như translation và question answering. Nhưng cực đại hóa xác suất cũng gây ra nhiều lỗi giải mã nghiêm trọng.
>
> Cạm bẫy đầu tiên là repetition traps (bẫy lặp từ) được nghiên cứu bởi [Welleck et al., 2020]. Với GPT2 và beam size 32, output có thể bị lặp vô tận các cụm từ như `singer-songwriter`, `songwriter-songwriter`. Các phương pháp khắc phục bao gồm repetition penalty và unlikelihood training.
>
> Cạm bẫy thứ hai là sinh chuỗi quá ngắn (short sequences) theo nghiên cứu của [Stahlberg and Byrne, 2019]: một chuỗi kết thúc sớm bằng token `<eos>` có thể có xác suất tích lũy cao hơn một câu dài đầy đủ thông tin hơn, ví dụ `Pr[Taylor Swift is <eos>] > Pr[Taylor Swift is an American singer-...]`. Phương pháp khắc phục phổ biến là length normalization.
>
> Cạm bẫy thứ ba là tính chất phi điển hình (atypicality) được phân tích bởi [Meister et al., 2022]. Với đồng xu lệch có xác suất ngửa `Pr[H]=0.6` và sấp `Pr[T]=0.4`, chuỗi kết quả có xác suất cao nhất cho 100 lần tung là toàn ngửa (HHHH...), nhưng chuỗi này lại vô cùng phi điển hình và thiếu tự nhiên. Tương tự, một generation có xác suất cao nhất của mô hình chưa chắc đã tự nhiên. Vì vậy, kết luận quan trọng của chúng ta là approximate MAP (chẳng hạn như narrow beam search) hoạt động tốt hơn exact MAP [Meister et al., 2020].
>
> Ý chính của đoạn này là `most likely` không đồng nghĩa với `best` cho mọi loại generation. Trong closed-ended tasks, MAP thường hữu ích vì output space bị ràng buộc và có đáp án rõ. Nhưng với open-ended text generation, cực đại hóa xác suất có thể đẩy mô hình vào output lặp, quá ngắn, hoặc không điển hình. Vì vậy chúng ta dùng các cạm bẫy này để chuyển từ optimization sang sampling.

### Scene 2.4 - Sampling, truncation và temperature
**Thời lượng:** 28:30-38:30  
**Slide:** 48-65

**Visual 3Blue1Brown:**
- Mở slide `Sampling` và `Objective: Sampling`, với settings sampling từ modern LLM APIs.
- Ancestral sampling: các token `y1`, `y2`, `y3` được sinh tuần tự từ phân phối điều kiện.
- So sánh ba cột từ slide 52-54: `Greedy (repetition trap)`, `Ancestral (incoherent)`, `Top-k (acceptable)` với đúng đoạn Taylor Swift trong slide.
- Truncation table slide 55: `Top-k`, `Top-p`, `epsilon` (probability threshold), `eta` (prob and entropy threshold), `Min-p` (probability at least p_min scaled by maximum token probability).
- Biểu đồ logprob từ slide 56-58 cho hai prefix `Taylor Swift` và `My name`; highlight từ `' made'` với `Top-k = 5` và `Top-p = 0.9` để thể hiện vùng token được giữ.
- Temperature: ba panel `tau=0.5`, `tau=1`, `tau=2`; không thêm giá trị xác suất ngoài slide.
- Code panels từ slide 61-62:
  - Greedy: `indices, weights = probs.argmax(keepdim=True), None`
  - Ancestral: `indices, weights = vocab_size, probs`
  - Top-k: `topk = probs.topk(k); indices, weights = topk.indices, topk.values`
  - Top-p: `argsort = probs.argsort(descending=True); top_p = (argsort.values.cumsum() < p).sum() + 1; indices, weights = argsort.indices[:top_p], argsort.values[:top_p]`
  - Epsilon: `indices, weights = vocab_size, probs * (probs > epsilon)`
  - Temperature: `indices, weights = vocab_size, (logits / temp).softmax(-1)`
  - Lấy mẫu: `next_token = random.choices(indices, weights=weights, k=1)`
  - vLLM: `llm = LLM(model="facebook/opt-125m"); sampling_params = SamplingParams(temperature=0.8, top_p=0.95); outputs = llm.generate(prompts, sampling_params)`
  - HF: `model = AutoModelForCausalLM.from_pretrained("gpt2"); tokenizer = AutoTokenizer.from_pretrained("gpt2"); text = "Hello, my name is"`
- Heavy-tail causes slide 63-65: `Under-training`, `Mode-seeking`, `low-rank constraints`.

**Công thức/keyword được phép:**
```tex
y_1 \sim p_\theta(\cdot \mid x),\quad
y_2 \sim p_\theta(\cdot \mid x, y_1),\quad
y_3 \sim p_\theta(\cdot \mid x, y_1, y_2)
```
```tex
p_\theta(y)=p_\theta(y_1)p_\theta(y_2\mid y_1)p_\theta(y_3\mid y_1y_2)\cdots p_\theta(y_T\mid y_{<T})
```
```tex
\mathrm{softmax}(x,\tau)=\frac{\exp(x/\tau)}{\sum_i \exp(x_i/\tau)}
```

**Voiceover:**
> Bây giờ objective chuyển sang sampling. Ancestral sampling sinh từng token bằng cách lấy mẫu từ phân phối điều kiện của mô hình: `y_t ~ pθ(· | x, y_<t)`. Điều này tương đương với sequence sampling theo tích các xác suất điều kiện.
>
> Vấn đề là greedy decoding gây repetition traps, còn ancestral sampling có thể gây incoherence do low-probability tokens are too likely (phân phối có heavy tail). Giải pháp là chop off the tail bằng truncation sampling.
>
> Truncation sampling chọn threshold xác suất ở mỗi time step. Slide 55 liệt kê: Top-k, Top-p, epsilon (giữ token có prob >= epsilon), eta, và Min-p (giữ token có xác suất tối thiểu bằng p_min nhân với xác suất của token lớn nhất). Khi so sánh prefix "Taylor Swift" và "My name" ở slide 56-58, ta thấy Top-k=5 luôn giữ cố định số lượng token, trong khi Top-p=0.9 tự co giãn theo tổng xác suất tích lũy của các token hàng đầu (ví dụ giữ lại từ ' made' có xác suất tích lũy cao).
>
> Temperature là một adapter khác: nó không cắt đuôi mà rescale logits bằng công thức softmax chia cho tau. High tau (>= 1) tăng tính đa dạng (diverse) nhưng dễ incoherent; low tau (< 1) tăng tính mạch lạc (coherent) nhưng dễ bị lặp (repetitive).
>
> Phần code trong slide 61 minh họa các thuật toán: greedy dùng argmax; ancestral lấy mẫu trên toàn bộ vocab; Top-k chọn k giá trị hàng đầu; Top-p sắp xếp logits giảm dần rồi tính cumsum dưới p; epsilon lọc theo ngưỡng cứng; temperature điều phối qua logits/temp trước khi softmax; cuối cùng dùng random.choices để lấy mẫu token. Slide 62 cũng cung cách dùng framework vLLM qua LLM.generate và HuggingFace qua AutoModelForCausalLM. Chúng ta kết thúc bằng ba lý do heavy-tail: under-training, tính chất mode-seeking của cross-entropy loss, và low-rank constraints của output layer.
>
> Khi giải thích Top-k và Top-p, cần nhấn mạnh sự khác biệt về threshold. Top-k luôn giữ đúng k token có xác suất cao nhất, nên nó không tự thích nghi với hình dạng phân phối. Top-p dùng cumulative probability, nên vùng được giữ có thể co giãn theo phân phối.
>
> Temperature không quyết định token nào bị cắt, mà rescale logits trước khi lấy mẫu. Vì vậy trong visual, temperature nên được thể hiện bằng phân phối trở nên peaked hơn hoặc gần uniform hơn, còn truncation nên được thể hiện bằng vùng token được giữ lại để sample.

### Scene 2.5 - Sampling adapters, constrained decoding và token healing
**Thời lượng:** 38:30-46:00  
**Slide:** 66-87

**Visual 3Blue1Brown:**
- Mở bằng bảng `Sampling adapters`: `A sampling adapter takes a token distribution pθ(· | x) and re-adjusts` (Slide 66-68).
- Hiển thị đủ các method trong bảng slide 66-68 với chú thích chi tiết:
  - `Ancestral sampling y∼pθ`
  - `Temperature sampling [Ackley et al., 1985]y∼q(pθ) Rescale`
  - `Greedy decoding y←maxpθ Argmax (temperature→0)`
  - `Top-k sampling [Fan et al., 2018]y∼q(pθ) Truncation (top-k)`
  - `Nucleus sampling [Holtzman et al., 2020]y∼q(pθ) Truncation (cumulative prob.)`
  - `Typical sampling [Meister et al., 2023]y∼q(pθ) Truncation (entropy)`
  - `Epsilon sampling [Hewitt et al., 2022]y∼q(pθ) Truncation (probability)`
  - `ηsampling [Hewitt et al., 2022]y∼q(pθ) Truncation (prob. and entropy)`
  - `Mirostat decoding [Basu et al., 2021] Target perplexity Truncation (adaptive top-k)`
  - `Basis-aware sampling [Finlayson et al., 2024]y∼q(pθ) Truncation (linear program)`
  - `Contrastive decoding [Li et al., 2023a]y∼q(pθ) log pθ′ −logpθand truncation`
  - `DExperts [Liu et al., 2021] y∼q∗(·|x,c) ∝pθ·(pθ+/pθ−)α`
  - `Inference-time adapters [Lu et al., 2023]y∼q∗∝r(y) ∝(pθ·pθ′)α`
  - `• Contrastive decoding [Li et al., 2023a, Liu et al., 2021]`
- Constrained decoding: prompt JSON Taylor Swift, schema `name: string`, `birth year: int`, output sai schema từ LLM.
- State machine slide 73-81: các node `start`, `{`, `"name"`, `[A-Za-z]`, `"birth year"`, `\d`, `}`.
- Tại mỗi bước, bảng GPT2 token probability chỉ hiển thị đúng các token/prob trong slide: `\n 0.36`, `" 0.16`, `{ 0.026`, `https 0.025`; `name 0.31`, `date 0.069`; `Taylor 0.85`; `1989 0.020`; `} 0.34`, v.v.
- Side effects slide 82: `Generation speedup`, `Reduced performance`.
- Token healing slide 83-86: `The url is http:` rồi `://`, candidates `s://`, `://`; alternative fix: tokenizer regularization during `training [Kudo, 2018].`
- Kết slide 87 summary.

**Công thức/keyword được phép:**
```tex
p(\cdot \mid x) \propto \frac{p_{expert}(\cdot \mid x)}{p_{antiexpert}(\cdot \mid x)}
```
```tex
y \sim q(p_\theta),\quad y \leftarrow \max p_\theta
```
```tex
\log p_{\theta'} - \log p_\theta
```
```tex
y \sim q^*(\cdot\mid x,c) \propto p_\theta \cdot (p_{\theta+}/p_{\theta-})^\alpha
```
```tex
y \sim q^* \propto r(y) \propto (p_\theta \cdot p_{\theta'})^\alpha
```
`A sampling adapter takes a token distribution pθ(· | x) and re-adjusts`, `Temperature sampling [Ackley et al., 1985]y∼q(pθ) Rescale`, `Top-k sampling [Fan et al., 2018]y∼q(pθ) Truncation (top-k)`, `Nucleus sampling [Holtzman et al., 2020]y∼q(pθ) Truncation (cumulative prob.)`, `Epsilon sampling [Hewitt et al., 2022]y∼q(pθ) Truncation (probability)`, `ηsampling [Hewitt et al., 2022]y∼q(pθ) Truncation (prob. and entropy)`, `Mirostat decoding [Basu et al., 2021] Target perplexity Truncation (adaptive top-k)`, `Basis-aware sampling [Finlayson et al., 2024]y∼q(pθ) Truncation (linear program)`, `Contrastive decoding [Li et al., 2023a]y∼q(pθ) log pθ′ −logpθand truncation`, `• Contrastive decoding [Li et al., 2023a, Liu et al., 2021]`, `training [Kudo, 2018].`

**Voiceover:**
> Sampling adapter nhận phân phối token `pθ(. | x)` và điều chỉnh lại xác suất. Truncation và temperature là adapters, nhưng bảng phân loại của chúng ta còn liệt kê nhiều phương pháp khác như typical sampling, epsilon, eta, Mirostat, basis-aware sampling, contrastive decoding, DExperts, inference-time adapters và proxy tuning. Với các công thức, chỉ dùng đúng các biểu thức trong bảng slide.
>
> Constrained decoding xuất hiện khi ta nhúng LLM vào hệ thống lớn hơn và cần output có cấu trúc, ví dụ JSON. Prompt yêu cầu format thông tin Taylor Swift theo schema `name: string`, `birth year: int`, nhưng output tự do của LLM không khớp JSON schema.
>
> Cách làm trong slide gồm hai bước: compile schema thành state machine, rồi filter next-token distribution để chỉ giữ token hợp lệ. Khi state machine yêu cầu dấu `{`, token khác bị loại; khi đang trong trường name, chỉ token phù hợp mới được phép đi tiếp. Nhờ vậy chuỗi cuối cùng có thể thành `{"name": "Taylor Swift", "birth year": 1989}`.
>
> Constrained decoding có side effects: có thể speed up generation, nhưng cũng có thể reduced performance. Token healing xử lý trường hợp templated generation ép boundary không tự nhiên, ví dụ `The url is http:` rồi `://`. Token healing rewinds tokenizer và enforce untokenized text như prefix cho token tiếp theo. Alternative fix trong slide là tokenizer regularization during training.
>
> Summary của phần primitive generators: có hai view của decoding là optimization và sampling; có diversity-coherence trade-off; constrained decoding enforce structure on LLM outputs. Đây là building blocks của modern LLM generation methods.
>
> Với sampling adapters, người xem cần hiểu rằng adapter không thay thế language model. Nó nhận phân phối từ model và re-adjust probabilities trước khi chọn token. Vì vậy temperature, truncation, contrastive decoding hay DExperts đều có thể được visual hóa như các lớp biến đổi đặt sau phân phối gốc `pθ`.
>
> Với constrained decoding, khái niệm cốt lõi là state machine biến schema thành tập token hợp lệ tại mỗi bước. Nếu token không đưa hệ thống sang state hợp lệ, token đó bị filter khỏi next-token distribution. Đây là cách ép LLM giao tiếp với hệ thống lớn hơn bằng structured outputs như JSON.

---

## CHƯƠNG 3 - META-GENERATORS

### Scene 3.1 - Mục tiêu, formalization và chaining
**Thời lượng:** 46:00-57:00  
**Slide:** 88-107

**Visual 3Blue1Brown:**
- Mở với title `Meta-generators`.
- System designer chọn một hệ thống `G` (với giả định `We know how to sample probable outputs, y ∼ pθ(y|x)` - Slide 89-90); bên cạnh là evaluator `A(y)` cho acceptability.
- Hiển thị hộp tương đương thuật ngữ từ Slide 91-92: `Terminology: Evaluator ≈ critic ≈ verifier ≈ value ≈ reward model ≈ scoring model` và mối quan hệ `v(y) ≈ A(y)`.
- Oracle verifier loop từ slide 95-96: `z ~ pθ(z|x)`, `y ~ pθ(y|x,z)`, stop nếu verifier nói answer correct (`1Adapted from [Brown et al., 2024]. See also [Li et al., 2022, Cobbe et al., 2021, Jiang et al., 2023]` - Slide 96).
- Formalization slide 97: meta-generator gọi nhiều generators `g1, g2, ..., gG` và parameters `φ`.
- Token-level generator special case slide 98.
- Chain slides 100-106:
  - `Motivating example: Chain-of-thought [Wei et al., 2022]:` với chú thích: `Variable output length, analogous to a writeable tape` và `3E.g., [Feng et al., 2023, Merrill and Sabharwal, 2024, Nowak et al., 2024]`.
  - `Self-Ask [Press et al., 2023]`.
  - `Demonstrate-Search-Predict (DSP)` (`[Khattab et al., 2022]`, `4[Khattab et al., 2022, Dohan et al., 2022, Schlag et al., 2023, Zheng et al., 2024]`).
  - `(System-2 Attention [Weston and Sukhbaatar, 2023])` và `(Draft-Sketch-Prove [Jiang et al., 2023])`.

**Công thức/keyword được phép:**
```tex
\arg\max_G\; \mathbb{E}_{y\sim G(\cdot)} A(y)
```
```tex
y \sim p_\theta(y\mid x),\quad v(y) \approx A(y)
```
```tex
z \sim p_\theta(z\mid x),\quad y \sim p_\theta(y\mid x,z)
```
```tex
y \sim G(y\mid x; g_1,g_2,\ldots,g_G,\phi)
```
```tex
y \sim g(y\mid x; p_\theta,\phi)
```
`We know how to sample probable outputs, y ∼ pθ(y|x)`, `1Adapted from [Brown et al., 2024]. See also [Li et al., 2022, Cobbe et al., 2021, Jiang et al., 2023]`, `Motivating example: Chain-of-thought [Wei et al., 2022]:`, `3E.g., [Feng et al., 2023, Merrill and Sabharwal, 2024, Nowak et al., 2024]`, `4[Khattab et al., 2022, Dohan et al., 2022, Schlag et al., 2023, Zheng et al., 2024]`, `(System-2 Attention [Weston and Sukhbaatar, 2023])`, `(Draft-Sketch-Prove [Jiang et al., 2023])`.
```tex
y_1\sim g_1(x),\quad y_2\sim g_2(x,y_1),\quad y_3\sim g_3(x,y_2)
```
Citations: `[Brown et al., 2024]`, `[Wei et al., 2022]`, `[Press et al., 2023]`, `[Khattab et al., 2022]`, `[Weston and Sukhbaatar, 2023]`, `[Jiang et al., 2023]`.

**Voiceover:**
> Mục tiêu của system designer là thiết kế một hệ thống `G` sinh ra acceptable sequences. Slide viết mục tiêu là tối ưu kỳ vọng acceptability `A(y)` trên output của `G`: `arg max_G E[A(y)]`. Acceptability có thể là correctness hoặc human preferences.
>
> Ta đã biết cách sinh probable outputs `y ~ pθ(y|x)`, nhưng nếu các output probable đó không acceptable thì cần thêm chiến lược. Ý tưởng đầu tiên của meta-generation là tận dụng external information, ví dụ học một evaluator `v(y) ≈ A(y)` và dùng nó khi sinh. Slide 91-92 nhấn mạnh sự tương đương thuật ngữ: Evaluator ≈ critic ≈ verifier ≈ value ≈ reward model ≈ scoring model.
>
> Ý tưởng thứ hai là gọi generator nhiều hơn một lần để search for good sequences. Với oracle verifier loop (phát triển từ [Brown et al., 2024], [Li et al., 2022], [Cobbe et al., 2021]), ta có thể lặp: sinh intermediate `z ~ pθ(z|x)`, sinh answer `y ~ pθ(y|x,z)`, rồi dừng khi verifier xác nhận answer correct.
>
> Formalization của slide là `y ~ G(y|x; g1, g2, ..., gG, φ)`. Design choices gồm strategy `G`, lựa chọn generators `g1...gG`, và các parameter khác như number of tokens. Token-level generators ở phần trước là special case: `y ~ g(y|x; pθ, φ)`.
>
> Chaining compose generators theo thứ tự: `y1 ~ g1(x)`, `y2 ~ g2(x,y1)`, `y3 ~ g3(x,y2)`. Chain-of-thought [Wei et al., 2022] là ví dụ điển hình: generate thought `z`, rồi generate answer `a`. Chúng ta ví von CoT như một dải băng ghi chép (writeable tape) giúp tăng tính biểu diễn nhờ độ dài đầu ra linh hoạt (variable output length). Chaining có thể mở rộng sang Self-Ask [Press et al., 2023], Demonstrate-Search-Predict (DSP) [Khattab et al., 2022], System-2 Attention [Weston and Sukhbaatar, 2023] và Draft-Sketch-Prove [Jiang et al., 2023]. Takeaway: chaining phân rã quá trình sinh và tích hợp công cụ/mô hình, nhưng chaining đơn thuần không explore output space.
>
> Điểm quan trọng của acceptability là nó không nhất thiết trùng với probability của mô hình. Một output có thể probable theo `pθ` nhưng không correct, không được con người thích, hoặc không đáp ứng yêu cầu của hệ thống. Meta-generation được đưa vào để tìm cách sinh ra sequences acceptable hơn, bằng cách dùng evaluator, verifier, tool, hoặc bằng cách gọi generator nhiều lần.
>
> Với chain-of-thought, subtitle nhấn mạnh đây là một decomposition đơn giản nhưng có tác động sâu: hệ thống cho phép sinh một intermediate thought `z`, rồi dùng `z` để sinh answer `a`. Slide cũng nói chain-of-thought tăng expressivity vì output length có thể biến đổi, tương tự một writable tape. Khi dựng visual, nên thể hiện chain như một chương trình nhiều bước: outer function là meta-generator, inner calls là generators hoặc tools.

### Scene 3.2 - Parallel generation, Best-of-N, voting và weighted voting
**Thời lượng:** 57:00-68:30  
**Slide:** 108-125

**Visual 3Blue1Brown:**
- Nhiều candidate `{y^(1),...,y^(N)}` sinh song song từ `G(· | x)`.
- Aggregator `y = h(y^(1),...,y^(N))` nhận toàn bộ candidates và trả `y`.
- Best-of-N: các candidates đi qua reward model `v(y) -> [0,1]`, candidate điểm cao nhất sáng lên: `Best-of-N = argmax_{y in {y^(1), ..., y^(N)}} v(y)`. Hiển thị `Best-of-N ≈ argmax_y v(y) ≈ argmax_y A(y)` (Citations: [Stiennon et al., 2020, Nakano et al., 2022]).
- Reward model training: hai slide riêng cho correct/incorrect examples ([Cobbe et al., 2021]) và preference data ([Stiennon et al., 2020]).
- Đồ thị over-optimization từ slide 115 biểu diễn mối quan hệ giữa true performance và optimization score.
- Voting/self-consistency: nhiều solution path hội tụ về answer `a`; answer có nhiều vote nhất được chọn: `argmax_a sum_{i=1}^N 1{y^(i) = a}` (Citation: [Wang et al., 2023]).
- Weighted voting: vote được nhân bởi reward model score `v(y^(i))`: `argmax_a sum_{i=1}^N v(y^(i)) * 1{y^(i) = a}` (Citation: [Li et al., 2023b]).
- Easy-to-Hard Generalization: slide 118 hiển thị `10[Sun et al., 2024] Easy-to-Hard Generalization: Scalable Alignment Beyond Human Supervision .` về việc verifier vượt qua con người.
- Convergence theorem slide 119-122 [Zhang et al., 2024]: hiển thị công thức hội tụ khi `N -> infinity` và ba takeaway.
- Kết slide 124-125: parallel meta-generators explore output space bằng full sequences, large gains, bounded by evaluator/generator quality, verifier chỉ dùng ở cuối.

**Công thức/keyword được phép:**
`10[Sun et al., 2024] Easy-to-Hard Generalization: Scalable Alignment Beyond Human Supervision .`
```tex
\{y^{(1)},\ldots,y^{(N)}\}\sim G(\cdot\mid x),\quad y=h(y^{(1)},\ldots,y^{(N)})
```
```tex
\text{Best-of-N}=\arg\max_{y\in\{y^{(1)},\ldots,y^{(N)}\}} v(y)
```
```tex
\text{Best-of-N}\approx \arg\max_y v(y)\approx \arg\max_y A(y)
```
```tex
\arg\max_a\sum_{i=1}^N \mathbf{1}\{y^{(i)}=a\}
```
```tex
\arg\max_a\sum_{i=1}^N v(y^{(i)})\cdot \mathbf{1}\{y^{(i)}=a\}
```
```tex
\frac{1}{M}\sum_{i=1}^M I\left[a_i^*=\arg\max_a\sum_z v(x,z,a)g(z,a\mid x)\right]
```
Citations: `[Stiennon et al., 2020]`, `[Nakano et al., 2022]`, `[Cobbe et al., 2021]`, `[Wang et al., 2023]`, `[Li et al., 2023b]`, `[Sun et al., 2024]`, `[Zhang et al., 2024]`.

**Voiceover:**
> Parallel meta-generators sinh nhiều candidates song song: `{y^(1), ..., y^(N)} ~ G(· | x)`, rồi aggregate thành output cuối cùng bằng `y = h(y^(1), ..., y^(N))`.
>
> Chiến lược đầu tiên là Best-of-N (hay rejection sampling), chọn candidate có reward model score cao nhất: `Best-of-N = argmax v(y)`. Công thức này xấp xỉ giá trị cực đại của acceptability, với cơ sở từ nghiên cứu của [Stiennon et al., 2020] và [Nakano et al., 2022]. Reward model `v(y) -> [0, 1]` có thể được huấn luyện từ các ví dụ đúng/sai ([Cobbe et al., 2021]) hoặc preference data ([Stiennon et al., 2020]). Khi số lượng sinh `N` tăng, Best-of-N tiệm cận tốt hơn với `argmax A(y)`, nhưng nếu reward model không hoàn hảo, hệ thống sẽ gặp bẫy `over-optimization` (được minh họa bằng đồ thị slide 115).
>
> Phương pháp aggregation thứ hai là Voting (Self-Consistency) chọn đáp án nhận nhiều phiếu bầu nhất: `argmax sum 1{y^(i) = a}` theo [Wang et al., 2023]. Weighted voting tiến xa hơn bằng cách nhân thêm điểm số của reward model vào mỗi phiếu: `argmax sum v(y^(i)) * 1{y^(i) = a}` theo [Li et al., 2023b]. Slide 118 cũng đưa ra một khía cạnh thú vị: Easy-to-Hard Generalization của [Sun et al., 2024], trong đó verifier có thể hoạt động hiệu quả hơn cả người chấm điểm. Khi số mẫu `N` tiến đến vô cùng, độ chính xác của voting hội tụ theo Định lý hội tụ của [Zhang et al., 2024].
>
> Định lý hội tụ mang lại ba takeaway quan trọng: thứ nhất, độ chính xác không tăng mãi mãi mà sẽ hội tụ ở một điểm giới hạn; thứ hai, weighted voting tốt hơn voting thường khi tích `v * g` phân bổ tổng khối lượng lớn hơn cho các câu trả lời đúng; thứ ba, để phá vỡ giới hạn hội tụ, bắt buộc phải cải thiện verifier `v` hoặc generator `g`.
>
> Parallel meta-generators explore output space bằng cách sinh full sequences, đem lại large performance gains trong thực tế, nhưng bị giới hạn bởi evaluator và generator. Insight quan trọng là verifier chỉ được dùng ở cuối, trên full sequences. Câu hỏi tiếp theo là liệu ta có thể tận dụng intermediate evaluation tốt hơn không.
>
> Reward model là cầu nối giữa probability và acceptability. Trong Best-of-N, generator tạo nhiều candidates, còn reward model xếp hạng chúng. Nếu reward model phản ánh acceptability tốt, tăng `N` giúp tìm candidate tốt hơn. Nhưng nếu reward model imperfect, hệ thống có thể tối ưu quá mức theo reward model thay vì theo acceptability thật; đây là ý `over-optimization` trong slide.
>
> Voting và weighted voting giải thích một dạng aggregation khác: không chỉ hỏi sequence nào có score cao nhất, mà hỏi answer nào được nhiều paths ủng hộ. Trong reasoning tasks, nhiều solution paths khác nhau có thể dẫn tới cùng một answer. Self-consistency tận dụng điều đó bằng cách marginalize out paths `z` và chọn answer được hỗ trợ mạnh nhất.

### Scene 3.3 - Tree search, PRM và Rebase
**Thời lượng:** 68:30-77:00  
**Slide:** 126-135

**Visual 3Blue1Brown:**
- Outline slide 126 nhấn `Tree search`.
- Dựng cây trạng thái: node `s`, cạnh `s -> s'`, điểm `v(s)`.
- Bảng design choices: `States s`, `Transitions s -> s'`, `Scores v(s)`, `Strategy (breadth-first, depth-first, ...)`.
- PRM: một solution path `s1, s2, ..., st` đi vào process reward model và trả score trong `[0,1]`: `v(x, s_1, s_2, ..., s_t) -> [0, 1]` (Citations: [Uesato et al., 2022, Lightman et al., 2024, Wang et al., 2024a]).
- Rebase: frontier node nhận budget theo softmax của score; chỉ dùng công thức slide 130.
- Aggregation: tree search sinh candidates rồi đưa vào voting; highlight `intermediate states`, `backtracking`, `exploration`.
- Examples: `Go [Silver et al., 2016]`, `Proofs [Polu and Sutskever, 2020]`, `Agents [Koh et al., 2024]`.

**Công thức/keyword được phép:**
```tex
v(x,s_1,s_2,\ldots,s_t)\to[0,1]
```
```tex
\mathrm{explore}_i=\mathrm{Round}\left(\mathrm{Budget}\frac{\exp(v(s_i)/\tau)}{\sum_j\exp(v(s_j)/\tau)}\right)
```
Citations: `[Uesato et al., 2022]`, `[Lightman et al., 2024]`, `[Wang et al., 2024a]`, `[Silver et al., 2016]`, `[Polu and Sutskever, 2020]`, `[Koh et al., 2024]`.

**Voiceover:**
> Tree search giả định generation process có thể decomposed thành search over states và transitions. Khi dùng tree search, ta phải chọn states `s`, transitions `s -> s'`, scores `v(s)`, và strategy như breadth-first hoặc depth-first.
>
> Với các bài toán toán học và lập luận phức tạp, một cách để chấm điểm cho từng bước trung gian là Process Reward Model (PRM) gán nhãn đúng sai cho từng bước `v(x, s_1, s_2, ..., s_t) -> [0, 1]`, dựa trên các nghiên cứu nền tảng của [Uesato et al., 2022], [Lightman et al., 2024] và [Wang et al., 2024a].
>
> Reward Balanced Search, hay Rebase, dùng score để phân bổ exploration budget cho frontier. Công thức trong slide phân bổ budget theo softmax của `v(si)/tau`. Node có score cao được cấp nhiều exploration hơn; node score thấp được cấp ít hoặc không được mở rộng.
>
> Sau tree search, ta có thể lấy candidates để aggregate, ví dụ voting. Key idea là tree search tận dụng scores trên intermediate states, có backtracking và exploration. Tuy vậy, tree-search meta-generators yêu cầu environment phù hợp, decomposition thành states, và reward signal tốt.
>
> Khác biệt lớn giữa parallel generation và tree search nằm ở thời điểm dùng evaluation. Parallel generation thường đợi đến khi có full sequence rồi mới dùng verifier hoặc reward model. Tree search dùng score ngay trên intermediate states. Nhờ vậy nó có thể dừng một nhánh xấu sớm, quay lui, hoặc phân bổ thêm budget cho nhánh hứa hẹn.
>
> Chúng ta cũng cần cảnh báo tree search không phải lúc nào cũng phù hợp. Nếu tác vụ không decomposable thành states, nếu environment không cung cấp intermediate information, hoặc nếu reward signal kém, tree search có thể không đem lại lợi ích tương xứng với chi phí.

### Scene 3.4 - Refinement và self-correction
**Thời lượng:** 77:00-86:30  
**Slide:** 136-153

**Visual 3Blue1Brown:**
- Outline slide 136 nhấn `Refinement/self-correction`.
- Một draft output đi vào vòng feedback rồi thành improved generation.
- Split screen feedback source: `Extrinsic` và `Intrinsic`.
- Extrinsic: external program verifier (`16 [Aggarwal et al., 2024], AlphaVerus. P . Aggarwal, B. Parno, S. Welleck. 81`), demo code, và success cases: verifiers (`• Verifiers [Aggarwal et al., 2024]`), code interpreters (`• Code interpreters [Chen et al., 2024b]`), retrievers (`• Retrievers [Asai et al., 2024]`), tools + agent environment.
- Intrinsic prompted: re-prompt same model (e.g. [Madaan et al., 2023] hay `Re-prompt a single LLM, e.g. [Madaan et al., 2023]`); hiển thị mixed results (positive on easy tasks `• Easy to evaluate tasks: positive [Wang et al., 2024b]` or missing info `• E.g., missing info [Asai et al., 2024]`), và highlight: `17E.g., [Huang et al., 2024] Large Language Models Cannot Self-Correct Reasoning Yet` cùng `Takeaway: feedback is too noisy From [Huang et al., 2024]`.
- Toy slide 148: `Generate "TAYLORSWIFT"`, generator `p(character)`, feedback incorrect characters, corrector regenerate incorrect.
- Trained corrector (như `17[Welleck et al., 2023], Generating Sequences by Learning to [Self-]Correct .`): collect `(bad, better)` pairs, `• Update corrector pθ(better|bad) using the collected data` (Slide 150-151), repeat; warning `Prone to behavior collapse`, remedy: `• [Kumar et al., 2024]: overcome with regularization + RL` (`18E.g., Self-corrective learning [Welleck et al., 2023], SCoRe [Kumar et al., 2024].` - Slide 150-151).
- Summary slide 153: extrinsic positive with environments detecting/localizing errors; intrinsic prompted mixed; intrinsic trained possible but requires training strategies.

**Công thức/keyword được phép:**
```tex
p_\theta(\mathrm{better}\mid \mathrm{bad})
```
Citations: `[Aggarwal et al., 2024]`, `[Chen et al., 2024b]`, `[Asai et al., 2024]`, `[Madaan et al., 2023]`, `[Wang et al., 2024b]`, `[Huang et al., 2024]`, `[Welleck et al., 2023]`, `[Kumar et al., 2024]`, `16 [Aggarwal et al., 2024], AlphaVerus. P . Aggarwal, B. Parno, S. Welleck. 81`, `• Verifiers [Aggarwal et al., 2024]`, `• Code interpreters [Chen et al., 2024b]`, `• Retrievers [Asai et al., 2024]`, `Re-prompt a single LLM, e.g. [Madaan et al., 2023]`, `• Easy to evaluate tasks: positive [Wang et al., 2024b]`, `• E.g., missing info [Asai et al., 2024]`, `17E.g., [Huang et al., 2024] Large Language Models Cannot Self-Correct Reasoning Yet`, `Takeaway: feedback is too noisy From [Huang et al., 2024]`, `17[Welleck et al., 2023], Generating Sequences by Learning to [Self-]Correct .`, `• Update corrector pθ(better|bad) using the collected data`, `Prone to behavior collapse`, `• [Kumar et al., 2024]: overcome with regularization + RL`, `18E.g., Self-corrective learning [Welleck et al., 2023], SCoRe [Kumar et al., 2024].`.

**Voiceover:**
> Refinement và self-correction cải thiện một generation bằng feedback. Trong thực tế, quality và source của feedback là crucial. Chúng ta phân biệt extrinsic feedback và intrinsic feedback.
>
> Extrinsic feedback cung cấp thông tin bên ngoài tại inference time, ví dụ external program verifier như AlphaVerus ([Aggarwal et al., 2024]). Slide liệt kê các thành công nhờ tích hợp verifiers ([Aggarwal et al., 2024]), code interpreters ([Chen et al., 2024b]), retrievers ([Asai et al., 2024]), cùng các công cụ trong môi trường agent. Trực giác là external feedback mang lại thông tin mới chưa có trong mô hình để phát hiện và định vị lỗi (detect/localize errors).
>
> Intrinsic feedback (phản hồi nội tại) không sử dụng thông tin bên ngoài lúc inference. Phương thức phổ biến là prompted-based re-prompting trên chính LLM đó, ví dụ như Self-Refine ([Madaan et al., 2023]). Kết quả của hướng đi này khá trái chiều: có phản hồi tích cực ở các tác vụ dễ đánh giá ([Wang et al., 2024b]) hoặc thiếu thông tin ([Asai et al., 2024]), nhưng với suy luận toán học thì kết quả rất hạn chế. Chúng ta cần nhấn mạnh phát hiện cốt lõi từ nghiên cứu của [Huang et al., 2024] rằng "Large Language Models Cannot Self-Correct Reasoning Yet" vì feedback nội tại thường quá nhiễu (feedback is too noisy).
>
> Hướng thứ hai là học một bộ sửa lỗi nội tại (intrinsic trained corrector), ví dụ như Self-corrective learning ([Welleck et al., 2023]). Quy trình tổng quát là thu thập các cặp dữ liệu `(bad, better)` thông qua việc sinh mẫu và đánh giá reward, sau đó cập nhật bộ sửa lỗi `pθ(better | bad)` trên dữ liệu đã thu thập, rồi lặp lại. Phương pháp này rất dễ bị sụp đổ hành vi (behavior collapse); thuật toán SCoRe của [Kumar et al., 2024] đã giải quyết bằng cách áp dụng regularization kết hợp học tăng cường (RL). Summary: extrinsic feedback hoạt động tốt khi môi trường định vị được lỗi; prompted intrinsic cho kết quả lẫn lộn; trained intrinsic có triển vọng nhưng đòi hỏi chiến lược huấn luyện rất cụ thể.
>
> Từ `feedback` trong refinement cần được giải thích rõ. Feedback extrinsic có thể cung cấp thông tin mới mà model không tự có, ví dụ một verifier hoặc code interpreter phát hiện lỗi. Feedback intrinsic thì dựa vào chính mô hình, nên rủi ro là mô hình vừa tạo lỗi vừa không đánh giá đúng lỗi của mình.
>
> Toy example `Generate TAYLORSWIFT` cho thấy refinement ở dạng đơn giản: generator sinh từng character, feedback chỉ ra incorrect characters, corrector regenerate phần sai. Ví dụ này giúp người xem hiểu vì sao feedback localize error quan trọng: nếu biết sai ở đâu, quá trình sửa dễ hơn nhiều so với chỉ biết toàn bộ output chưa tốt.

### Scene 3.5 - Scaling meta-generators và compute allocation
**Thời lượng:** 86:30-94:00  
**Slide:** 154-164

**Visual 3Blue1Brown:**
- Outline slide 154 nhấn `Scaling meta-generators`.
- Một budget meter `C` chia vào ba knob: model size `N`, generated tokens `T`, inference strategy `S`.
- Frontier plot từ slide 157: điểm xanh `compute-optimal frontier`.
- Question 1: small model + more generations vs large model + fewer generations.
- Question 2: compute-optimal meta-generation strategy; highlight result slide 161: `Tree search (Rebase) can be compute-optimal [Wu et al., 2024b]`.
- Recap slide 162-163 bằng cards: performance improves with compute, but depends on model size and strategy; smaller models sometimes better [Wu et al., 2024b]; strategies can be combined/mixed; choose based on task performance and cost.
- Transition slide 164: many tokens, diverse ways, how do we do this quickly and efficiently?

**Công thức/keyword được phép:**
```tex
\arg\min_{N,T,S}\; \mathrm{error}(N,T,S)\quad \text{s.t.}\quad \mathrm{cost}(N,T,S)=C
```
Citations: `[Wu et al., 2024b]`.

**Voiceover:**
> Sau khi giới thiệu các strategy, chúng ta chuyển sang câu hỏi scaling: làm thế nào allocate test-time compute? Ta chọn strategy dựa trên task performance và compute cost. Cost là function của model size và number of generated tokens.
>
> Với compute budget `C`, bài toán compute-optimal inference là chọn `N`, `T`, `S` để minimize error, subject to `cost(N,T,S)=C`. Ở đây `N` là number of model parameters, `T` là number of generated tokens, `S` là inference strategy, và cost được tính bằng floating-point operations (FLOP).
>
> Câu hỏi thứ nhất: tốt hơn nên dùng small model và more generations, hay large model và fewer generations? Slide nêu rằng các mô hình nhỏ hơn có thể tối ưu hơn về mặt chi phí (smaller models can be compute optimal) dựa theo kết quả nghiên cứu của [Wu et al., 2024b]. Câu hỏi thứ hai: meta-generation strategy nào compute-optimal? Slide chỉ ra rằng tree search, cụ thể là Rebase, có thể compute-optimal [Wu et al., 2024b].
>
> Recap của phần meta-generation: performance improves với increased compute, nhưng phụ thuộc vào model size và meta-generator. Optimal model size và strategy thay đổi theo compute budget; đôi khi smaller models tốt hơn. Mục tiêu dài hạn là design strategies that are universally optimal. Vì các meta-generators sinh nhiều tokens và theo nhiều cách đa dạng như tree search, phần tiếp theo hỏi: làm sao sinh nhanh và hiệu quả?
>
> Khái niệm compute-optimal frontier nên được giải thích như tập các configuration không bị dominated: với cùng cost, chúng có error tốt hơn; hoặc với cùng error, chúng dùng ít cost hơn. Vì vậy câu hỏi không chỉ là `dùng model lớn nhất có thể`, mà là chọn model size, number of generated tokens, và strategy sao cho phù hợp budget.
>
> Đây cũng là điểm nối sang systems efficiency. Nếu hai meta-generators dùng cùng token budget nhưng một phương pháp parallelizable và prefix-shareable hơn, chi phí thực tế và latency có thể rất khác. Do đó cost-performance tradeoff phải xét cả algorithm lẫn cách hệ thống thực thi algorithm đó.

---

## CHƯƠNG 4 - EFFICIENT META-GENERATION

### Scene 4.1 - Efficiency basics, hardware, batching và KV cache
**Thời lượng:** 94:00-103:00  
**Slide:** 165-179

**Visual 3Blue1Brown:**
- Mở title `Efficient meta-generation`.
- Ba mục scope slide 166: basics of efficient generation, make meta-generation faster, which meta-generators are most efficient.
- Hai đồng hồ đo: `Latency` và `Throughput`; thêm tam giác trade-off với `Quality` đúng slide 168.
- Hardware diagram: VRAM, processor, memory bandwidth, FLOP/s, `• Communication Speeds (GB/s)` (Slide 171), and H100 SXM specs card (`23H100 SXM: BF16 dense tensor core max FLOP/s ≈ 1× 1015 FLOP/s, Memory bandwidth` `≈ 3.35× 1012 byte/s. ≫ 100 FLOP/byte is “free”!` - Slide 172).
- Bottleneck cards: loading activations, loading weights, performing computation, communicating across devices.
- Time model slide 172: operation time là max giữa compute time và memory transfer time, với công thức `(FLOP per second) · (total operation FLOP)` ở Slide 178-179.
- Batching: nhiều inputs gom lại và computed simultaneously; nhấn `cost-free for memory-bound operations`.
- KV cache: prefill stage xử lý prompt all at once; decode stage dùng cached K/V và append new K,V.
- Single-token optimization slides 176-179:
  - Giảm memory bandwidth: weight/activation quantization, model compression/distillation.
  - Tăng FLOP/s: FlashAttention [Dao et al., 2022] (performs same operations but improves utilization).
  - Giảm FLOP: `FLOP ↓: reduce operations required` (Slide 179) với Mixture-of-Experts (MoE) (`dense models [Fedus et al., 2022] 111` - Slide 179) (fewer FLOPs per token).

**Công thức/keyword được phép:**
```tex
\mathrm{Time}=\max\left(\frac{\mathrm{Operation\ FLOP}}{\mathrm{Device\ FLOP/s}},\frac{\mathrm{Data\ Transferred\ (GB)}}{\mathrm{Memory\ Bandwidth\ (GB/s)}}\right)
```
```tex
\mathrm{Size}=(\mathrm{batch}\cdot n_{ctx})\cdot(2\cdot n_{layer}\cdot n_{heads}\cdot head_{dim})\cdot n_{bytes}
```
Citations: `[Dao et al., 2022]`, `[Fedus et al., 2022]`, `• Communication Speeds (GB/s)`, `23H100 SXM: BF16 dense tensor core max FLOP/s ≈ 1× 1015 FLOP/s, Memory bandwidth`, `≈ 3.35× 1012 byte/s. ≫ 100 FLOP/byte is “free”!`, `(FLOP per second) · (total operation FLOP)`, `FLOP ↓: reduce operations required`, `dense models [Fedus et al., 2022] 111`.

**Voiceover:**
> Phần efficiency chuyển từ thuật toán sang hệ thống. Scope gồm basics of efficient generation, cách làm meta-generation faster, và câu hỏi meta-generators nào efficient nhất.
>
> Efficiency được đo bằng latency và throughput. Latency là người dùng phải chờ bao lâu cho response; throughput là bao nhiêu requests hoàn thành mỗi giây. Latency, throughput và quality thường trade off với nhau ở một budget nhất định.
>
> Hardware ảnh hưởng tới generation efficiency qua ba yếu tố: dung lượng dữ liệu trên thiết bị (on-device memory/VRAM), số phép tính trên giây (FLOP/s), và tốc độ truyền dữ liệu (Memory Bandwidth, GB/s). Các bottleneck bao gồm: loading inputs/activations, loading weights, performing computation, và communicating across devices.
>
> Chúng ta mô hình hóa time per operation bằng công thức `Time = max(Operation FLOP / Device FLOP/s, Data Transferred / Memory Bandwidth)`. Lấy ví dụ với NVIDIA H100 SXM, sức mạnh tính toán BF16 dense tensor core đạt tới 1x10^15 FLOP/s, trong khi băng thông bộ nhớ là 3.35x10^12 byte/s. Tỷ lệ này cho thấy nếu một phép toán thực hiện trên 100 FLOP/byte thì chi phí tính toán gần như là "miễn phí" so với chi phí truyền dữ liệu!
>
> Với single decoding step, các hướng tối ưu là giảm memory bandwidth (bằng cách quantization, distillation), tăng FLOP/s (bằng FlashAttention [Dao et al., 2022] giúp tăng hiệu suất sử dụng phần cứng dù số phép toán không đổi), hoặc giảm FLOP (bằng Mixture-of-Experts [Fedus et al., 2022] sử dụng ít FLOP hơn cho mỗi token so với mô hình dense).
>
> Compute-bound nghĩa là thời gian chủ yếu bị giới hạn bởi số phép tính có thể thực hiện mỗi giây. Memory-bound nghĩa là processor có thể tính nhanh hơn, nhưng phải chờ dữ liệu được chuyển từ memory. Công thức `Time = max(...)` trong slide cho thấy operation time bị chi phối bởi nhánh chậm hơn giữa compute và memory transfer.
>
> Batching đặc biệt quan trọng vì nhiều decoding operations memory-bound. Nếu đã phải tải weights từ memory, ta muốn dùng cùng lần tải đó cho nhiều inputs cùng lúc. Đó là lý do slide nói batching có thể gần như cost-free cho memory-bound operations.
>
> KV cache giải quyết một vấn đề khác: tránh tính lại keys và values cho toàn bộ prefix ở mỗi bước decode. Prefill tạo cache cho prompt, còn decode chỉ thêm K,V của token mới. Visual nên làm rõ rằng KV cache giảm repeated computation, nhưng bản thân cache cũng tiêu VRAM, nên nó trở thành một bottleneck khi batch hoặc context length lớn.

### Scene 4.2 - Speculative decoding
**Thời lượng:** 103:00-108:00  
**Slide:** 180-184

**Visual 3Blue1Brown:**
- Mở `How to speed up a single generation?`.
- Chuỗi long output `... The cow jumped over the moon . <EOS>` chạy tuần tự để cho thấy next-token prediction bottleneck.
- Draft model nhỏ tạo `N proposal tokens` rẻ; main generator kiểm tra song song.
- Dòng token được chia màu: proposals accepted giữ lại; mismatched tokens discarded (mô phỏng Speculative Decoding theo [Xia et al., 2024]).
- Slide 184: biểu đồ throughput/latency theo context length của MagicDec giữ nguyên nội dung nguồn, không thêm số liệu.

**Công thức/keyword được phép:** Không dùng công thức acceptance tự thêm nếu không lấy từ slide chính. Code chi tiết chỉ dùng ở Appendix slides 212-214. Citations: `[Xia et al., 2024]`.

**Voiceover:**
> Generation của long outputs bị bottleneck bởi sequential next-token prediction. Nhưng không phải token nào cũng khó như nhau. Câu hỏi của slide là: làm thế nào spend less time on easier tokens?
>
> Speculative decoding dùng một smaller draft model để tạo guesses cho `N` token tiếp theo một cách rẻ. Sau đó các proposal tokens này được truyền song song vào main generator để thẩm định, được mô tả chi tiết trong công trình của [Xia et al., 2024]. Những token khớp với prediction của main generator được giữ lại, còn token không khớp bị discard.
>
> Chúng ta cần nhấn mạnh decoding thường memory-bound. Speculative decoding có thể harm throughput ở low context, nhưng cải thiện cả throughput và latency ở long context lengths, theo kết quả MagicDec trong slide.
>
> Khái niệm cần truyền tải là speculative decoding chuyển một phần công việc tuần tự thành công việc song song. Thay vì main model phải sinh từng token một, draft model đề xuất nhiều token trước. Main model sau đó kiểm tra các proposal này cùng lúc. Nếu các token dễ đoán, nhiều proposal được giữ lại và hệ thống tiết kiệm được nhiều bước decode tuần tự.
>
> Nhưng slide cũng cảnh báo không phải lúc nào speculative decoding cũng tốt. Ở low context, overhead của draft model và verification có thể làm throughput xấu đi. Ở long context lengths, memory-bound decode nặng hơn, nên lợi ích của việc kiểm tra nhiều proposal song song rõ hơn.

### Scene 4.3 - KV cache reuse, prefix sharing, KV cache compression và recap, takeaways
**Thời lượng:** 108:00-120:00  
**Slide:** 185-205

**Visual 3Blue1Brown:**
- Mở `How to speed up meta-generation?`.
- Shared prefix prompt xuất hiện nhiều lần trong parallel generation; các bản sao KV cache dư thừa được tô đỏ.
- PagedAttention (`PagedAttention [Kwon et al., 2023] prevents redundant storage costs by` `mapping KV cache blocks to physical “pages” of VRAM` - Slide 188).
- Multi-level prefix sharing: long few-shot prompt + Best-of-N generation; vẽ cây prefix nhiều tầng (`• Long inputs can be amortized via Prefix Sharing of KV Cache` - Slide 200).
- RadixAttention: `RadixAttention enables complex prefix sharing patterns [Zheng et al., 2024],` quản lý cache dưới dạng Radix tree; LRU eviction khi memory cần giải phóng.
- Hydragen: `Hydragen [Juravsky et al., 2024] makes shared-prefix attention components` đi qua Tensor Cores; không thêm công thức ngoài slide.
- KV cache compression [Adams et al., 2024]: ba hướng `Token Dropping`, `Quantization`, `Architectural Modification`.
- Với token dropping, quantization, MQA/GQA, luôn hiển thị lại cùng công thức size từ slide 193-195 để cho thấy mỗi hướng tác động vào thành phần nào.
- Architectural tweaks: `Architectural tweaks such as Multi-Query Attention [Shazeer, 2019] or` `Grouped-Query Attention [Ainslie et al., 2023] reduce the number of Key +` Value heads (Slide 195).
- Recap slide 196: meta-generators efficient nếu `Parallelizable` và `• Prefix-shareable: long inputs are presented as identical shared` (Slide 196); token budget không phải indicator duy nhất (Citations: `[Aggarwal et al., 2024], AlphaVerus. P . Aggarwal, B. Parno, S. Welleck.` - Slide 201).
- Trình bày bảng so sánh hiệu năng tổng kết (Slide 196):
  - Chained: Parallelizable (No), Prefix-shareable (No)
  - Parallel: Parallelizable (Yes), Prefix-shareable (Yes)
  - Tree Search: Parallelizable (Semi), Prefix-shareable (Yes)
  - Refinement: Parallelizable (No), Prefix-shareable (No)
- Hiển thị các hướng đi tương lai (Looking Ahead) (Slide 197-205): hybrid meta-generators, learning to search, agent environments, compute allocation.
- Survey paper slide 204: tên paper, authors, TMLR 2024, arXiv URL.
- Thank you slide 205: đúng URL `https://cmu-l3.github.io/neurips2024-inference-tutorial`.

**Công thức/keyword được phép:**
```tex
(\mathrm{batch}\cdot n_{ctx})\cdot(2\cdot n_{layer}\cdot n_{heads}\cdot head_{dim})\cdot n_{bytes}
```
Citations: `[Kwon et al., 2023]`, `[Zheng et= al., 2024]`, `[Juravsky et al., 2024]`, `[Adams et al., 2024]`, `[Shazeer, 2019]`, `[Ainslie et al., 2023]`, `PagedAttention [Kwon et al., 2023] prevents redundant storage costs by`, `mapping KV cache blocks to physical “pages” of VRAM`, `• Long inputs can be amortized via Prefix Sharing of KV Cache`, `RadixAttention enables complex prefix sharing patterns [Zheng et al., 2024],`, `Hydragen [Juravsky et al., 2024] makes shared-prefix attention components`, `Architectural tweaks such as Multi-Query Attention [Shazeer, 2019] or`, `Grouped-Query Attention [Ainslie et al., 2023] reduce the number of Key +`, `• Prefix-shareable: long inputs are presented as identical shared`, `[Aggarwal et al., 2024], AlphaVerus. P . Aggarwal, B. Parno, S. Welleck.`.

**Voiceover:**
> Với meta-generation, câu hỏi là meta-generators tương tác với real-world efficiency và hardware utilization như thế nào, và làm sao thiết kế meta-generators efficient hơn.
>
> Common deployment và parallel generation thường có redundant shared prefix content trong prompts. PagedAttention trong vLLM tránh redundant storage bằng cách map KV cache blocks tới physical pages của VRAM.
>
> KV cache reuse không chỉ giới hạn ở một shared prefix. Multiple levels of prefix sharing có thể xuất hiện, ví dụ long few-shot prompt kết hợp Best-of-N generation. RadixAttention trong SGLang hỗ trợ complex prefix sharing patterns và evict least-recently-used KV cache blocks khi cần.
>
> Hydragen làm shared-prefix attention components nhanh hơn bằng cách leveraging Tensor Cores. Phần KV cache compression nhấn mạnh KV cache size là bottleneck cho larger batches và longer context inference. Ba hướng là token dropping, quantization và architectural modification. Architectural tweaks như Multi-Query Attention hoặc Grouped-Query Attention giảm số Key + Value attention heads để thu nhỏ KV cache.
>
> Recap của slide 196: meta-generators efficient nếu trajectories có thể chạy parallel và long inputs có thể prefix-share để reuse KV caches. Token budget không phải indicator duy nhất của meta-generator efficiency.
>
> Prefix sharing xuất hiện tự nhiên trong meta-generation. Ví dụ Best-of-N dùng cùng prompt để sinh nhiều candidates; tree search có nhiều nhánh chia sẻ cùng prefix; chatbot hoặc few-shot prompting có phần system prompt dài giống nhau. Nếu mỗi request lưu riêng KV cache cho prefix giống nhau, VRAM bị lãng phí.
>
> PagedAttention giải quyết redundant storage ở mức memory pages. RadixAttention mở rộng ý tưởng đó cho nhiều cấp prefix sharing bằng cây prefix. Hydragen tập trung vào làm phần attention trên shared prefix nhanh hơn, tận dụng Tensor Cores. Ba kỹ thuật này cùng truyền một thông điệp: cấu trúc của prompt và meta-generator có thể tạo ra cơ hội tối ưu hệ thống.
>
> Với KV cache compression, mỗi hướng tác động vào một biến trong công thức size. Token dropping giảm effective context length, quantization giảm bytes, architectural modification giảm số Key/Value heads. Đây là lý do công thức size nên xuất hiện lặp lại trong visual để người xem thấy mỗi kỹ thuật giảm phần nào của bộ nhớ.
>
> Tổng kết lại, kịch bản chương trình gồm ba phần lớn: primitive generators sinh từng token một; meta-generators là cách gọi các generators; và efficient meta-generation giúp tối ưu hóa hệ thống phần cứng khi chạy các thuật toán đó.
>
> Để tối ưu hóa Meta-generation, chúng ta có nhiều chiến lược như chained, parallel, tree search hay refinement. Chúng ta phân bổ test-time compute để cải thiện performance và thiết kế dựa trên cost-performance trade-offs. Về mặt hệ thống, khả năng song song hóa (parallelizability) giúp giảm latency và tăng throughput. Cấu trúc câu nhắc và meta-generator quyết định phần lớn hiệu năng thực tế, vì vậy token budget chỉ là một sự đơn giản hóa.
>
> Hướng phát triển tương lai sẽ tập trung vào các hệ thống lai (hybrid systems) kết hợp song song và cải thiện tuần tự, học cách tự tìm kiếm (learning to search) với khả năng quay lui và tự sửa lỗi, tối ưu hóa agent để tương tác với môi trường bên ngoài, và tự động phân bổ compute linh hoạt. Slide kết thúc bằng lời khuyên: rất nhiều kết luận khoa học hiện nay chỉ dựa trên một vài tác vụ thử nghiệm và giới thiệu tài liệu tham khảo "From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models" tại trang web cmu-l3.github.io/neurips2024-inference-tutorial.
>
> Câu `Science: many conclusions are based on a few tasks` cần được giữ trong voice vì nó là cảnh báo quan trọng của chúng ta. Các kỹ thuật meta-generation cho thấy nhiều kết quả mạnh, nhưng mức độ tổng quát của kết luận vẫn phụ thuộc vào tasks, evaluator, generator và budget được thử nghiệm. Vì vậy phần looking ahead không chỉ là danh sách hướng nghiên cứu, mà còn là lời nhắc rằng lĩnh vực này cần thêm bằng chứng rộng hơn.

---

## PANEL, APPENDIX VÀ REFERENCES

### Scene 5.1 - Panel session
**Thời lượng:** 120:00-127:00  
**Slide:** 206  
**Subtitle source:** đoạn panel cuối trong `Subtitle-lab1-ml-clean.txt`.

**Visual 3Blue1Brown:**
- Hiển thị slide panel đúng tên và affiliation:
  - Beidi Chen, CMU, `@BeidiChen`
  - Nouha Dziri, AI2, `@nouhadziri`
  - Rishabh Agarwal, DeepMind/McGill, `@agarwl_`
  - Jakob Foerster, Oxford/Meta AI, `@j_foerst`
  - Noam Brown, OpenAI, `@polynoamial`
  - Ilia Kulikov, Meta AI, moderator, `@uralik1`
- Dùng layout panel dạng các node người tham gia quanh một vòng tròn câu hỏi. Không thêm avatar/tổ chức ngoài slide.
- Ba cụm câu hỏi từ subtitle: future larger models vs inference-time algorithms; limits of inference scaling; efficiency/hardware/system co-design.
- Không hiển thị công thức mới trong panel.

**Công thức/keyword được phép:** Không có công thức mới.

**Voiceover:**
> Panel bắt đầu từ câu hỏi liệu các mô hình pretrained tốt hơn trong tương lai có làm mất nhu cầu về inference-time algorithms hay không. Nội dung subtitle cho thấy câu trả lời chung là các hướng này complementary. Nếu mô hình học được cách search tốt hơn trong training, ta có thể cần ít inference-time compute hơn, nhưng vẫn cần các algorithm ở inference để refine, extend capability, backtrack, evaluate hoặc dùng feedback.
>
> Câu hỏi tiếp theo là giới hạn của inference scaling. Panel phân biệt các domain có verification rõ như math và code với các domain khó hơn như writing, biology, drug discovery, hoặc các vấn đề ambiguity/correctness. Một bottleneck được nhắc tới là verifier quality: nếu không phân biệt được false positive và true positive, tăng compute không tự giải quyết vấn đề.
>
> Panel cũng nhắc đến các trường hợp verification có thể khó hơn generation, ví dụ kiểm chứng một chương trình an toàn với mọi input. Ngoài ra còn có câu hỏi liệu systems reasoning có giải quyết được các vấn đề xã hội rất phức tạp như poverty hay climate change không, và các giới hạn kiến trúc có thể liên quan đến state tracking hoặc sequence length.
>
> Phần efficiency của panel hỏi liệu còn không gian tối ưu trong architecture hiện tại hay chỉ chờ accelerator mới. Nội dung subtitle nêu hướng co-design giữa algorithm, modeling và hardware; phần cứng trước đây được thiết kế nhiều cho training, trong khi inference có thể trở thành phần lớn hơn của tổng compute. Các ý cuối gồm hybrid systems dùng code khi hữu ích, generative verifiers, inference scaling laws, và nhu cầu cộng đồng open source tập trung hơn vào công cụ cho hướng này.
>
> Một nuance quan trọng trong panel là inference-time algorithms không nhất thiết làm heavy lifting mãi mãi. Nếu mô hình tương lai học search tốt hơn trong training, inference-time algorithms có thể trở thành một lớp maintenance hoặc refinement nhẹ hơn. Nhưng panel vẫn xem chúng là cần thiết vì nhiều tác vụ cần feedback, backtracking, tool use hoặc evaluation tại thời điểm chạy.
>
> Về limits of inference scaling, panel nhấn mạnh sự khác nhau giữa tasks có outcome supervision rõ ràng và tasks mơ hồ hơn. Math và code dễ scale hơn vì có verifier hoặc test rõ. Writing, biology, drug discovery, societal issues, hoặc các bài toán cần human verification đắt đỏ thì khó hơn. Khi verification không dễ hơn generation, chỉ tăng sample hoặc compute không đủ.
>
> Về research direction, subtitle nhắc tới học search trong pretraining, self-improvement cho chain-of-thought, khả năng generalize downstream, và câu hỏi liệu reasoning đã học ở một độ dài nhất định có scale được tới context dài hơn không. Đây là các ý nên được visual hóa như các nhánh nghiên cứu chứ không trình bày thành kết luận chắc chắn.
>
> Ở phần systems, panel mở rộng từ software optimization sang hardware và hybrid architecture. Một hướng là co-design model, algorithm và hardware vì inference có thể chiếm phần lớn compute hơn trước. Một hướng khác là hệ thống lai biết dùng code hoặc tool khi đó là giải pháp efficient hơn, thay vì mọi thứ đều phải do LLM sinh token. Panel cũng nhắc tới generative verifiers: nếu verifier cũng là language model, ta có thể áp dụng inference-time compute cho verifier, dẫn tới tầng meta tiếp theo.



## Checklist kiểm soát nguồn cho khi dựng Manim

- Scene 2.1: chỉ dùng token-level generation, causal LM distribution `pθ[x_t | x_<t]`, decoding is search, và outline optimization/sampling/constrained. Không thêm nội dung kỹ thuật hoặc công thức ngoài nguồn.
- Scene 2.2: greedy/beam phải dùng đúng xác suất slide 34-41; không đổi `0.80` thành số khác; phải có `width-limited BFS`, `GPT2, beam size 2`, và note beam size 1 is greedy.
- Scene 2.3: atypicality chỉ dùng coin biased example trong slide; không thêm suy diễn xác suất hoặc số phần trăm nếu không có trong slide/subtitle.
- Scene 2.4: sampling/truncation/temperature chỉ dùng formulas và code trong slide 50, 55, 59, 61, 62; không thêm probability bar tự tạo.
- Scene 2.5: phải cover đủ sampling adapters table slide 66-68, constrained JSON slide 70-81, side effects slide 82, token healing slide 83-86, summary slide 87.
- Scene 3.1: phải có objective `arg max_G E A(y)`, formal meta-generator `G`, special case token generator `g`, và chain formulas.
- Scene 3.2: phải có Best-of-N formulas, reward model training, voting, weighted voting, convergence takeaways, và bounded-by-evaluator/generator summary.
- Scene 3.3: không dùng quote panel; chỉ tree search, PRM, Rebase, aggregation, examples Go/Proofs/Agents và requirements.
- Scene 3.4: phải có extrinsic/intrinsic/trained corrector, toy `TAYLORSWIFT`, `pθ(better|bad)`, behavior collapse, SCoRe regularization + RL.
- Scene 3.5: bắt buộc thêm vì slide 154-164 trước đây chưa có scene rõ: compute allocation, compute-optimal inference, smaller models, Rebase compute-optimal, recap.
- Scene 4.1: phải có latency/throughput/quality, hardware bottlenecks, time formula, batching, KV cache size formula, single-token optimizations.
- Scene 4.2: speculative decoding chỉ dùng nội dung slide 180-184; code chi tiết đưa vào Appendix A.2 nếu cần.
- Scene 4.3: phải có PagedAttention, RadixAttention, Hydragen, KV compression, token dropping, quantization, MQA/GQA, efficiency recap.
- Scene 4.4: phải có recap/takeaways, looking ahead, survey paper và đúng URL thank-you.
- Scene 5.1: panel chỉ dùng panelists từ slide 206 và ý chính từ subtitle panel; không gán quote nếu subtitle không rõ người nói.
