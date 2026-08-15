from manim import *
import numpy as np


# ============================================================
# PART 6
#
# THE HYPOTENUSE IS NOT REALLY STRAIGHT
#
# Main question:
#
#       "Is that long edge really one straight line?"
#
# We investigate two apparently matching line segments.
#
# Segment A:
#
#       rise = 2
#       run  = 5
#
# Segment B:
#
#       rise = 3
#       run  = 8
#
# Their slopes are:
#
#       2/5
#       3/8
#
# and
#
#       2/5 - 3/8 = 1/40
#
# That tiny difference is the entire secret.
#
# This part should feel like a mathematical detective story.
# ============================================================


class MissingTrianglePart6(MovingCameraScene):

    def construct(self):

        self.camera.background_color = "#F8F5E9"

        self.setup_scene()

        self.create_main_lines()

        self.create_slope_triangles()

        self.create_equations()

        self.create_gap_objects()

        self.opening()

        self.show_apparently_straight_line()

        self.break_line_into_two_parts()

        self.show_first_slope()

        self.show_second_slope()

        self.compare_slopes()

        self.show_cross_multiplication()

        self.reveal_one_over_forty()

        self.return_to_geometry()

        self.exaggerate_difference()

        self.show_endpoint_gap()

        self.show_true_shape()

        self.compare_straight_and_bent()

        self.zoom_into_corner()

        self.final_equation()

        self.final_question()

        self.end_part()


    # ========================================================
    # SCENE SETUP
    # ========================================================

    def setup_scene(self):

        self.scale_factor = 0.58

        self.left_x = -4.2

        self.base_y = -1.5


        self.start_point = np.array([
            self.left_x,
            self.base_y,
            0,
        ])


        self.first_run = 5

        self.first_rise = 2

        self.second_run = 8

        self.second_rise = 3


        self.first_end = (
            self.start_point
            + RIGHT
            * self.first_run
            * self.scale_factor
            + UP
            * self.first_rise
            * self.scale_factor
        )


        self.second_end = (
            self.first_end
            + RIGHT
            * self.second_run
            * self.scale_factor
            + UP
            * self.second_rise
            * self.scale_factor
        )


        self.total_run = (
            self.first_run
            +
            self.second_run
        )


        self.total_rise = (
            self.first_rise
            +
            self.second_rise
        )


        self.true_final_point = (
            self.start_point
            + RIGHT
            * self.total_run
            * self.scale_factor
            + UP
            * self.total_rise
            * self.scale_factor
        )


        # ----------------------------------------------------
        # A mathematically straight line connecting the same
        # starting and final points.
        # ----------------------------------------------------

        self.straight_line = Line(
            self.start_point,
            self.true_final_point,
            stroke_color=BLACK,
            stroke_width=5,
        )


        # ----------------------------------------------------
        # The two actual pieces.
        # ----------------------------------------------------

        self.segment_one = Line(
            self.start_point,
            self.first_end,
            stroke_color=BLACK,
            stroke_width=5,
        )


        self.segment_two = Line(
            self.first_end,
            self.second_end,
            stroke_color=BLACK,
            stroke_width=5,
        )


        self.bent_line = VGroup(
            self.segment_one,
            self.segment_two,
        )


    # ========================================================
    # SLOPE TRIANGLES
    # ========================================================

    def create_slope_triangles(self):

        # ----------------------------------------------------
        # Triangle for slope 2/5
        # ----------------------------------------------------

        first_horizontal_end = (
            self.start_point
            + RIGHT
            * self.first_run
            * self.scale_factor
        )


        self.first_slope_horizontal = Line(
            self.start_point,
            first_horizontal_end,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.first_slope_vertical = Line(
            first_horizontal_end,
            self.first_end,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.first_slope_triangle = VGroup(
            self.first_slope_horizontal,
            self.first_slope_vertical,
            self.segment_one.copy(),
        )


        # ----------------------------------------------------
        # Triangle for slope 3/8
        # ----------------------------------------------------

        second_horizontal_end = (
            self.first_end
            + RIGHT
            * self.second_run
            * self.scale_factor
        )


        self.second_slope_horizontal = Line(
            self.first_end,
            second_horizontal_end,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.second_slope_vertical = Line(
            second_horizontal_end,
            self.second_end,
            stroke_color=BLACK,
            stroke_width=2,
        )


        self.second_slope_triangle = VGroup(
            self.second_slope_horizontal,
            self.second_slope_vertical,
            self.segment_two.copy(),
        )


        self.first_slope_triangle.set_opacity(0)

        self.second_slope_triangle.set_opacity(0)


    # ========================================================
    # EQUATIONS
    # ========================================================

    def create_equations(self):

        self.first_slope_equation = MathTex(
            r"m_1"
            "="
            r"\frac{\text{rise}}{\text{run}}"
            "="
            r"\frac25",
            color=BLACK,
        ).scale(0.75)


        self.second_slope_equation = MathTex(
            r"m_2"
            "="
            r"\frac{\text{rise}}{\text{run}}"
            "="
            r"\frac38",
            color=BLACK,
        ).scale(0.75)


        self.slope_difference_equation = MathTex(
            r"m_1-m_2"
            "="
            r"\frac25-\frac38",
            color=BLACK,
        ).scale(0.75)


        self.cross_multiply_equation = MathTex(
            r"\frac25-\frac38"
            "="
            r"\frac{16}{40}-\frac{15}{40}",
            color=BLACK,
        ).scale(0.72)


        self.final_difference_equation = MathTex(
            r"\boxed{\frac25-\frac38=\frac1{40}}",
            color=BLACK,
        ).scale(0.85)


        self.not_equal_equation = MathTex(
            r"\frac25\neq\frac38",
            color=BLACK,
        ).scale(0.9)


    # ========================================================
    # GAP OBJECTS
    # ========================================================

    def create_gap_objects(self):

        # ----------------------------------------------------
        # The point where the bent line changes direction.
        # ----------------------------------------------------

        self.corner_dot = Dot(
            self.first_end,
            radius=0.07,
            color=BLACK,
        )


        self.start_dot = Dot(
            self.start_point,
            radius=0.07,
            color=BLACK,
        )


        self.final_dot = Dot(
            self.second_end,
            radius=0.07,
            color=BLACK,
        )


        # ----------------------------------------------------
        # Gap between the true bent endpoint and the straight
        # line at the same horizontal position.
        # ----------------------------------------------------

        x_position = self.second_end[0]


        straight_y_at_end = (
            self.start_point[1]
            +
            (
                self.true_final_point[1]
                -
                self.start_point[1]
            )
            *
            (
                (
                    x_position
                    -
                    self.start_point[0]
                )
                /
                (
                    self.true_final_point[0]
                    -
                    self.start_point[0]
                )
            )
        )


        self.straight_endpoint_at_bent_x = np.array([
            x_position,
            straight_y_at_end,
            0,
        ])


        self.endpoint_gap = Line(
            self.straight_endpoint_at_bent_x,
            self.second_end,
            stroke_color=BLACK,
            stroke_width=3,
        )


        self.gap_brace = Brace(
            self.endpoint_gap,
            direction=RIGHT,
        )


    # ========================================================
    # OPENING
    # ========================================================

    def opening(self):

        self.title = Text(
            "Look closely at the long edge.",
            font_size=32,
            color=BLACK,
        )


        self.title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            FadeIn(
                self.title,
                shift=DOWN * 0.15,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


    # ========================================================
    # APPARENTLY STRAIGHT LINE
    # ========================================================

    def show_apparently_straight_line(self):

        self.play(
            Create(
                self.straight_line,
            ),
            run_time=1.5,
        )


        self.wait(0.7)


        straight_text = Text(
            "It looks perfectly straight.",
            font_size=28,
            color=BLACK,
        )


        straight_text.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            FadeIn(
                straight_text,
                shift=UP * 0.15,
            ),
            run_time=0.7,
        )


        self.wait(1)


        self.play(
            Indicate(
                self.straight_line,
                scale_factor=1.03,
            ),
            run_time=0.8,
        )


        self.wait(0.7)


        self.play(
            FadeOut(
                straight_text,
            ),
            run_time=0.4,
        )


    # ========================================================
    # BREAK INTO TWO PARTS
    # ========================================================

    def break_line_into_two_parts(self):

        break_title = Text(
            "But this edge is made from two pieces.",
            font_size=30,
            color=BLACK,
        )


        break_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                break_title,
            ),
            run_time=0.7,
        )


        self.wait(0.6)


        self.play(
            FadeOut(
                self.straight_line,
            ),
            run_time=0.5,
        )


        self.play(
            Create(
                self.segment_one,
            ),
            Create(
                self.segment_two,
            ),
            run_time=1.2,
        )


        self.wait(0.8)


        self.play(
            FadeIn(
                self.start_dot,
                self.corner_dot,
                self.final_dot,
            ),
            run_time=0.5,
        )


        self.wait(0.7)


        corner_label = Text(
            "corner",
            font_size=22,
            color=BLACK,
        )


        corner_label.next_to(
            self.corner_dot,
            DOWN,
            buff=0.15,
        )


        self.play(
            FadeIn(
                corner_label,
            ),
            run_time=0.5,
        )


        self.wait(0.8)


        self.corner_label = corner_label


    # ========================================================
    # FIRST SLOPE
    # ========================================================

    def show_first_slope(self):

        self.play(
            FadeOut(
                self.corner_label,
            ),
            run_time=0.4,
        )


        first_title = Text(
            "Measure the first piece.",
            font_size=30,
            color=BLACK,
        )


        first_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                first_title,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        self.first_slope_triangle.set_opacity(1)


        self.play(
            Create(
                self.first_slope_horizontal,
            ),
            Create(
                self.first_slope_vertical,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        rise_label = MathTex(
            r"2",
            color=BLACK,
        ).scale(0.65)


        rise_label.next_to(
            self.first_slope_vertical,
            RIGHT,
            buff=0.15,
        )


        run_label = MathTex(
            r"5",
            color=BLACK,
        ).scale(0.65)


        run_label.next_to(
            self.first_slope_horizontal,
            DOWN,
            buff=0.15,
        )


        self.play(
            Write(
                rise_label,
            ),
            Write(
                run_label,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.play(
            Write(
                self.first_slope_equation,
            ),
            run_time=0.9,
        )


        self.first_slope_equation.to_edge(
            DOWN,
            buff=0.45,
        )


        self.wait(1)


        self.first_rise_label = rise_label

        self.first_run_label = run_label


    # ========================================================
    # SECOND SLOPE
    # ========================================================

    def show_second_slope(self):

        second_title = Text(
            "Now measure the second piece.",
            font_size=30,
            color=BLACK,
        )


        second_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                second_title,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        self.second_slope_triangle.set_opacity(1)


        self.play(
            Create(
                self.second_slope_horizontal,
            ),
            Create(
                self.second_slope_vertical,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        rise_label_2 = MathTex(
            r"3",
            color=BLACK,
        ).scale(0.65)


        rise_label_2.next_to(
            self.second_slope_vertical,
            RIGHT,
            buff=0.15,
        )


        run_label_2 = MathTex(
            r"8",
            color=BLACK,
        ).scale(0.65)


        run_label_2.next_to(
            self.second_slope_horizontal,
            DOWN,
            buff=0.15,
        )


        self.play(
            Write(
                rise_label_2,
            ),
            Write(
                run_label_2,
            ),
            run_time=0.7,
        )


        self.wait(0.7)


        self.play(
            FadeOut(
                self.first_slope_equation,
            ),
            run_time=0.4,
        )


        self.second_slope_equation.to_edge(
            DOWN,
            buff=0.45,
        )


        self.play(
            Write(
                self.second_slope_equation,
            ),
            run_time=0.9,
        )


        self.wait(1)


        self.second_rise_label = rise_label_2

        self.second_run_label = run_label_2


    # ========================================================
    # COMPARE SLOPES
    # ========================================================

    def compare_slopes(self):

        compare_title = Text(
            "And now compare them.",
            font_size=30,
            color=BLACK,
        )


        compare_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                compare_title,
            ),
            run_time=0.6,
        )


        self.wait(0.6)


        self.play(
            FadeOut(
                self.second_slope_equation,
            ),
            run_time=0.4,
        )


        self.not_equal_equation.move_to(
            DOWN * 1.8,
        )


        self.play(
            Write(
                self.not_equal_equation,
            ),
            run_time=0.9,
        )


        self.wait(0.8)


        self.play(
            Indicate(
                self.not_equal_equation,
                scale_factor=1.12,
            ),
            run_time=0.8,
        )


        self.wait(0.8)


        # ----------------------------------------------------
        # Put the two fractions vertically.
        # ----------------------------------------------------

        first_fraction = MathTex(
            r"\frac25",
            color=BLACK,
        ).scale(0.9)


        second_fraction = MathTex(
            r"\frac38",
            color=BLACK,
        ).scale(0.9)


        first_fraction.move_to(
            LEFT * 1.0
            +
            UP * 0.5,
        )


        second_fraction.move_to(
            LEFT * 1.0
            +
            DOWN * 0.5,
        )


        comparison_symbol = MathTex(
            r"\neq",
            color=BLACK,
        ).scale(0.8)


        comparison_symbol.move_to(
            RIGHT * 0.1,
        )


        self.play(
            FadeOut(
                self.not_equal_equation,
            ),
            FadeIn(
                first_fraction,
            ),
            FadeIn(
                comparison_symbol,
            ),
            FadeIn(
                second_fraction,
            ),
            run_time=0.7,
        )


        self.wait(0.8)


        self.fraction_group = VGroup(
            first_fraction,
            comparison_symbol,
            second_fraction,
        )


    # ========================================================
    # CROSS MULTIPLICATION
    # ========================================================

    def show_cross_multiplication(self):

        cross_title = Text(
            "Let's check it without decimals.",
            font_size=29,
            color=BLACK,
        )


        cross_title.to_edge(
            UP,
            buff=0.4,
        )


        self.play(
            Transform(
                self.title,
                cross_title,
            ),
            run_time=0.6,
        )


        self.wait(0.5)


        cross_step = MathTex(
            r"\frac25"
            r"\quad\text{vs.}\quad"
            r"\frac38",
            color=BLACK,
        ).scale(0.8)


        cross_step.move_to(
            UP * 1.0,
        )


        self.play(
            ReplacementTransform(
                self.fraction_group,
                cross_step,
            ),
            run_time=0.8,
        )


        self.wait(0.5)


        cross_numbers = MathTex(
            r"2\times8"
            r"\quad\text{vs.}\quad"
            r"3\times5",
            color=BLACK,
        ).scale(0.8)


        cross_numbers.next_to(
            cross_step,
            DOWN,
            buff=0.4,
        )


     
