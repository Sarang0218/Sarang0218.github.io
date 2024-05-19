from manim import *
from manim.typing import *
import math

from manim_slides import ThreeDSlide



class Paragraph1(ThreeDSlide):
    
    def construct(self):
        
        title = VGroup(
            Text("블랙홀이란 무엇인가?", t2c={"블랙홀": BLUE}).scale(1.5),
            Text("발표: 박사랑", t2c={"박사랑": YELLOW}),
        ).arrange(DOWN)
        
        lyric1 = VGroup(
            Text("저기 사라진 별의 자리", t2c={"별": YELLOW}),
            Text("아스라이 하얀빛", t2c={"빛": YELLOW}),
            Text("한동안은 꺼내볼수 있을꺼야"),
        ).arrange(DOWN)
        lyric2 = VGroup(
            Text("그래도 이제는,"),
            Text("사건의 지평선 너머로", t2c={"사건의 지평선": YELLOW}),
        ).arrange(DOWN)
        
        
        
        newton = MathTex(r"F = G \frac{m_1 m_2}{r^2}").shift(UP*2)
        EFE = MathTex(r"R_{\mu \nu} - {1 \over 2}g_{\mu \nu}\,R + g_{\mu \nu} \Lambda = {8 \pi G \over c^4} T_{\mu \nu}").shift(LEFT).shift(DOWN)
        SCHWART = MathTex(r"{ds}^{2}=c^{2}\,{d\tau }^{2}=\left(1-{\frac {r_{\mathrm {s} }}{r}}\right)c^{2}\,dt^{2}-\left(1-{\frac {r_{\mathrm {s} }}{r}}\right)^{-1}\,dr^{2}-r^{2}{d\Omega }^{2}").shift(LEFT).shift(DOWN).scale(0.5)
        pnet1 = Circle(1, color=RED).shift(LEFT*2)
        pnet2 = Circle(1, color=BLUE).shift(RIGHT*2)
        pnet1_arrow = Arrow(start=LEFT*2, end=ORIGIN)
        pnet2_arrow = Arrow(start=RIGHT*2, end=ORIGIN)
        
        resolution_fa = 25
        self.camera.background_color = ManimColor.from_hex("#040c24")  
        axes = ThreeDAxes(x_range=(-20, 20, 1), y_range=(-20, 20, 1), z_range=(0, 20, 1))
        def param_trig(u, v, offset=(0,0), r_s=0.5):
            x = u
            y = v
            
            z = 2 * np.sqrt(r_s*(np.sqrt((x-offset[0])**2 + (y-offset[1])**2) - r_s))
            
            if np.isnan(z):
                return -5
            return z
        
        def param_trig_generator(A):
            return lambda u,v : param_trig(u,v)+param_trig(u,v,offset=A, r_s=0.05)
            

        
        trig_plane = axes.plot_surface(
            param_trig,
            resolution=(resolution_fa, resolution_fa),
            u_range = (-10, 10),
            v_range = (-10, 10),
            colorscale = [BLUE, GREEN],
        )
        
        trig_plane.set_style(fill_opacity=0)
        
        
        blackhole = Sphere(center=(0, 0, 1.4), radius=0.3, resolution=(18, 18), checkerboard_colors=False)
        blackhole.set_color(BLACK)
        
        blackhole_out = Sphere(center=(0, 0, 1.4), radius=0.31, resolution=(18, 18), checkerboard_colors=False)
        blackhole_out.set_color(BLUE)
        blackhole_out.set_style(fill_opacity=0.1)
        
        
        
        
        trajectory = Circle.from_three_points(axes.coords_to_point(3,3,0),axes.coords_to_point(-3,-3,0),axes.coords_to_point(3,-3,0))
        planet = Sphere(center=(0, 0, 1.4), radius=0.1, resolution=(18, 18), checkerboard_colors=False)
        planet.set_color(BLUE)
        
        ptracker = ValueTracker(0)
        planet.add_updater(
            lambda x: x.move_to([trajectory.point_from_proportion(ptracker.get_value() - math.floor(ptracker.get_value()))[0],trajectory.point_from_proportion(ptracker.get_value() - math.floor(ptracker.get_value()))[1],trajectory.point_from_proportion(ptracker.get_value() - math.floor(ptracker.get_value()))[2]+1.4])
        )
        
        def tempplane(x):
            s1 = axes.plot_surface(
                    param_trig_generator((planet.get_x(), planet.get_y())),
                    resolution=(resolution_fa, resolution_fa),
                    u_range = (-10, 10),
                    v_range = (-10, 10),
                    colorscale = [BLUE, GREEN],
                )
            s1.set_style(fill_opacity=0)
            return s1
            
        trig_plane.add_updater(
            lambda x: x.become(
                tempplane(x)
            )
        )
        
        self.play(FadeIn(title))
        self.next_slide()
        self.wipe(title)
        self.next_slide()
        self.play(Write(lyric1))
        self.next_slide()
        self.wipe(lyric1)
        self.play(Write(lyric2))
        self.next_slide()
        self.wipe(lyric2)
        
        self.play(Create(pnet1), Create(pnet2))
        self.play(Create(pnet1_arrow), Create(pnet2_arrow))
        
        self.play(Wiggle(pnet1_arrow), Wiggle(pnet2_arrow))
        self.next_slide()
        self.play(Write(newton))
        
        
        self.next_slide()
        phi, theta, focal_distance, gamma, zoom = self.camera.get_value_trackers()   
        print(phi.get_value(), theta.get_value(), focal_distance.get_value(), gamma.get_value(), zoom.get_value() )
        self.play(zoom.animate.set_value(3.7), phi.animate.set_value(30*DEGREES), theta.animate.set_value(30*DEGREES), Uncreate(pnet1_arrow), Uncreate(pnet2_arrow), pnet1.animate.scale(0.5),pnet2.animate.scale(0.5))
        EFE.set_opacity(0)
        self.add_fixed_in_frame_mobjects(EFE)
        
        self.play(Uncreate(pnet1), Uncreate(pnet2), Unwrite(newton), Create(axes))
        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(Create(blackhole), Create(blackhole_out))

        self.play(DrawBorderThenFill(trig_plane))
        self.play(DrawBorderThenFill(planet))

        self.play(Write(EFE), EFE.animate.set_opacity(1))

        #GOOD!
        
        self.next_slide(loop=True)
        self.play(ptracker.animate.set_value(2), run_time=10, rate_func=rate_functions.linear)
        
        
        self.next_slide()
        self.stop_ambient_camera_rotation()
        self.play(ptracker.animate.set_value(2.5), run_time=2.5, rate_func=rate_functions.ease_out_sine)
        SCHWART.set_opacity(0)
        self.add_fixed_in_frame_mobjects(SCHWART)
        
        daxes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
        )
        
        
        self.play(zoom.animate.set_value(1), phi.animate.set_value(0*DEGREES), theta.animate.set_value(-90*DEGREES), )
        self.play(Transform(EFE,SCHWART), SCHWART.animate.set_opacity(1), Transform(axes, daxes))
        def flamm(x):
            if abs(x) < 0.5:
                return 0
            else:
                return math.sqrt(0.5*(abs(x)-0.5))
        graph = daxes.plot(lambda x: flamm(x))
        self.play(ReplacementTransform(trig_plane,graph), Uncreate(planet), Uncreate(blackhole), Uncreate(blackhole_out))
        
        self.next_slide()
        
        ### SECTION 2 ### 다르게 해석하면, 이 특정거리에 존재하는 입자가 이 질량점으로부터 멀어지기 위한 탈출속도가 빛의 속도를 뛰어넘는다는것이였습니다. 이렇게 되면 질량점을 주변으로 빛도 빠져나오지 못하는 시공간속의 검정색 구멍이 생기게 됩니다. 이것이 블랙홀에 대한 최초의 예측이였습니다.
        
        
        particle = Circle(0.1).shift(UP*2).shift(LEFT*0.5)
        p_arrow = Arrow(start = UP*2+LEFT*0.5, end = UP*4+LEFT*2)
        self.play(Create(particle), Create(p_arrow))
        
        velocity = MathTex(r"v_{esc}").shift(UP*3).shift(LEFT*1.25).set_color(ORANGE)
        self.play(Write(velocity))
        vc_comp = MathTex(r"v_{esc} > c").shift(UP*3).shift(LEFT*1.25).set_color(ORANGE)
    
        self.play(Transform(velocity, vc_comp))
        
        self.next_slide()
        
        bh_png = ImageMobject("bh.png")
        self.play(GrowFromCenter(bh_png), Uncreate(graph), Uncreate(particle), Uncreate(p_arrow), Uncreate(velocity),Unwrite(SCHWART),Uncreate(axes))
        
        
        
        
        
        
        ### PARAGRAPH 2 ##
        
        #line = Line(start=LEFT*1.5+)
        
        

        
        
        
        
        
        
        # plane = NumberPlane()
        #self.play(FadeOut(planet), ptracker.animate.set_value(1.6), run_time=1,rate_func=rate_functions.linear)

        #ptracker.set_value(1.7)
        #self.play(FadeIn(planet),ptracker.animate.set_value(2.7), run_time=5, rate_func=rate_functions.linear)

        
        
        
        
        
        #