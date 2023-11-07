from manim import *
import numpy as np
import math
import sys

from manim.utils.file_ops import open_file as open_media_file 

arg_arr = sys.argv[1:]

g_to_r = 0.0174533

t_val = []
u_val = []
P_val = []
y_val = []
x_val = []

v0 = float(arg_arr[1])
teta0 = float(arg_arr[0])
u = (v0 * math.cos(teta0 * g_to_r))
x = 0
y = 0
t = 0
H0 = 1
c = float(arg_arr[2])
teta = teta0
P = math.tan(teta*g_to_r)

dx = 0.5

def H(y):
    if y == 0:
        return 1
    else:
        if y > 15: y=15
        return ((20-y)/(20+y))

t_val.append(t)
u_val.append(u)
P_val.append(P)
y_val.append(y)
x_val.append(x)

while y>=0:
    det1 = dx*(1/u)
    deu1 = dx*(-c*H(y)*1.2)
    deP1 = dx*(-9.8/u**2)
    dey1 = dx*P

    det2 = dx*(1/(u+deu1/2))
    deu2 = dx*(-c*H(y+dey1/2)*0.85)
    deP2 = dx*(-9.8/(u+deu1/2)**2)
    dey2 = dx*(P+deP1/2)

    det3 = dx*(1/(u+deu2/2))
    deu3 = dx*(-c*H(y+dey2/2)*0.85)
    deP3 = dx*(-9.8/(u+deu2/2)**2)
    dey3 = dx*(P+deP2/2)

    det4 = dx*(1/(u+deu3))
    deu4 = dx*(-c*H(y+dey3)*0.85)
    deP4 = dx*(-9.8/(u+deu3)**2)
    dey4 = dx*(P+deP3)


    #-----------------
    t += (det1+2*det2+2*det3+det4)/6
    u += (deu1+2*deu2+2*deu3+deu4)/6
    P += (deP1+2*deP2+2*deP3+deP4)/6
    y += (dey1+2*dey2+2*dey3+dey4)/6

    t_val.append(t)
    u_val.append(u)
    P_val.append(P)
    y_val.append(y)
    x_val.append(x)

    x = x+dx

class BALListic_Graph(Scene):

    
    def construct(self):
        point_group = VGroup()
        plane = NumberPlane(
            x_range=(-2, 14, 1),
            y_range=(-2, 14, 1)
            )
        ax = Axes(
            x_range = [0, 2000, 250],
            y_range = [0, 2000, 250],
            x_length= 12,
            y_length=12,
            tips=False,
            axis_config={"include_numbers": True}
        )

        for i in range(len(x_val)):
            coef = 12/4000
            myx = (x_val[i])*coef-6
            myy = (y_val[i])*coef-6
            
            new_point = Dot(point=[myx, myy, 0], radius=0.08, color='#FF00FF', fill_opacity=1)
            point_group.add(new_point)
        
        self.play(Create(plane))
        self.wait()
        self.play(Create(ax))
        self.wait()
        self.play(Create(point_group), lag_ratio=2)
        self.wait(2)

        self.clear()

        self.add((plane))

        self.add((ax))

        self.add(point_group)



if __name__ == '__main__':
    scene = BALListic_Graph()
    scene.render() 

    open_media_file(scene.renderer.file_writer.movie_file_path)