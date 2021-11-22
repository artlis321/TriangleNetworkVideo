from manim import *

class TrongleMain(VGroup):
    def __init__(self,A,B,C,A0,B0,C0,O=None,s=0.1):
        AA0 = Line(start=[*A,0],end=[*A0,0])
        BB0 = Line(start=[*B,0],end=[*B0,0])
        CC0 = Line(start=[*C,0],end=[*C0,0])
        A0B0 = Line(start=[*A0,0],end=[*B0,0])
        B0C0 = Line(start=[*B0,0],end=[*C0,0])
        C0A0 = Line(start=[*C0,0],end=[*A0,0])

        pointA = Circle(radius=s,color='red',fill_opacity=1)
        pointA.move_to([*A,0]).set_z_index(1)

        pointB = Circle(radius=s,color='red',fill_opacity=1)
        pointB.move_to([*B,0]).set_z_index(1)

        pointC = Circle(radius=s,color='red',fill_opacity=1)
        pointC.move_to([*C,0]).set_z_index(1)

        pointA0 = Circle(radius=s,color='green',fill_opacity=1)
        pointA0.move_to([*A0,0]).set_z_index(1)

        pointB0 = Circle(radius=s,color='green',fill_opacity=1)
        pointB0.move_to([*B0,0]).set_z_index(1)

        pointC0 = Circle(radius=s,color='green',fill_opacity=1)
        pointC0.move_to([*C0,0]).set_z_index(1)

        VGroup.__init__(self)

        self.add(
            pointA,pointB,pointC,pointA0,pointB0,pointC0,
            AA0,BB0,CC0,A0B0,B0C0,C0A0
            )

        if O != None:
            A0O = DashedLine(start=[*A0,0],end=[*O,0])
            B0O = DashedLine(start=[*B0,0],end=[*O,0])
            C0O = DashedLine(start=[*C0,0],end=[*O,0])

            pointO = Circle(radius=s,color='blue',fill_opacity=1)
            pointO.move_to([*O,0]).set_z_index(1)

            self.add(pointO,A0O,B0O,C0O)


class Test(Scene):
    def construct(self):
        trongle = TrongleMain([0,0],[2,0],[1,3],[0.5,0.5],[1.5,0.5],[1,1],O=[1,0.8],s=0.01)

        self.play( Create(trongle) )
        
        new_trongle = TrongleMain([0,0],[2,0],[1,3],[0.7,0.7],[1.2,0.2],[1,0.8],O=[1,0.6],s=0.01)

        self.play( Transform(trongle,new_trongle) )