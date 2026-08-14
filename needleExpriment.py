from manim import *
from typing import Literal

class Paper(Rectangle):
    def __init__(self, mode : Literal["standart"] | None =None, **kwargs):
        '''
        all **kwargs parameter is same parameter of "Rectangle"
        '''
        self.mode = mode
        if self.mode == "standart":
            height = kwargs.get("height",6)
            kwargs["height"] = height
            kwargs["width"] = height*(9/11)
            kwargs["fill_color"]="#F8F5E9"
            kwargs["fill_opacity"]=1
        super().__init__(**kwargs)

    def get_height(self):
        height = self.get_top()[1] - self.get_bottom()[1]
        return height

    def get_width(self):
        width = self.get_right()[0]-self.get_left()[0]
        return width

    def add_vertices_lable(self,vertices_index=None,label_ver_dis = 0.5,**kwargs):
        '''
        all **kwargs parameter is same parameter of "Tex" or "text" 
        '''
        if vertices_index is None:
            vertices_index = [0,1,2,3]
        vertices = self.get_vertices()
        ver_labels = VGroup()
        show_vertices = VGroup()
        for ver , label , pos  in zip(vertices,["0","1","2","3"],[UR,UL,DL,DR]):
            try:
                ver_label = Tex(label,**kwargs).move_to(ver+pos*label_ver_dis)
            except:
                ver_label = Text(label,**kwargs).move_to(ver+pos*label_ver_dis)
            ver_labels.add(ver_label)
        for i in vertices_index:
            show_vertices.add(ver_labels[i])
        self.add(show_vertices)
        return show_vertices
    def add_lines(self,lines=10,visuall_lines = True ,**kwargs):
        '''
        all **kwargs parameter is same parameter of "Line"
        '''
        left_x = self.get_left()[0]
        right_x = self.get_right()[0]
        ds_start = np.linspace(self.get_vertices()[1][1],self.get_vertices()[2][1],lines)
        ds_end = np.linspace(self.get_vertices()[0][1],self.get_vertices()[3][1],lines)
        lines = VGroup()
        for start,end in zip(ds_start,ds_end):
            start_point = np.array([left_x,start,0])
            end_point = np.array([right_x,end,0])
            line = Line(start=start_point,end=end_point,color=BLACK,stroke_width=1,buff=0.2,**kwargs)
            lines.add(line)
        if visuall_lines:
            lines.remove(lines[0])
            lines.remove(lines[-1])
            return lines
        else:
            return lines

    def add_axes(self,**kwargs):
        '''
        all parameter is same parameter of "Axes"
        '''
        ax = Axes(
            x_range=[-5,5,1],
            y_range=[-10,10,1],
            x_length=self.get_width(),
            y_length=self.get_height(),
            axis_config={'color':BLACK,'include_tip':False},
            **kwargs
        )
        return ax
    def add_grid(self,**kwargs ):
        '''
        the pratameter is same parameter of "NunberPlane"
        '''
        grid = NumberPlane(
            x_range=[-5,5,1],
            y_range=[-10,10,1],
            x_length=self.get_width(),

            y_length=self.get_height(),
            axis_config={'color':BLACK,'include_tip':False},
            **kwargs
        )
        return grid



class NeedleNeedleExperiment(Scene):
    def construct(self):
        paper = Paper(mode="standart")
        paper.lines = paper.add_lines(lines=10)
        paper.axes = paper.add_axes()

        self.play(DrawBorderThenFill(paper))
        self.wait(1)
        self.play(LaggedStart(*[Create(line) for line in paper.lines],run_time=3,lag_ratio=0.1))
        self.add(paper.axes)
        self.wait(2)

class Test(Scene):
    def construct(self):
        paper = Paper(mode="standart").set_z_index(0)
        paper.axes = paper.add_grid().set_z_index(1)
        paper.axes.add_coordinates(font_size=30)
        paper.axes.x_axis.set_color(BLACK)
        paper.axes.y_axis.set_color(BLACK)

        self.add(paper.axes,paper)
        self.wait(2)


%manim -v WARNING -ql Test
