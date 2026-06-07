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
| Panel, appendix, references | 206-245 | 10:00 |
| Tổng | 1-245 | ~130:00 |

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
> Chúng ta bắt đầu với chủ đề chính của tutorial: các thuật toán sinh đầu ra bằng mô hình ngôn ngữ, đặc biệt là meta-generation algorithms cho large language models. Lý do chủ đề này quan trọng là cộng đồng đang tìm cách dùng thêm compute tại test time, sau khi mô hình đã được huấn luyện, để cải thiện chất lượng generation system.
>
> Mô hình ngôn ngữ có thể hỗ trợ nhiều tác vụ nếu tác vụ đó được biểu diễn như việc sinh một chuỗi: từ giải bài toán olympiad cho tới viết code. Vì vậy tutorial tập trung vào câu hỏi: khi đã có một language model, ta nên gọi nó, điều khiển nó, và kết hợp nó với các thành phần khác như thế nào để sinh kết quả tốt hơn?
>
> Trong subtitle, tác giả cũng đặt chủ đề này trong bối cảnh inference algorithms và LLM OS. Nghĩa là ta không chỉ xem language model như một hàm dự đoán token đơn lẻ, mà xem nó như một thành phần trong một hệ thống sinh hoàn chỉnh: hệ thống có thể gọi mô hình nhiều lần, dùng công cụ, dùng evaluator, và quyết định cách tiêu compute tại thời điểm sinh.

### Scene 1.2 - Ba hướng scale compute
**Thời lượng:** 02:00-04:20  
**Slide:** 5-7

**Visual 3Blue1Brown:**
- Dựng ba trục song song: `pretraining compute`, `post-training compute`, `test-time compute`.
- Trục pretraining: model lớn hơn, dataset lớn hơn; gắn `Scaling Laws for Neural Language Models [Kaplan et al., 2020]`.
- Trục post-training: các cặp `(input, output)` đi vào fine-tuning; gắn `Scaling Instruction-Finetuned Language Models [Chung et al., 2022]`.
- Trục test-time: mũi tên tăng compute tại generation time; gắn `Test-time compute vs. accuracy ([OpenAI, 2024])`.

**Công thức/keyword được phép:** `pretraining compute`, `post-training compute`, `test-time compute`.

**Voiceover:**
> Khi nhìn vào tiến bộ của language models, tutorial mô tả ba làn sóng scale. Làn sóng đầu tiên là scale pretraining compute: dùng mô hình lớn hơn và tập dữ liệu lớn hơn, với kết quả scaling laws cho neural language models.
>
> Làn sóng thứ hai là post-training compute: thu thập các cặp input-output, rồi fine-tune mô hình để làm tốt hơn trên các tác vụ và có thể generalize sang tác vụ mới.
>
> Làn sóng hiện tại là test-time scaling. Ta giữ mô hình đã huấn luyện, nhưng thiết kế phương pháp dùng thêm compute tại inference hoặc generation time để tăng performance.
>
> Điểm tác giả nhấn mạnh là hai làn sóng đầu, dù rất quan trọng, vẫn chưa đủ cho mọi tác vụ mà ta muốn language model làm. Vì vậy test-time scaling không thay thế pretraining hay post-training; nó là một chiều compute khác, được dùng sau khi mô hình đã tồn tại, ngay lúc hệ thống đang cần sinh câu trả lời.

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
> Có ba cách chính để dùng test-time compute. Thứ nhất, ta cho mô hình sinh thêm token, ví dụ chain-of-thought: mô hình viết các bước trung gian trước khi trả lời.
>
> Thứ hai, ta gọi generator nhiều lần. AlphaCode là ví dụ điển hình: hệ thống sinh rất nhiều chương trình, rồi lọc và gom nhóm để lấy một tập output nhỏ hơn.
>
> Thứ ba, ta chuyển từ một language model đơn lẻ sang compound AI system: mô hình có thể dùng evaluator, verifier, code interpreter, search engine hoặc công cụ bên ngoài. Đây là nền để định nghĩa meta-generation.
>
> Khi sinh thêm token, mỗi token tương ứng với một lần forward pass qua neural network, nên bản thân việc generate nhiều hơn đã là tiêu compute. Với chain-of-thought, compute đó được dùng để tạo intermediate thought tokens. Với repeated calls, compute được dùng để tạo nhiều candidates. Với compound AI system, một phần computation có thể được chuyển sang các tools đáng tin cậy hơn như code interpreter hoặc search engine.

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
> Tutorial gồm ba phần chính: primitive generators, meta-generators, và efficient meta-generation. Sau đó là panel session. Website của tutorial cung cấp slides, code examples và reading list.
>
> Từ `primitive` ở đây không có nghĩa là các phương pháp này không quan trọng. Trong subtitle, tác giả giải thích chúng là primitives theo nghĩa building blocks: các khối cơ bản để xây dựng những meta-generation algorithms phức tạp hơn. Vì vậy trước khi nói về meta-generator, ta phải hiểu cách một generator sinh một sequence đơn lẻ.

---

## CHƯƠNG 2 - PRIMITIVE GENERATORS

### Scene 2.1 - Token-level generation và decoding là search
**Thời lượng:** 10:00-16:30  
**Slide:** 23-31

**Visual 3Blue1Brown:**
- Mở với title `I. Primitive Generators` và subtitle `Generating one token at a time`.
- Chuỗi nguồn từ slide: `Taylor Alison Swift (born December 13, 1989) is`.
- Một hộp `LM` nhận prefix `x_<t` và xuất phân phối token: `an`, `a`, `the`, `best`, `one`, ...
- Token `an` được chọn rồi prefix cập nhật thành `... is an`; phân phối tiếp theo gồm `American`, `actress`, `English`, `actor`, `award`, ...
- Chuyển sang cây quyết định từ slide 30 cho `Taylor Swift is`: các nhánh `the`, `a`, `writer`, `singer`, `and`, `song`, `producer`, ...
- Kết bằng outline slide 31: `Optimization`, `Sampling`, `Constrained generation, structured outputs`.

**Công thức/keyword được phép:**
```tex
p_\theta[x_t \mid x_{<t}]
```

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
  - Greedy: `Taylor Swift is a former contestant on`; token prob: `0.023`, `0.022`, `0.80`, `0.0004`.
  - Non-greedy: `Taylor Swift is a singer , song`; token prob: `0.012`, `0.26`, `0.21`, `0.0007`.
- Beam search: vẽ cây width-limited BFS đúng nhánh slide 37-41, gồm `a`, `the`, `an`, `former`, `writer`, `latest`, `to`, `be`, `join`, `in`, `only`, `person`, `who`, `one` và các xác suất xuất hiện trong slide.
- Nhãn bắt buộc: `GPT2, beam size 2`; `Beam search with beam size 1 is greedy decoding`.

**Công thức/keyword được phép:**
```tex
\arg\max_x p_\theta[x]
```
```tex
x_t = \arg\max_x p_\theta[x \mid x_{<t}]
```

**Voiceover:**
> MAP decoding tìm chuỗi có xác suất cao nhất theo mô hình: `arg max_x pθ[x]`. Hai thuật toán optimization được giới thiệu là greedy decoding và beam search.
>
> Greedy decoding chọn token có xác suất cao nhất tại từng bước: `x_t = arg max_x pθ[x | x_<t]`. Nhưng greedy không đảm bảo tìm được chuỗi có xác suất cao nhất. Slide minh họa một chuỗi greedy với các token prob `0.023`, `0.022`, `0.80`, `0.0004`, và một chuỗi non-greedy có các token prob `0.012`, `0.26`, `0.21`, `0.0007`.
>
> Beam search là width-limited breadth-first search. Ở mỗi bước, nó giữ lại một số nhánh tốt nhất theo beam size, rồi tiếp tục mở rộng. Với GPT2 và beam size 2, cây tìm kiếm được prune theo width. Nếu beam size bằng 1, beam search chính là greedy decoding.
>
> Subtitle giải thích greedy giống một lựa chọn cục bộ: ở mỗi bước nó chọn token tốt nhất ngay lúc đó. Điều này đơn giản và rẻ, nhưng không bảo đảm tối ưu toàn chuỗi, vì chuỗi tốt hơn có thể bắt đầu bằng một token không phải token tốt nhất tại bước đầu.
>
> Beam search là điểm trung gian giữa greedy và exhaustive search. Exhaustive search sẽ mở rộng quá nhiều khả năng nên không feasible với language model có hàng chục hoặc hàng trăm nghìn token trong vocabulary. Beam search giữ lại một beam hữu hạn, vì vậy nó vẫn search qua nhiều nhánh hơn greedy nhưng kiểm soát được chi phí bằng beam size.

### Scene 2.3 - Lợi ích và cạm bẫy của MAP
**Thời lượng:** 23:00-28:30  
**Slide:** 42-47

**Visual 3Blue1Brown:**
- Mở bằng `Benefits of MAP`: closed-ended tasks như translation và question answering.
- Ba warning cards từ slide: `Repetition traps`, `Short sequences`, `Atypicality`.
- Repetition: hiển thị đúng đoạn GPT2 beam size 32 về Taylor Swift lặp `singer-songwriter`, `songwriter-songwriter`, `song-writer-songwriter`.
- Short sequence: so sánh xác suất đúng từ slide: `Pr[Taylor Swift is <eos>] > Pr[Taylor Swift is an American singer-…]`; remedy: `length normalization`.
- Atypicality: đồng xu lệch `Pr[H]=0.6`, `Pr[T]=0.4`; outcome 100 heads là most likely nhưng atypical.
- Kết luận slide 47: approximate MAP, ví dụ narrow beam search, works better than exact MAP.

**Công thức/keyword được phép:**
```tex
Pr[H] = 0.6,\quad Pr[T] = 0.4
```
```tex
Pr[\text{Taylor Swift is <eos>}] > Pr[\text{Taylor Swift is an American singer-...}]
```

**Voiceover:**
> MAP decoding hoạt động tốt cho các tác vụ closed-ended như translation và question answering. Nhưng probability maximization cũng gây ra nhiều decoding problems.
>
> Cạm bẫy đầu tiên là repetition traps. Với GPT2 và beam size 32, output có thể lặp các cụm như `singer-songwriter`, `songwriter-songwriter`, và `song-writer-songwriter`. Remedies trong slide là repetition penalty và unlikelihood training.
>
> Cạm bẫy thứ hai là short sequences: một chuỗi kết thúc sớm bằng `<eos>` có thể có xác suất cao hơn một câu dài đầy đủ hơn. Remedy được nêu là length normalization.
>
> Cạm bẫy thứ ba là atypicality. Với đồng xu lệch `Pr[H]=0.6`, `Pr[T]=0.4`, outcome có xác suất cao nhất cho 100 lần tung là toàn heads, nhưng outcome đó lại atypical. Tương tự, most likely generation có thể không phải generation tự nhiên. Takeaway của tác giả: approximate MAP, chẳng hạn narrow beam search, có thể tốt hơn exact MAP.
>
> Ý chính của đoạn này là `most likely` không đồng nghĩa với `best` cho mọi loại generation. Trong closed-ended tasks, MAP thường hữu ích vì output space bị ràng buộc và có đáp án rõ. Nhưng với open-ended text generation, cực đại hóa xác suất có thể đẩy mô hình vào output lặp, quá ngắn, hoặc không điển hình. Vì vậy tác giả dùng các pitfalls này để chuyển từ optimization sang sampling.

### Scene 2.4 - Sampling, truncation và temperature
**Thời lượng:** 28:30-38:30  
**Slide:** 48-65

**Visual 3Blue1Brown:**
- Mở slide `Sampling` và `Objective: Sampling`, với settings sampling từ modern LLM APIs.
- Ancestral sampling: các token `y1`, `y2`, `y3` được sinh tuần tự từ phân phối điều kiện.
- So sánh ba cột từ slide 52-54: `Greedy (repetition trap)`, `Ancestral (incoherent)`, `Top-k (acceptable)` với đúng đoạn Taylor Swift trong slide.
- Truncation table slide 55: `Top-k`, `Top-p`, `epsilon`, `eta`, `Min-p` và threshold strategy tương ứng.
- Biểu đồ logprob từ slide 56-58 cho hai prefix `Taylor Swift` và `My name`; overlay `Top-k = 5`, `Top-p = 0.9`.
- Temperature: ba panel `tau=0.5`, `tau=1`, `tau=2`; không thêm giá trị xác suất ngoài slide.
- Code panels từ slide 61-62: `Sampling implementations`, `vLLM`, `HuggingFace`.
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
> Bây giờ objective chuyển sang sampling. Ancestral sampling sinh từng token bằng cách lấy mẫu từ phân phối điều kiện của mô hình. Điều này tương đương với sequence sampling theo tích các xác suất điều kiện.
>
> Vấn đề là greedy decoding gây repetition traps, còn ancestral sampling có thể gây incoherence. Lý do tác giả nêu là low-probability tokens are too likely: phân phối có heavy tail. Giải pháp là chop off the tail.
>
> Truncation sampling nằm giữa greedy và ancestral sampling bằng cách chọn threshold xác suất ở mỗi time step. Slide liệt kê Top-k, Top-p, epsilon, eta và Min-p. Temperature không trực tiếp cắt đuôi mà làm phân phối peaked hơn hoặc phẳng hơn: high tau đa dạng hơn nhưng dễ incoherent; low tau coherent hơn nhưng dễ repetitive.
>
> Phần implementation dùng đúng code trong slide cho greedy, ancestral, top-k, top-p, epsilon, temperature, và các framework như vLLM và HuggingFace. Tác giả kết thúc bằng ba lý do heavy-tail: under-training, mode-seeking của cross-entropy loss, và low-rank constraints trên output của LLM.
>
> Khi giải thích Top-k và Top-p, cần nhấn mạnh sự khác biệt về threshold. Top-k luôn giữ đúng k token có xác suất cao nhất, nên nó không tự thích nghi với hình dạng phân phối. Top-p dùng cumulative probability, nên vùng được giữ có thể co giãn theo phân phối. Đây là lý do slide đặt Top-k và Top-p cạnh nhau trên hai prefix `Taylor Swift` và `My name`.
>
> Temperature là một adapter khác với truncation: nó không quyết định token nào bị cắt, mà rescale logits trước khi lấy mẫu. Vì vậy trong visual, temperature nên được thể hiện bằng phân phối trở nên peaked hơn hoặc gần uniform hơn, còn truncation nên được thể hiện bằng vùng token được giữ lại để sample.

### Scene 2.5 - Sampling adapters, constrained decoding và token healing
**Thời lượng:** 38:30-46:00  
**Slide:** 66-87

**Visual 3Blue1Brown:**
- Mở bằng bảng `Sampling adapters`: phân phối `pθ(. | x)` đi qua adapter rồi thành phân phối đã re-adjust.
- Hiển thị đủ các method trong bảng slide 66-68: Ancestral, Temperature, Greedy, Top-k, Nucleus, Typical, Epsilon, eta, Mirostat, Basis-aware, Contrastive, DExperts, Inference-time adapters, Proxy tuning.
- Constrained decoding: prompt JSON Taylor Swift, schema `name: string`, `birth year: int`, output sai schema từ LLM.
- State machine slide 73-81: các node `start`, `{`, `"name"`, `[A-Za-z]`, `"birth year"`, `\d`, `}`.
- Tại mỗi bước, bảng GPT2 token probability chỉ hiển thị đúng các token/prob trong slide: `\n 0.36`, `" 0.16`, `{ 0.026`, `https 0.025`; `name 0.31`, `date 0.069`; `Taylor 0.85`; `1989 0.020`; `} 0.34`, v.v.
- Side effects slide 82: `Generation speedup`, `Reduced performance`.
- Token healing slide 83-86: `The url is http:` rồi `://`, candidates `s://`, `://`; không thêm tokenizer ví dụ ngoài slide.
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

**Voiceover:**
> Sampling adapter nhận phân phối token `pθ(. | x)` và điều chỉnh lại xác suất. Truncation và temperature là adapters, nhưng bảng của tác giả còn liệt kê nhiều phương pháp khác như typical sampling, epsilon, eta, Mirostat, basis-aware sampling, contrastive decoding, DExperts, inference-time adapters và proxy tuning. Với các công thức, chỉ dùng đúng các biểu thức trong bảng slide.
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
- System designer chọn một hệ thống `G`; bên cạnh là evaluator `A(y)` cho acceptability.
- External information: evaluator `v(y) ≈ A(y)`, với các tên tương đương: critic, verifier, value, reward model, scoring model.
- Oracle verifier loop từ slide 95: `z ~ pθ(z|x)`, `y ~ pθ(y|x,z)`, stop nếu verifier nói answer correct.
- Formalization slide 97: meta-generator gọi nhiều generators `g1, g2, ..., gG` và parameters `φ`.
- Token-level generator special case slide 98.
- Chain slides 100-106: `y1`, `y2`, `y3`; chain-of-thought; self-ask; DSP; examples System-2 Attention và Draft-Sketch-Prove.

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
```tex
y_1\sim g_1(x),\quad y_2\sim g_2(x,y_1),\quad y_3\sim g_3(x,y_2)
```

**Voiceover:**
> Mục tiêu của system designer là thiết kế một hệ thống `G` sinh ra acceptable sequences. Slide viết mục tiêu là tối ưu kỳ vọng acceptability `A(y)` trên output của `G`. Acceptability có thể là correctness hoặc human preferences.
>
> Ta đã biết cách sample probable outputs từ `pθ(y|x)`, nhưng nếu các output probable đó không acceptable thì cần thêm chiến lược. Ý tưởng đầu tiên của meta-generation là tận dụng external information trong generation, ví dụ học một evaluator `v(y) ≈ A(y)` và dùng nó khi sinh. Tác giả dùng các tên gần tương đương: evaluator, critic, verifier, value, reward model, scoring model.
>
> Ý tưởng thứ hai là gọi generator nhiều hơn một lần để search for good sequences. Với oracle verifier, ta có thể lặp: sinh intermediate `z`, sinh answer `y`, rồi dừng khi verifier nói answer correct.
>
> Formalization của slide là `y ~ G(y|x; g1, g2, ..., gG, φ)`. Design choices gồm strategy `G`, lựa chọn generators `g1...gG`, và các parameter khác như number of tokens. Token-level generators ở phần trước là special case: `y ~ g(y|x; pθ, φ)`.
>
> Chaining compose generators theo thứ tự: `y1 ~ g1(x)`, `y2 ~ g2(x,y1)`, `y3 ~ g3(x,y2)`. Chain-of-thought là ví dụ: generate thought `z`, rồi generate answer `a`. Chaining có thể mở rộng sang self-ask, API calls, language model programs, System-2 Attention, Draft-Sketch-Prove. Takeaway: chaining decompose generation và incorporate tools/models, nhưng chaining alone không explore output space.
>
> Điểm quan trọng của acceptability là nó không nhất thiết trùng với probability của mô hình. Một output có thể probable theo `pθ` nhưng không correct, không được con người thích, hoặc không đáp ứng yêu cầu của hệ thống. Meta-generation được đưa vào để tìm cách sinh ra sequences acceptable hơn, bằng cách dùng evaluator, verifier, tool, hoặc bằng cách gọi generator nhiều lần.
>
> Với chain-of-thought, subtitle nhấn mạnh đây là một decomposition đơn giản nhưng có tác động sâu: hệ thống cho phép sinh một intermediate thought `z`, rồi dùng `z` để sinh answer `a`. Slide cũng nói chain-of-thought tăng expressivity vì output length có thể biến đổi, tương tự một writable tape. Khi dựng visual, nên thể hiện chain như một chương trình nhiều bước: outer function là meta-generator, inner calls là generators hoặc tools.

### Scene 3.2 - Parallel generation, Best-of-N, voting và weighted voting
**Thời lượng:** 57:00-68:30  
**Slide:** 108-125

**Visual 3Blue1Brown:**
- Nhiều candidate `y(1)...y(N)` sinh song song từ `G(.|x)`.
- Aggregator `h` nhận toàn bộ candidates và trả `y`.
- Best-of-N: các candidates đi qua reward model `v(y) -> [0,1]`, candidate điểm cao nhất sáng lên.
- Reward model training: hai slide riêng cho correct/incorrect examples và preference data.
- Đồ thị over-optimization từ slide 115 giữ dạng slide, không thêm số liệu mới.
- Voting/self-consistency: nhiều solution path hội tụ về answer `a`; answer có nhiều vote nhất được chọn.
- Weighted voting: vote được nhân bởi reward model score `v(y(i))`.
- Convergence theorem slide 119-122: hiển thị công thức và ba takeaway.
- Kết slide 124-125: parallel meta-generators explore output space bằng full sequences, large gains, bounded by evaluator/generator quality, verifier chỉ dùng ở cuối.

**Công thức/keyword được phép:**
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

**Voiceover:**
> Parallel meta-generators sinh nhiều candidates song song: `{y(1), ..., y(N)} ~ G(.|x)`, rồi aggregate thành output cuối cùng bằng `h`.
>
> Best-of-N hay rejection sampling chọn candidate có reward model score cao nhất. Reward model `v(y) -> [0,1]` có thể được train bằng correct và incorrect examples, hoặc bằng preference data. Best-of-N approximates maximum acceptability: khi số generations `N` tăng, approximation tới `arg max_y v(y)` tốt hơn; nhưng nếu reward model imperfect thì có over-optimization.
>
> Voting aggregation chọn answer nhận nhiều vote nhất. Weighted voting thêm reward model score vào vote. Slide nêu rằng voting có thể outperform Best-of-N trong một số ví dụ, và khi `N -> infinity`, voting accuracy converges tới biểu thức marginalize out paths `z`.
>
> Ba takeaway của theorem: accuracy không cải thiện mãi với nhiều samples mà eventually converges; weighted voting tốt hơn voting khi `v · g` gán nhiều total mass hơn cho correct answers; muốn cải thiện thêm thì cần improve reward model `v` hoặc generator `g`.
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
- PRM: một solution path `s1, s2, ..., st` đi vào process reward model và trả score trong `[0,1]`.
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

**Voiceover:**
> Tree search giả định generation process có thể decomposed thành search over states và transitions. Khi dùng tree search, ta phải chọn states `s`, transitions `s -> s'`, scores `v(s)`, và strategy như breadth-first hoặc depth-first.
>
> Với math problems, một cách score node là process reward model, hay PRM. PRM nhận input và chuỗi bước trung gian `s1, s2, ..., st`, rồi trả điểm trong `[0,1]`.
>
> Reward Balanced Search, hay Rebase, dùng score để phân bổ exploration budget cho frontier. Công thức trong slide phân bổ budget theo softmax của `v(si)/tau`. Node có score cao được cấp nhiều exploration hơn; node score thấp được cấp ít hoặc không được mở rộng.
>
> Sau tree search, ta có thể lấy candidates để aggregate, ví dụ voting. Key idea là tree search tận dụng scores trên intermediate states, có backtracking và exploration. Tuy vậy, tree-search meta-generators yêu cầu environment phù hợp, decomposition thành states, và reward signal tốt.
>
> Khác biệt lớn giữa parallel generation và tree search nằm ở thời điểm dùng evaluation. Parallel generation thường đợi đến khi có full sequence rồi mới dùng verifier hoặc reward model. Tree search dùng score ngay trên intermediate states. Nhờ vậy nó có thể dừng một nhánh xấu sớm, quay lui, hoặc phân bổ thêm budget cho nhánh hứa hẹn.
>
> Tác giả cũng cảnh báo tree search không phải lúc nào cũng phù hợp. Nếu tác vụ không decomposable thành states, nếu environment không cung cấp intermediate information, hoặc nếu reward signal kém, tree search có thể không đem lại lợi ích tương xứng với chi phí.

### Scene 3.4 - Refinement và self-correction
**Thời lượng:** 77:00-86:30  
**Slide:** 136-153

**Visual 3Blue1Brown:**
- Outline slide 136 nhấn `Refinement/self-correction`.
- Một draft output đi vào vòng feedback rồi thành improved generation.
- Split screen feedback source: `Extrinsic` và `Intrinsic`.
- Extrinsic: external program verifier, AlphaVerus, tutorial code demo URL, và danh sách success cases: verifiers, code interpreters, retrievers, tools + agent environment.
- Intrinsic prompted: re-prompt same model; hiển thị mixed results, feedback too noisy.
- Toy slide 148: `Generate "TAYLORSWIFT"`, generator `p(character)`, feedback incorrect characters, corrector regenerate incorrect.
- Trained corrector: collect `(bad, better)` pairs, update `pθ(better|bad)`, repeat; warning `behavior collapse`, remedy `[Kumar et al., 2024]: regularization + RL`.
- Summary slide 153: extrinsic positive with environments detecting/localizing errors; intrinsic prompted mixed; intrinsic trained possible but requires training strategies.

**Công thức/keyword được phép:**
```tex
p_\theta(\mathrm{better}\mid \mathrm{bad})
```

**Voiceover:**
> Refinement và self-correction cải thiện một generation bằng feedback. Trong thực tế, quality và source của feedback là crucial. Tác giả phân biệt extrinsic feedback và intrinsic feedback.
>
> Extrinsic feedback là external information tại inference time, ví dụ external program verifier. Slide nêu AlphaVerus, tutorial code demo, và các success cases như verifiers, code interpreters, retrievers, tools plus agent environment. Trực giác là external feedback thêm thông tin mới và có thể detect hoặc localize errors.
>
> Intrinsic feedback không dùng external information tại inference time. Một cách là re-prompt cùng một LLM, như Self-Refine. Kết quả mixed: một số task dễ evaluate có kết quả positive, nhưng mathematical reasoning mixed; takeaway từ slide là feedback too noisy.
>
> Trường hợp intrinsic trained corrector học trực tiếp để correct. General pattern là collect `(bad, better)` pairs bằng generating và evaluating reward, update corrector `pθ(better|bad)` bằng collected data, rồi repeat. Phương pháp này prone to behavior collapse; SCoRe vượt qua bằng regularization và RL. Summary: extrinsic thường tốt khi environment detect/localize errors; intrinsic prompted mixed; intrinsic trained có thể cải thiện nhưng cần training strategies cụ thể.
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
- Frontier plot từ slide 157: điểm xanh `compute-optimal frontier`; không tự thêm số liệu.
- Question 1: small model + more generations vs large model + fewer generations.
- Question 2: compute-optimal meta-generation strategy; highlight result slide 161: `Tree search (Rebase) can be compute-optimal`.
- Recap slide 162-163 bằng cards: performance improves with compute, but depends on model size and strategy; smaller models sometimes better; strategies can be combined/mixed; choose based on task performance and cost.
- Transition slide 164: many tokens, diverse ways, how do we do this quickly and efficiently?

**Công thức/keyword được phép:**
```tex
\arg\min_{N,T,S}\; \mathrm{error}(N,T,S)\quad \text{s.t.}\quad \mathrm{cost}(N,T,S)=C
```

**Voiceover:**
> Sau khi giới thiệu các strategy, tác giả chuyển sang câu hỏi scaling: làm thế nào allocate test-time compute? Ta chọn strategy dựa trên task performance và compute cost. Cost là function của model size và number of generated tokens.
>
> Với compute budget `C`, bài toán compute-optimal inference là chọn `N`, `T`, `S` để minimize error, subject to `cost(N,T,S)=C`. Ở đây `N` là number of model parameters, `T` là number of generated tokens, `S` là inference strategy, và cost được tính bằng floating-point operations.
>
> Câu hỏi thứ nhất: tốt hơn nên dùng small model và more generations, hay large model và fewer generations? Slide nêu rằng smaller models can be compute optimal trong kết quả của Wu et al. Câu hỏi thứ hai: meta-generation strategy nào compute-optimal? Slide nêu rằng tree search, cụ thể Rebase, can be compute-optimal.
>
> Recap của phần meta-generation: performance improves with increased compute, nhưng phụ thuộc vào model size và meta-generator. Optimal model size và strategy thay đổi theo compute budget; đôi khi smaller models tốt hơn. Mục tiêu dài hạn là design strategies that are universally optimal. Vì các meta-generators sinh nhiều tokens và theo nhiều cách đa dạng như tree search, phần tiếp theo hỏi: làm sao sinh nhanh và hiệu quả?
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
- Hardware diagram: VRAM, processor, memory bandwidth, FLOP/s, on-device memory.
- Bottleneck cards: loading activations, loading weights, performing computation, communicating across devices.
- Time model slide 172: operation time là max giữa compute time và memory transfer time.
- Batching: nhiều inputs gom lại và computed simultaneously; nhấn `cost-free for memory-bound operations`.
- KV cache: prefill stage xử lý prompt all at once; decode stage dùng cached K/V và append new K,V.
- Single-token optimization slides 176-179: reduce memory bandwidth, improve FLOP/s, reduce FLOP; examples quantization/compression/distillation, FlashAttention, MoE.

**Công thức/keyword được phép:**
```tex
\mathrm{Time}=\max\left(\frac{\mathrm{Operation\ FLOP}}{\mathrm{Device\ FLOP/s}},\frac{\mathrm{Data\ Transferred\ (GB)}}{\mathrm{Memory\ Bandwidth\ (GB/s)}}\right)
```
```tex
\mathrm{Size}=(\mathrm{batch}\cdot n_{ctx})\cdot(2\cdot n_{layer}\cdot n_{heads}\cdot head_{dim})\cdot n_{bytes}
```

**Voiceover:**
> Phần efficiency chuyển từ thuật toán sang hệ thống. Scope gồm basics of efficient generation, cách làm meta-generation faster, và câu hỏi meta-generators nào efficient nhất.
>
> Efficiency được đo bằng latency và throughput. Latency là người dùng phải chờ bao lâu cho response; throughput là bao nhiêu requests hoàn thành mỗi giây. Latency, throughput và quality thường trade off với nhau ở một budget nhất định.
>
> Hardware ảnh hưởng tới generation efficiency qua ba câu hỏi: giữ được bao nhiêu data on-device trong VRAM, device thực hiện bao nhiêu operations mỗi giây, và mất bao lâu để gửi operands từ HBM đến processor. Các bottleneck gồm loading inputs, loading weights, performing computation, và communication across devices.
>
> Slide mô hình hóa time per operation bằng max giữa compute time và memory transfer time. Operations có thể compute-bound hoặc memory-bound. Batching cho phép nhiều inputs computed simultaneously và có thể cost-free với memory-bound operations.
>
> KV cache tách inference thành prefill và decode. Prefill xử lý prompt all at once và giữ keys/values để initialize KV cache. Decode dùng cached KV values cho timestep hiện tại và append K,V mới. Kích thước KV cache theo công thức trong slide phụ thuộc batch, context length, layers, heads, head dimension và bytes.
>
> Với single decoding step, các hướng tối ưu là giảm memory bandwidth, tăng FLOP/s, hoặc giảm FLOP. Slide nêu quantize weights/activations, compress/distill model, FlashAttention, và Mixture-of-Experts.
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
- Dòng token được chia màu: proposals accepted giữ lại; mismatched tokens discarded.
- Slide 184: biểu đồ throughput/latency theo context length của MagicDec giữ nguyên nội dung nguồn, không thêm số liệu.

**Công thức/keyword được phép:** Không dùng công thức acceptance tự thêm nếu không lấy từ slide chính. Code chi tiết chỉ dùng ở Appendix slides 212-214.

**Voiceover:**
> Generation của long outputs bị bottleneck bởi sequential next-token prediction. Nhưng không phải token nào cũng khó như nhau. Câu hỏi của slide là: làm thế nào spend less time on easier tokens?
>
> Speculative decoding dùng một smaller draft model để tạo guesses cho `N` token tiếp theo một cách rẻ. Sau đó các proposal tokens này được truyền song song vào main generator. Những token khớp với prediction của main generator được giữ lại, còn token không khớp bị discard.
>
> Tác giả nhấn mạnh decoding thường memory-bound. Speculative decoding có thể harm throughput ở low context, nhưng cải thiện cả throughput và latency ở long context lengths, theo kết quả MagicDec trong slide.
>
> Khái niệm cần truyền tải là speculative decoding chuyển một phần công việc tuần tự thành công việc song song. Thay vì main model phải sinh từng token một, draft model đề xuất nhiều token trước. Main model sau đó kiểm tra các proposal này cùng lúc. Nếu các token dễ đoán, nhiều proposal được giữ lại và hệ thống tiết kiệm được nhiều bước decode tuần tự.
>
> Nhưng slide cũng cảnh báo không phải lúc nào speculative decoding cũng tốt. Ở low context, overhead của draft model và verification có thể làm throughput xấu đi. Ở long context lengths, memory-bound decode nặng hơn, nên lợi ích của việc kiểm tra nhiều proposal song song rõ hơn.

### Scene 4.3 - KV cache reuse, prefix sharing và KV cache compression
**Thời lượng:** 108:00-116:30  
**Slide:** 185-196

**Visual 3Blue1Brown:**
- Mở `How to speed up meta-generation?`.
- Shared prefix prompt xuất hiện nhiều lần trong parallel generation; các bản sao KV cache dư thừa được tô đỏ.
- PagedAttention: các logical blocks map vào physical pages trong VRAM; shared prefix trỏ chung page.
- Multi-level prefix sharing: long few-shot prompt + Best-of-N generation; vẽ cây prefix nhiều tầng.
- RadixAttention: Radix tree quản lý cache; LRU eviction khi memory cần giải phóng.
- Hydragen: shared-prefix attention components đi qua Tensor Cores; không thêm công thức ngoài slide.
- KV cache compression: ba hướng `Token Dropping`, `Quantization`, `Architectural Modification`.
- Với token dropping, quantization, MQA/GQA, luôn hiển thị lại cùng công thức size từ slide 193-195 để cho thấy mỗi hướng tác động vào thành phần nào.
- Recap slide 196: meta-generators efficient nếu `Parallelizable` và `Prefix-shareable`; token budget không phải indicator duy nhất.

**Công thức/keyword được phép:**
```tex
(\mathrm{batch}\cdot n_{ctx})\cdot(2\cdot n_{layer}\cdot n_{heads}\cdot head_{dim})\cdot n_{bytes}
```

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

### Scene 4.4 - Recap, takeaways, looking ahead và thank you
**Thời lượng:** 116:30-120:00  
**Slide:** 197-205

**Visual 3Blue1Brown:**
- Slide 197 `Recap and takeaways`.
- Ba khối của tutorial xuất hiện: Primitive generators, Meta-generators, Efficient meta-generation.
- Takeaways meta-generators: chained, parallel, tree search, refinement; spend test-time compute; use cost-performance tradeoffs.
- Takeaways efficient meta-generation: parallelizability, prefix sharing KV cache, prompt design và meta-generator structure ảnh hưởng efficiency.
- Looking ahead: hybrid meta-generators, learning to search, agent environments, compute allocation; warning science conclusions based on few tasks.
- Survey paper slide 204: tên paper, authors, TMLR 2024, arXiv URL.
- Thank you slide 205: đúng URL `https://cmu-l3.github.io/neurips2024-inference-tutorial`.

**Công thức/keyword được phép:** Không có công thức mới.

**Voiceover:**
> Recap của tutorial gồm ba phần: primitive generators sinh từng token một; meta-generators là strategies for calling generators; efficient meta-generation là sinh nhanh và hiệu quả.
>
> Takeaway về meta-generators: có nhiều strategy như chained, parallel, tree search, refinement. Chúng spend test-time compute để cải thiện performance, và cần dùng cost-performance tradeoffs để choose hoặc design phương pháp.
>
> Takeaway về efficiency: parallelizability giảm latency và tăng throughput; long inputs có thể được amortized bằng prefix sharing của KV cache; prompt design và meta-generator structure có thể thay đổi efficiency thực tế đáng kể. Token budget có thể là oversimplification.
>
> Looking ahead gồm hybrid meta-generators, learning to search như explore, backtrack, self-correct, agent environments, và câu hỏi allocate compute. Tác giả cũng nhấn mạnh rằng nhiều kết luận khoa học hiện dựa trên chỉ một vài tasks. Tutorial dựa trên survey paper `From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models`, TMLR 2024. Kết thúc bằng trang thank you và URL tutorial.
>
> Câu `Science: many conclusions are based on a few tasks` cần được giữ trong voice vì nó là cảnh báo quan trọng của tác giả. Các kỹ thuật meta-generation cho thấy nhiều kết quả mạnh, nhưng mức độ tổng quát của kết luận vẫn phụ thuộc vào tasks, evaluator, generator và budget được thử nghiệm. Vì vậy phần looking ahead không chỉ là danh sách hướng nghiên cứu, mà còn là lời nhắc rằng lĩnh vực này cần thêm bằng chứng rộng hơn.

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

### Appendix A.1 - Pairwise MBR và liên hệ với weighted voting
**Thời lượng:** 127:00-128:30  
**Slide:** 207-211

**Visual 3Blue1Brown:**
- Slide 207 `Appendix` dùng như transition.
- Slides 208-209: candidate set `{y(1),...,y(N)}` nằm trên vòng tròn; mỗi candidate được so với các candidate khác bằng utility `v(y,y(i))`.
- Slide 210: chart AlpacaEval 2.0 win rate giữ nguyên dạng slide; không thêm số liệu ngoài slide.
- Slide 211: weighted voting được diễn giải như instance của MBR, với utility bằng indicator same answer nhân sequence score.

**Công thức/keyword được phép:**
```tex
\mathrm{MBR}(g,v,N)=\arg\max_{y\in\{y^{(1)},\ldots,y^{(N)}\}}\frac{1}{N}\sum_{i=1}^N v(y,y^{(i)})
```
```tex
\frac{1}{N}\sum_{i=1}^N v(y,y^{(i)})\approx \mathbb{E}_{y'\sim p}[v(y,y')]
```
```tex
v(y,y^{(i)})=\mathbf{1}[a=a^{(i)}]\cdot v(y^{(i)}),\quad y=(z,a),\; y^{(i)}=(z^{(i)},a^{(i)})
```

**Voiceover:**
> Appendix bổ sung phần pairwise aggregation bằng Minimum Bayes Risk. MBR chọn candidate có consensus utility cao nhất so với các candidates còn lại. Candidate set được sample từ generator `g`, và `v(y,y')` là utility function.
>
> Slide cũng cho ví dụ dùng LLM utility trên AlpacaEval 2.0 và liên hệ weighted voting với MBR. Weighted voting là một instance của MBR khi utility bằng indicator cùng answer nhân với sequence score.
>
> Khái niệm `consensus utility` ở đây khác với Best-of-N thông thường. Best-of-N hỏi candidate nào có score độc lập cao nhất. Pairwise MBR hỏi candidate nào được các candidate khác hỗ trợ nhiều nhất theo utility function. Vì vậy MBR là một cách aggregate dựa trên quan hệ giữa candidates, không chỉ dựa trên score đơn lẻ của từng candidate.

### Appendix A.2 - Code examples cho speculative decoding
**Thời lượng:** 128:30-129:30  
**Slide:** 212-214

**Visual 3Blue1Brown:**
- Slide 212 `Code examples`.
- Slides 213-214 hiển thị code block đúng nội dung, highlight từng phần:
  - `speculative_decode(...)`
  - `generate(drf_m, tok, gen, spec_size, t)`
  - `tgt_lprob = tgt_m(spec_id)`
  - `compute_ll_rejs(...)`
  - `compute_adjusted_dist(...)`
- Không diễn giải thành công thức acceptance mới ngoài code.

**Công thức/code được phép:**
```python
def speculative_decode(tgt_m, drf_m, tok, inp: torch.Tensor, max_tok: int, n_spec: int = 5, t: float = 1.0):
    gen = inp
    max_len = inp.shape[1] + max_tok
    while gen.shape[1] < max_len:
        tok_left = max_len - gen.shape[1]
        spec_size = min(n_spec, tok_left - 1)
        if spec_size > 0:
            spec_id, spec_lprob = generate(drf_m, tok, gen, spec_size, t)
            tgt_lprob = tgt_m(spec_id)
            rejs = compute_ll_rejs(tgt_lprob, spec_lprob)
            if len(rejs) > 0:
                accepted = spec_id[:, :rejs[0]]
                adj_probs = compute_adjusted_dist(tgt_lprob, spec_lprob)
                next_tok = Categorical(adj_probs)
            else:
                accepted = spec_id
                next_tok = Categorical(tgt_lprob.exp())
            gen = torch.cat([gen, accepted, next_tok])
```
```python
def compute_ll_rejs(tgt_lprob: torch.Tensor, spec_lprob: torch.Tensor, spec_tok_id: torch.Tensor) -> torch.Tensor:
    llrs = tgt_lprob[spec_tok_id] - spec_lprob[spec_tok_id]
    uniform_lprobs = torch.log(torch.rand_like(llrs))
    rej_idx = torch.nonzero((llrs <= uniform_lprobs))
    return rej_idx

def compute_adjusted_dist(tgt_lprob: torch.Tensor, spec_lprob: torch.Tensor, rej_idx: torch.Tensor) -> torch.Tensor:
    adj_dist = torch.clamp(torch.exp(tgt_lprob[rej_idx]) - torch.exp(spec_lprob[rej_idx]), min=0)
    adj_dist = torch.div(adj_dist, adj_dist.sum())
    return adj_dist
```

**Voiceover:**
> Code examples trong appendix cho speculative decoding. Hàm chính giữ `gen`, tính `max_len`, chọn `spec_size`, dùng draft model để sinh speculative ids và log probabilities, rồi forward target model để lấy target log probabilities. Nếu có rejection, phần accepted lấy đến rejection đầu tiên và next token được sample từ adjusted distribution; nếu không có rejection, toàn bộ speculative ids được accepted.
>
> Hai helper functions trong slide tính rejection bằng log-likelihood ratio và tạo adjusted distribution bằng hiệu giữa target probability và speculative probability, clamp về không âm rồi normalize.
>
> Khi dựng video, phần code không cần giải thích như một tutorial PyTorch đầy đủ. Mục tiêu là liên hệ code với khái niệm ở Scene 4.2: draft model propose, target model verify, helper function tìm rejection, và adjusted distribution xử lý bước tiếp theo sau rejection. Không thêm công thức acceptance ngoài những gì code thể hiện.

### References roll
**Thời lượng:** 129:30-130:00  
**Slide:** 215-245

**Visual 3Blue1Brown:**
- Hiển thị `References i` đến `References xxxi` như credit/reference roll.
- Không đọc từng reference thành narration dài; các trang references là nguồn citation, không phải nội dung giảng mới.
- Có thể dùng layout grid 3x3 các thumbnail slide reference chạy từ page 215 đến 245, hoặc scroll dọc tốc độ vừa đủ để người xem thấy đây là bibliography.

**Công thức/keyword được phép:** Không có công thức mới.

**Voiceover:**
> Phần còn lại của PDF là danh mục references, từ `References i` đến `References xxxi`. Các references này là nguồn cho các paper và phương pháp đã được nhắc trong tutorial. Video kết thúc bằng reference roll thay vì biến danh mục này thành nội dung giảng mới.

---

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
- Appendix: slides 207-214 là appendix/code; slides 215-245 là references roll.
