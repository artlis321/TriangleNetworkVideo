from manim import *
from pointslopeLLtrongle import d,testO
from tqdm import tqdm

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


        try:
            A0O = DashedLine(start=[*A0,0],end=[*O,0])
            B0O = DashedLine(start=[*B0,0],end=[*O,0])
            C0O = DashedLine(start=[*C0,0],end=[*O,0])

            pointO = Circle(radius=s,color='blue',fill_opacity=1)
            pointO.move_to([*O,0]).set_z_index(1)

            self.add(pointO,A0O,B0O,C0O)
        except:
            return

class TronglePointSlope(TrongleMain):
    def __init__(self,A,B,C,O,testOdict,normscale,s=0.1):
        A0 = O - (O-A)/d(O,A)*normscale*testOdict['scale_max']*testOdict['A0O']
        B0 = O - (O-B)/d(O,B)*normscale*testOdict['scale_max']*testOdict['B0O']
        C0 = O - (O-C)/d(O,C)*normscale*testOdict['scale_max']*testOdict['C0O']

        super().__init__(A,B,C,A0,B0,C0,O=O,s=s)

class FullTrongle(Scene):
    def construct(self):
        A = np.array([0,0])
        B_x = 5
        B = np.array([B_x,0])
        C_x = 3
        C_y = 3
        C = np.array([C_x,C_y])
        
        first = True

        center_point = [-3,0,0]
        x_num = 40
        y_num = 24
        scale_num = 2
        x_range = np.linspace(0,5,x_num)
        y_range = np.linspace(0,3,y_num)
        scale_range = np.linspace(0,1,scale_num)

        def box_to_zoom(c):
            return (c-np.array([2.85-5.5,1.3-1.5,0]))*4 + np.array([-0.5,1,0])

        box = Rectangle(color='yellow',height=0.5,width=0.2)
        box.move_to([2.85-5.5,1.3-1.5,0])


        ax = Axes(
            x_range = [0,18,4],
            y_range = [0,20,3],
            x_length = 5,
            y_length = 5
        )
        ax.move_to([3,0,0])
        labels = ax.get_axis_labels(x_label='L',y_label='D')

        curpoint = Circle(radius=0.08,color='GRAY').set_z_index(1)
        curpoint.move_to( ax.coords_to_point(0,0) )

        lines = {}

        fPoint = Circle(radius=0.1,color='RED',fill_opacity=1)
        fPoint.move_to(np.array(center_point)+np.array([0.39,-0.08,0]))
        vals_f = testO(A,B,C,np.array([2.89,1.42]))
        coords_f = [vals_f['L_0'],vals_f['D_0']]
        point_f = ax.coords_to_point(*coords_f)
        fPointAx = Circle(radius=0.05,color='RED',fill_opacity=1)
        fPointAx.move_to(point_f)
        fPointZoom = Circle(radius=0.1,color='RED',fill_opacity=1)

        bPoint = Circle(radius=0.1,color='RED',fill_opacity=1)
        bPoint.move_to(np.array(center_point)+np.array([0.32,-0.33,0]))
        vals_b = testO(A,B,C,np.array([2.82,1.17]))
        coords_b = [vals_b['L_max'],vals_b['D_min']]
        point_b = ax.coords_to_point(*coords_b)
        bPointAx = Circle(radius=0.05,color='RED',fill_opacity=1)
        bPointAx.move_to(point_b)
        bPointZoom = Circle(radius=0.1,color='RED',fill_opacity=1)


        self.play(FadeIn(ax,labels,curpoint,fPointAx,bPointAx))

        for i in tqdm(range(y_num-1,-1,-1)):
            if i % 2 == 0:
                j_range = range(x_num)
            else:
                j_range = range(-1,-x_num-1,-1)
            for j in j_range:
                y = y_range[i]
                x = x_range[j]
                if (x>y*C_x/C_y) and (x<(B_x*(1-y/C_y)+C_x*(y/C_y))):
                    O = np.array([x,y])
                    vals = testO(A,B,C,O)

                    if vals['success']:
                        if first:
                            t = TronglePointSlope(A,B,C,O,vals,0)
                            t.move_to(center_point)

                            self.play( FadeIn(t) )
                            self.play( FadeIn(fPoint,bPoint) )

                            first = False
                        start = True
                        for scale in scale_range:
                            t_new = TronglePointSlope(A,B,C,O,vals,scale)
                            t_new.move_to(center_point)

                            if start:
                                lines[str(i)+"|"+str(j)] = ax.plot_line_graph([vals['L_0']],[vals['D_0']],vertex_dot_radius=0.02,line_color='#FFFFFF')
                                newpoint = Circle(radius=0.08,color='GRAY').set_z_index(1)
                                newpoint.move_to( ax.coords_to_point(vals['L_0'],vals['D_0']) )

                                self.play(  Transform(t,t_new,run_time=0.2) , 
                                            FadeIn(lines[str(i)+"|"+str(j)],run_time=0.2) ,
                                            Transform(curpoint,newpoint,run_time=0.2) )

                                start = False
                            else:
                                l_val = vals['L_0']*(1-scale)+vals['L_max']*scale
                                d_val = vals['D_0']*(1-scale)+vals['D_min']*scale
                                newline = ax.plot_line_graph([vals['L_0'],l_val],[vals['D_0'],d_val],vertex_dot_radius=0.02,line_color='#FFFFFF')

                                newpoint = Circle(radius=0.08,color='GRAY').set_z_index(1)
                                newpoint.move_to( ax.coords_to_point(l_val,d_val) )

                                self.play(  Transform(t,t_new,run_time=0.2) ,
                                            FadeIn(newline,run_time=0.2) ,
                                            FadeOut(lines[str(i)+"|"+str(j)],run_time=0.2) ,
                                            Transform(curpoint,newpoint,run_time=0.2) )

                                lines[str(i)+"|"+str(j)] = newline
                            self.wait(0.1)

        self.wait(1)

class FocusTrongle(Scene):
    def construct(self):
        A = np.array([0,0])
        B_x = 5
        B = np.array([B_x,0])
        C_x = 3
        C_y = 3
        C = np.array([C_x,C_y])
        
        first = True

        center_point = [-3,0,0]
        x_num = 8
        y_num = 32
        scale_num = 2
        x_range = np.linspace(2.8,2.9,x_num)
        y_range = np.linspace(1.1,1.5,y_num)
        scale_range = np.linspace(0,1,scale_num)

        def box_to_zoom(c):
            return (c-np.array([2.85-5.5,1.3-1.5,0]))*4 + np.array([-0.5,1,0])

        box = Rectangle(color='yellow',height=0.5,width=0.2)
        box.move_to([2.85-5.5,1.3-1.5,0])

        zoom_box = Rectangle(color='yellow',height=2,width=0.8)
        zoom_box.move_to([-0.5,1,0])

        ax = Axes(
            x_range = [7,13,1],
            y_range = [12,16,1],
            x_length = 5,
            y_length = 5
        )
        ax.move_to([3,0,0])
        labels = ax.get_axis_labels(x_label='L',y_label='D')

        curpoint = Circle(radius=0.08,color='GRAY').set_z_index(1)
        curpoint.move_to( ax.coords_to_point(0,0) )

        lines = {}

        fPoint = Circle(radius=0.1,color='RED',fill_opacity=1)
        fPoint.move_to(np.array(center_point)+np.array([0.39,-0.08,0]))
        vals_f = testO(A,B,C,np.array([2.89,1.42]))
        coords_f = [vals_f['L_0'],vals_f['D_0']]
        point_f = ax.coords_to_point(*coords_f)
        fPointAx = Circle(radius=0.05,color='RED',fill_opacity=1)
        fPointAx.move_to(point_f)
        fPointZoom = Circle(radius=0.1,color='RED',fill_opacity=1)
        fPointZoom.move_to(box_to_zoom(fPoint.get_center()))

        bPoint = Circle(radius=0.1,color='RED',fill_opacity=1)
        bPoint.move_to(np.array(center_point)+np.array([0.32,-0.33,0]))
        vals_b = testO(A,B,C,np.array([2.82,1.17]))
        coords_b = [vals_b['L_max'],vals_b['D_min']]
        point_b = ax.coords_to_point(*coords_b)
        bPointAx = Circle(radius=0.05,color='RED',fill_opacity=1)
        bPointAx.move_to(point_b)
        bPointZoom = Circle(radius=0.1,color='RED',fill_opacity=1)
        bPointZoom.move_to(box_to_zoom(bPoint.get_center()))

        Ozoom = Circle(radius=0.1,color='BLUE',fill_opacity=1).set_z_index(1)

        self.play(FadeIn(ax,labels,curpoint,fPointAx,bPointAx))

        for i in tqdm(range(y_num-1,-1,-1)):
            if i % 2 == 0:
                j_range = range(x_num)
            else:
                j_range = range(-1,-x_num-1,-1)
            for j in j_range:
                y = y_range[i]
                x = x_range[j]
                if (x>y*C_x/C_y) and (x<(B_x*(1-y/C_y)+C_x*(y/C_y))):
                    O = np.array([x,y])
                    vals = testO(A,B,C,O)

                    if vals['success']:
                        if first:
                            t = TronglePointSlope(A,B,C,O,vals,0)
                            t.move_to(center_point)
                            Ozoom.move_to(box_to_zoom(np.array([*O,0])+np.array([-5.5,-1.5,0])))

                            self.play( FadeIn(t,box,zoom_box,Ozoom) )
                            self.play( FadeIn(fPoint,bPoint,fPointZoom,bPointZoom) )

                            first = False
                        start = True
                        for scale in scale_range:
                            t_new = TronglePointSlope(A,B,C,O,vals,scale)
                            t_new.move_to(center_point)
                            Ozoom_new = Circle(radius=0.1,color='BLUE',fill_opacity=1).set_z_index(1)
                            Ozoom_new.move_to(box_to_zoom(np.array([*O,0])+np.array([-5.5,-1.5,0])))

                            if start:
                                lines[str(i)+"|"+str(j)] = ax.plot_line_graph([vals['L_0']],[vals['D_0']],vertex_dot_radius=0.02,line_color='#FFFFFF')
                                newpoint = Circle(radius=0.08,color='GRAY').set_z_index(1)
                                newpoint.move_to( ax.coords_to_point(vals['L_0'],vals['D_0']) )

                                self.play(  Transform(t,t_new,run_time=0.2) , 
                                            Transform(Ozoom,Ozoom_new,run_time=0.2),
                                            FadeIn(lines[str(i)+"|"+str(j)],run_time=0.2) ,
                                            Transform(curpoint,newpoint,run_time=0.2) )

                                start = False
                            else:
                                l_val = vals['L_0']*(1-scale)+vals['L_max']*scale
                                d_val = vals['D_0']*(1-scale)+vals['D_min']*scale
                                newline = ax.plot_line_graph([vals['L_0'],l_val],[vals['D_0'],d_val],vertex_dot_radius=0.02,line_color='#FFFFFF')

                                newpoint = Circle(radius=0.08,color='GRAY').set_z_index(1)
                                newpoint.move_to( ax.coords_to_point(l_val,d_val) )

                                self.play(  Transform(t,t_new,run_time=0.2) ,
                                            Transform(Ozoom,Ozoom_new,run_time=0.2),
                                            FadeIn(newline,run_time=0.2) ,
                                            FadeOut(lines[str(i)+"|"+str(j)],run_time=0.2) ,
                                            Transform(curpoint,newpoint,run_time=0.2) )

                                lines[str(i)+"|"+str(j)] = newline
                            self.wait(0.1)

        self.wait(1)

class BestTrongle(Scene):
    def construct(self):
        d_min = np.loadtxt('d_min.txt')
        l_max = np.loadtxt('l_max.txt')
        O_x = np.loadtxt('O_x.txt')
        O_y = np.loadtxt('O_y.txt')

        size = d_min.size
        n_avg = 30
        size_avg = size // n_avg
        d_avg = np.empty(size_avg)
        l_avg = np.empty(size_avg)
        O_x_avg = np.empty(size_avg)
        O_y_avg = np.empty(size_avg)

        for i in range( d_avg.size ):
            d_avg[i] = np.average(d_min[i*n_avg:(i+1)*n_avg])
            l_avg[i] = np.average(l_max[i*n_avg:(i+1)*n_avg])
            O_x_avg[i] = np.average(O_x[i*n_avg:(i+1)*n_avg])
            O_y_avg[i] = np.average(O_y[i*n_avg:(i+1)*n_avg])

        A = np.array([0,0])
        B_x = 5
        B = np.array([B_x,0])
        C_x = 3
        C_y = 3
        C = np.array([C_x,C_y])
        
        first = True

        center_point = [-3,0,0]
        x_num = 8
        y_num = 32
        scale_num = 2
        x_range = np.linspace(2.8,2.9,x_num)
        y_range = np.linspace(1.1,1.5,y_num)
        scale_range = np.linspace(0,1,scale_num)

        def box_to_zoom(c):
            return (c-np.array([2.85-5.5,1.3-1.5,0]))*4 + np.array([-0.5,1,0])

        box = Rectangle(color='yellow',height=0.5,width=0.2)
        box.move_to([2.85-5.5,1.3-1.5,0])

        zoom_box = Rectangle(color='yellow',height=2,width=0.8)
        zoom_box.move_to([-0.5,1,0])

        ax = Axes(
            x_range = [7,13,1],
            y_range = [12,16,1],
            x_length = 5,
            y_length = 5
        )
        ax.move_to([3,0,0])
        labels = ax.get_axis_labels(x_label='L',y_label='D')

        curpoint = Circle(radius=0.08,color='GRAY').set_z_index(1)

        lines = {}

        fPoint = Circle(radius=0.1,color='RED',fill_opacity=1)
        fPoint.move_to(np.array(center_point)+np.array([0.39,-0.08,0]))
        vals_f = testO(A,B,C,np.array([2.89,1.42]))
        coords_f = [vals_f['L_0'],vals_f['D_0']]
        point_f = ax.coords_to_point(*coords_f)
        fPointAx = Circle(radius=0.05,color='RED',fill_opacity=1)
        fPointAx.move_to(point_f)
        fPointZoom = Circle(radius=0.1,color='RED',fill_opacity=1)
        fPointZoom.move_to(box_to_zoom(fPoint.get_center()))

        bPoint = Circle(radius=0.1,color='RED',fill_opacity=1)
        bPoint.move_to(np.array(center_point)+np.array([0.32,-0.33,0]))
        vals_b = testO(A,B,C,np.array([2.82,1.17]))
        coords_b = [vals_b['L_max'],vals_b['D_min']]
        point_b = ax.coords_to_point(*coords_b)
        bPointAx = Circle(radius=0.05,color='RED',fill_opacity=1)
        bPointAx.move_to(point_b)
        bPointZoom = Circle(radius=0.1,color='RED',fill_opacity=1)
        bPointZoom.move_to(box_to_zoom(bPoint.get_center()))

        Ozoom = Circle(radius=0.1,color='BLUE',fill_opacity=1).set_z_index(1)

        O = np.array([2.89,1.42])
        vals = testO(A,B,C,O)
        t = TronglePointSlope(A,B,C,O,vals,0)
        t.move_to(center_point)

        l_vals = [vals['L_0']]
        d_vals = [vals['D_0']]
        line = ax.plot_line_graph(l_vals,d_vals,vertex_dot_radius=0.02,line_color='#FFFFFF')

        curpoint.move_to( ax.coords_to_point(vals['L_0'],vals['D_0']) )

        Ozoom.move_to(box_to_zoom(np.array([*O,0])+np.array([-5.5,-1.5,0])))

        self.play(FadeIn(t,zoom_box,box,fPoint,bPoint,fPointAx,bPointAx,fPointZoom,bPointZoom,Ozoom,ax,curpoint,line,labels))

        for scale in np.linspace(0,1,d_avg.size//2):
            t_new = TronglePointSlope(A,B,C,O,vals,scale)
            t_new.move_to(center_point)

            new_l = vals['L_0']*(1-scale)+vals['L_max']*scale
            new_d = vals['D_0']*(1-scale)+vals['D_min']*scale
            l_vals.append( new_l )
            d_vals.append( new_d )
            newcurpoint = Circle(radius=0.08,color='GRAY').set_z_index(1)
            newcurpoint.move_to( ax.coords_to_point(new_l,new_d) )

            newline = ax.plot_line_graph(l_vals,d_vals,vertex_dot_radius=0,line_color='#FFFFFF')

            self.play(  Transform(t,t_new,run_time=1/60) ,
                        FadeOut(line,run_time=1/60) ,
                        FadeIn(newline,run_time=1/60) ,
                        Transform(curpoint,newcurpoint,run_time=1/60)
            )
            line = newline
            self.wait(1/60)

        for i in range(d_avg.size):
            O = [O_x_avg[i],O_y_avg[i]]
            Ozoom_new = Circle(radius=0.1,color='BLUE',fill_opacity=1).set_z_index(1)
            Ozoom_new.move_to(box_to_zoom(np.array([*O,0])+np.array([-5.5,-1.5,0])))
            vals = testO(A,B,C,O)
            t_new = TronglePointSlope(A,B,C,O,vals,1)
            t_new.move_to(center_point)

            new_l = vals['L_max']
            new_d = vals['D_min']
            l_vals.append( new_l )
            d_vals.append( new_d )

            newcurpoint = Circle(radius=0.08,color='GRAY').set_z_index(1)
            newcurpoint.move_to( ax.coords_to_point(new_l,new_d) )

            newline = ax.plot_line_graph(l_vals,d_vals,vertex_dot_radius=0,line_color='#FFFFFF')

            self.play(  Transform(t,t_new,run_time=1/60),
                        Transform(Ozoom,Ozoom_new,run_time=1/60),
                        FadeOut(line,run_time=1/60) ,
                        FadeIn(newline,run_time=1/60),
                        Transform(curpoint,newcurpoint,run_time=1/60)
            )
            line = newline
            self.wait(1/60)