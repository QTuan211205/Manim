import os
import tempfile

from manim import *

config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
config.max_files_cached = 10000


def create_text(text, font_size=24, font="Segoe UI", color=WHITE, **kwargs):
    base_size = 48
    scale_factor = font_size / base_size
    text_mob = Text(text, font_size=base_size, font=font, color=color, **kwargs)
    text_mob.scale(scale_factor)
    return text_mob


def create_markup_text(text, font_size=24, font="Segoe UI", **kwargs):
    base_size = 48
    scale_factor = font_size / base_size
    text_mob = MarkupText(text, font_size=base_size, font=font, **kwargs)
    text_mob.scale(scale_factor)
    return text_mob


def fit_mobject(mob, max_width=None, max_height=None):
    if max_width is not None and mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    if max_height is not None and mob.height > max_height:
        mob.scale_to_fit_height(max_height)
    return mob

class Scene5_1(Scene):
    def make_search_tree(self):
        root = Circle(radius=0.12, color=YELLOW, fill_opacity=0.85).move_to(UP * 0.45)
        root_label = create_text("Cây tìm kiếm", font_size=5.5, color=YELLOW).next_to(root, UP, buff=0.05)
        nodes = VGroup(root)
        edges = VGroup()
        for i, x in enumerate([-0.55, -0.18, 0.18, 0.55]):
            child = Circle(radius=0.08, color=GRAY_B, fill_opacity=0.75).move_to(RIGHT * x + DOWN * 0.05)
            edges.add(Line(root.get_center(), child.get_center(), color=GRAY_C, stroke_width=1.2))
            nodes.add(child)
            for j, dx in enumerate([-0.08, 0.08]):
                leaf = Circle(radius=0.055, color=GREEN, fill_opacity=0.65).move_to(RIGHT * (x + dx) + DOWN * 0.45)
                edges.add(Line(child.get_center(), leaf.get_center(), color=GRAY_D, stroke_width=0.9))
                nodes.add(leaf)
        return VGroup(edges, nodes, root_label).scale(0.82)

    def make_state_machine(self):
        title = create_text("Máy trạng thái ràng buộc", font_size=5.2, color=BLUE_A)
        states = VGroup()
        for i, label in enumerate(["S0", "S1", "S2"]):
            box = RoundedRectangle(width=0.45, height=0.28, corner_radius=0.04, color=BLUE_A, fill_color="#102035", fill_opacity=0.95)
            txt = create_text(label, font_size=5.5, color=WHITE).move_to(box.get_center())
            states.add(VGroup(box, txt))
        states.arrange(RIGHT, buff=0.3)
        arrows = VGroup(
            Arrow(states[0].get_right(), states[1].get_left(), color=BLUE_A, stroke_width=1.3, buff=0.04),
            Arrow(states[1].get_right(), states[2].get_left(), color=BLUE_A, stroke_width=1.3, buff=0.04),
        )
        title.next_to(states, UP, buff=0.12)
        return VGroup(title, states, arrows).scale(0.95)

    def make_conveyor(self):
        title = create_text("Băng chuyền đầu cơ", font_size=5.4, color=ORANGE)
        belt = RoundedRectangle(width=1.75, height=0.35, corner_radius=0.05, color=ORANGE, fill_color="#2a1b0f", fill_opacity=0.95)
        tokens = VGroup()
        for i, label in enumerate(["draft", "verify", "accept"]):
            tok = RoundedRectangle(width=0.42, height=0.22, corner_radius=0.035, color=ORANGE, fill_color="#3a2a12", fill_opacity=0.9)
            txt = create_text(label, font_size=3.5, color=WHITE).move_to(tok.get_center())
            tokens.add(VGroup(tok, txt))
        tokens.arrange(RIGHT, buff=0.1).move_to(belt.get_center())
        arrow = Arrow(LEFT * 0.9, RIGHT * 0.9, color=ORANGE, stroke_width=1.2).next_to(belt, DOWN, buff=0.05)
        title.next_to(belt, UP, buff=0.12)
        return VGroup(title, belt, tokens, arrow).scale(0.95)

    def make_kv_tree(self):
        title = create_text("Cây tiền tố KV Cache", font_size=5.3, color=GREEN)
        trunk = Line(UP * 0.35, DOWN * 0.2, color=GREEN, stroke_width=3)
        shared = create_text("shared prefix", font_size=4.5, color=GREEN_A).next_to(trunk, LEFT, buff=0.08)
        branches = VGroup()
        for y in [0.15, -0.1, -0.35]:
            branches.add(Line(DOWN * 0.1, RIGHT * 0.75 + UP * y, color=GREEN_A, stroke_width=1.5))
        leaves = VGroup(*[
            Circle(radius=0.05, color=GREEN_A, fill_opacity=0.85).move_to(RIGHT * 0.75 + UP * y)
            for y in [0.15, -0.1, -0.35]
        ])
        title.next_to(trunk, UP, buff=0.12)
        return VGroup(title, trunk, shared, branches, leaves).scale(1.0)

    def make_expert_card(self, name, org, handle, color):
        card = RoundedRectangle(width=2.15, height=1.15, corner_radius=0.06, color=color, fill_color="#181a1e", fill_opacity=0.96)
        avatar = Circle(radius=0.18, color=color, fill_color=color, fill_opacity=0.25).move_to(card.get_center() + UP * 0.25)
        initial = create_text(name[0], font_size=10, color=color).move_to(avatar.get_center())
        name_txt = create_text(name, font_size=6.1, color=WHITE).move_to(card.get_center() + DOWN * 0.04)
        org_txt = create_text(org, font_size=5.0, color=color).move_to(card.get_center() + DOWN * 0.22)
        handle_txt = create_text(handle, font_size=4.2, color=GRAY_B).move_to(card.get_center() + DOWN * 0.38)
        return VGroup(card, avatar, initial, name_txt, org_txt, handle_txt)

    def quote_box(self, speaker, text, color, height=1.45, y=0):
        box = RoundedRectangle(width=10.5, height=height, corner_radius=0.06, color=color, fill_color="#181a1e", fill_opacity=0.95)
        speaker_txt = create_markup_text(f"<b>{speaker}</b>", font_size=7.8, color=color)
        body = create_markup_text(text, font_size=6.3, color=WHITE, line_spacing=1.16)
        block = VGroup(speaker_txt, body).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fit_mobject(block, max_width=9.9, max_height=height - 0.22)
        block.move_to(box.get_center())
        return VGroup(box, block).move_to(UP * y)

    def construct(self):
        self.camera.background_color = "#111111"

        title = create_markup_text("<b>Kết luận &amp; Phiên thảo luận Panel</b>", font_size=21, color=YELLOW)
        subtitle = create_text("Kết luận và phiên thảo luận panel", font_size=10, color=GRAY_A)
        intro = VGroup(title, subtitle).arrange(DOWN, buff=0.16).move_to(ORIGIN)
        top_line = Line(LEFT * 4.5, RIGHT * 4.5, color=YELLOW, stroke_width=1.3).next_to(intro, UP, buff=0.32)
        bot_line = Line(LEFT * 4.5, RIGHT * 4.5, color=YELLOW, stroke_width=1.3).next_to(intro, DOWN, buff=0.32)
        self.play(Create(top_line), Create(bot_line), FadeIn(intro, shift=UP * 0.2), run_time=1.4)
        self.wait(4)

        header = create_text("Kết luận & Panel Session", font_size=12, color=YELLOW).to_edge(UP, buff=0.28)
        self.play(FadeOut(top_line), FadeOut(bot_line), ReplacementTransform(intro, header), run_time=1.0)
        self.wait(0.6)

        # Visual recap from the full video script: previous components assemble around the axis.
        axes = VGroup(
            Arrow(LEFT * 2.1, RIGHT * 2.1, color=GRAY_B, stroke_width=1.8),
            Arrow(DOWN * 1.35, UP * 1.35, color=GRAY_B, stroke_width=1.8),
            Line(LEFT * 1.25 + DOWN * 0.8, RIGHT * 1.25 + UP * 0.8, color=GRAY_D, stroke_width=1.4),
        ).move_to(ORIGIN)
        z_label = create_text("Z", font_size=9, color=GRAY_B).next_to(axes[1], UP, buff=0.08)
        recap_title = create_markup_text("<b>Hành trình đã đi qua</b>", font_size=13, color=YELLOW).move_to(UP * 2.25)
        journey = create_markup_text(
            "Bộ sinh token cơ bản  →  Meta-Generation tìm kiếm/tự sửa  →  Tối ưu hệ thống phần cứng",
            font_size=7.3,
            color=GRAY_A,
        ).move_to(DOWN * 2.2)

        search_tree = self.make_search_tree().move_to(LEFT * 4.1 + UP * 0.9)
        state_machine = self.make_state_machine().move_to(RIGHT * 4.1 + UP * 0.9)
        conveyor = self.make_conveyor().move_to(LEFT * 4.1 + DOWN * 0.8)
        kv_tree = self.make_kv_tree().move_to(RIGHT * 4.1 + DOWN * 0.8)
        components = VGroup(search_tree, state_machine, conveyor, kv_tree)
        targets = [
            LEFT * 1.65 + UP * 0.75,
            RIGHT * 1.65 + UP * 0.75,
            LEFT * 1.65 + DOWN * 0.75,
            RIGHT * 1.65 + DOWN * 0.75,
        ]

        self.play(FadeIn(recap_title), FadeIn(axes), FadeIn(z_label), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in components], lag_ratio=0.15), run_time=1.8)
        self.play(
            *[comp.animate.move_to(target).scale(0.92) for comp, target in zip(components, targets)],
            FadeIn(journey),
            run_time=2.0,
        )
        self.wait(13)
        self.play(FadeOut(recap_title), FadeOut(axes), FadeOut(z_label), FadeOut(components), FadeOut(journey), run_time=1.0)

        # Panel participants.
        panel_title = create_markup_text("<b>Phiên thảo luận Panel</b>", font_size=14, color=YELLOW).move_to(UP * 2.3)
        experts = VGroup(
            self.make_expert_card("Noam Brown", "OpenAI", "@polynoamial", "#FF6B6B"),
            self.make_expert_card("Rishabh Agarwal", "DeepMind/McGill", "@agarwl_", "#C780FF"),
            self.make_expert_card("Jakob Foerster", "Oxford/Meta AI", "@j_foerst", "#4D96FF"),
            self.make_expert_card("Beidi Chen", "CMU", "@BeidiChen", "#FFD93D"),
            self.make_expert_card("Nouha Dziri", "AI2", "@nouhadziri", "#6BCB77"),
            self.make_expert_card("Ilia Kulikov", "Meta AI | Moderator", "@uralik1", GRAY_A),
        ).arrange_in_grid(rows=2, cols=3, buff=0.26).move_to(UP * 0.25)
        self.play(FadeIn(panel_title), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in experts], lag_ratio=0.14), run_time=2.0)
        self.wait(11)
        self.play(FadeOut(panel_title), FadeOut(experts), run_time=1.0)

        question = create_markup_text(
            "<b>Câu hỏi lớn:</b>\nLiệu huấn luyện các mô hình lớn hơn có loại bỏ nhu cầu\nvề các giải thuật tìm kiếm Meta-Generation?",
            font_size=13,
            color=YELLOW,
            line_spacing=1.2,
        ).move_to(ORIGIN)
        self.play(Write(question), run_time=1.5)
        self.wait(8)
        self.play(FadeOut(question), run_time=0.8)

        nouha = self.quote_box(
            "Nouha Dziri (AI2)",
            "Không. Mô hình lớn hơn vẫn đối mặt với hai giới hạn cốt lõi:\n"
            "<b>1. Snowballing of error</b>: một lỗi nhỏ ban đầu làm lệch toàn bộ suy luận phía sau.\n"
            "<b>2. Difficulty of look-ahead</b>: khó nhìn trước hệ quả nhiều bước.",
            "#6BCB77",
            height=1.65,
            y=0.85,
        )
        structure = self.quote_box(
            "Vai trò của Meta-Generation",
            "Tìm kiếm cây, quay lui và đánh giá tiến trình PRM là lớp cấu trúc bổ sung\nđể mở rộng khả năng của mô hình.",
            GREEN,
            height=1.15,
            y=-1.0,
        )
        self.play(FadeIn(nouha, shift=RIGHT * 0.15), run_time=1.0)
        self.play(FadeIn(structure, shift=RIGHT * 0.15), run_time=1.0)
        self.wait(20)
        self.play(FadeOut(nouha), FadeOut(structure), run_time=0.9)

        noam = self.quote_box(
            "Noam Brown (OpenAI)",
            "\"Inference Compute là một ranh giới vô hạn.\"\n"
            "Một câu hỏi thường chỉ tốn một phần nhỏ của một xu; nhưng với bài toán quan trọng\n"
            "như giả thuyết Riemann hay phát hiện thuốc mới, người ta có thể trả hàng ngàn\n"
            "đến một triệu đô la cho câu trả lời chính xác.",
            "#FF6B6B",
            height=1.95,
            y=0.75,
        )
        scale = self.quote_box(
            "Góc nhìn kinh tế",
            "Khoảng cách 8 cấp độ quy mô là không gian lớn để tiếp tục mở rộng suy luận.",
            "#FF6B6B",
            height=0.95,
            y=-1.35,
        )
        self.play(FadeIn(noam, shift=RIGHT * 0.15), run_time=1.0)
        self.play(FadeIn(scale, shift=RIGHT * 0.15), run_time=0.8)
        self.wait(22)
        self.play(FadeOut(noam), FadeOut(scale), run_time=0.9)

        beidi = self.quote_box(
            "Beidi Chen (CMU)",
            "Phần lớn phần cứng GPU hiện nay được thiết kế cho huấn luyện nặng\n"
            "và suy luận giá rẻ. Khi chi phí suy luận chiếm phần lớn hơn,\n"
            "đồng thiết kế giữa thuật toán tìm kiếm và phần cứng GPU mở ra cơ hội tối ưu hóa lớn.",
            "#FFD93D",
            height=1.65,
            y=0.6,
        )
        cod = self.quote_box(
            "Algorithm-hardware co-design",
            "Mục tiêu là giảm giá thành suy luận và vận hành các hệ thống Meta-Generation hiệu quả hơn.",
            "#FFD93D",
            height=0.95,
            y=-1.2,
        )
        self.play(FadeIn(beidi, shift=RIGHT * 0.15), run_time=1.0)
        self.play(FadeIn(cod, shift=RIGHT * 0.15), run_time=0.8)
        self.wait(18)
        self.play(FadeOut(beidi), FadeOut(cod), run_time=0.9)

        final_box = RoundedRectangle(width=10.4, height=2.35, corner_radius=0.08, color=YELLOW, fill_color="#201c14", fill_opacity=0.95)
        final_text = create_markup_text(
            "<b>Tương lai của AI</b>\n\n"
            "Không chỉ nằm ở việc xây dựng các mô hình lớn hơn,\n"
            "mà nằm ở việc thiết kế các hệ thống thông minh\n"
            "biết cách suy nghĩ và phân bổ tài nguyên suy luận một cách tối ưu.\n\n"
            "Cảm ơn các bạn đã theo d�        self.wait(1.5)

        # =====================================================================
        # OUTRO CẢM ƠN KẾT THÚC TOÀN BỘ VIDEO
        # =====================================================================
        final_outro_box = RoundedRectangle(width=8.5, height=2.2, corner_radius=0.08, color=YELLOW, fill_color="#201c14", fill_opacity=0.95)
        final_outro_txt = create_markup_text(
            "<b>Cảm ơn các bạn đã theo dõi!</b>\n\n"
            "Hãy like và subscribe kênh để cập nhật thêm các bài học mới.\n"
            "Toàn bộ slide và mã nguồn được đính kèm bên dưới mô tả.",
            font_size=10.5, color=WHITE, line_spacing=1.3
        )
        final_outro_txt.move_to(final_outro_box.get_center())
        final_outro = VGroup(final_outro_box, final_outro_txt).move_to(ORIGIN)
        
        self.play(
            FadeIn(final_outro, shift=UP * 0.15),
            run_time=1.2
        )
        self.wait(5.0)
        self.play(FadeOut(final_outro), run_time=1.0)
        self.wait(1.5)ãy like và subscribe kênh để cập nhật thêm các bài học mới.\n"
            "Toàn bộ slide và mã nguồn được đính kèm bên dưới mô tả.",
            font_size=10.5, color=WHITE, line_spacing=1.3
        )
        final_outro_txt.move_to(final_outro_box.get_center())
        final_outro = VGroup(final_outro_box, final_outro_txt).move_to(ORIGIN)
        
        self.play(
            FadeOut(ref_title), FadeOut(ref_group),
            FadeIn(final_outro, shift=UP * 0.15),
            run_time=1.2
        )
        self.wait(5.0)
        self.play(FadeOut(final_outro), run_time=1.0)
        self.wait(1.5)

