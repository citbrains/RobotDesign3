#!/usr/bin/env python

import sys,os,time
from math import atan2,cos,sin,sqrt,degrees,radians

L =  120   #hand's length 
L1 = 300
L2 = 250
L3 = 160
L4 = 72

def send_angles(j,wait):
    with open("/run/shm/angles.tmp","w") as f:
        f.write("%d,%d,%d,%d,%d\n" % (j[0],j[1],j[2],j[3],j[4]))
        f.flush()
        
    os.rename("/run/shm/angles.tmp","/run/shm/angles")
    time.sleep(wait)

def air_toggle(flag,wait):
    with open("/run/shm/ev_on_off.tmp","w") as air_f:
        air_f.write("1\n" if flag else "0\n")
        air_f.flush()

    os.rename("/run/shm/ev_on_off.tmp","/run/shm/ev_on_off")
    time.sleep(wait)

def j_k(th1,th2,th3,th4,th5):
    th1,th2,th3,th4,th5 = radians(th1),radians(th2),radians(th3),radians(th4),radians(th5)
    x = cos(th1)*(L2*sin(th2)+L3*sin(th2+th3)+(L4+L)*sin(th2+th3+th4))
    y = sin(th1)*(L2*sin(th2)+L3*sin(th2+th3)+(L4+L)*sin(th2+th3+th4))
    z = L1+L2*cos(th2)+L3*cos(th2+th3)+(L4+L)*cos(th2+th3+th4)
    a = th1
    b = th2+th3+th4
    c = th5
    q = [x,y,z,degrees(a),degrees(b),degrees(c)]
    print(q)
    return q

def i_k(x,y,z,a,b,c,th1_flag,th3_flag):
    th1 = radians(a) * (1 if th1_flag else -1)
    th5 = radians(c)
    b = radians(b)
    cos3 = (((z-L1-(L4+L)*cos(b))**2+(((x-cos(th1)*(L4+L)*sin(b))**2)+(y-sin(th1)*(L4+L)*sin(b))**2))-L2**2-L3**2)/(2*L3*L2)
    sin3 = (1-cos3**2)**0.5 * (1 if th3_flag else -1)
    th3 = atan2(sin3,cos3)
    flaged_sign = 1 if (cos(th1)*x>=0 and sin(th1)*y>=0) else -1
    cos2 = ((z-L1-(L4+L)*cos(b))*(L2+L3*cos3)+flaged_sign*sqrt(((x-cos(th1)*(L4+L)*sin(b))**2)+(y-sin(th1)*(L4+L)*sin(b))**2)*L3*sin3)
    sin2 = (-(z-L1-(L4+L)*cos(b))*L3*sin3+flaged_sign*sqrt(((x-cos(th1)*(L4+L)*sin(b))**2)+(y-sin(th1)*(L4+L)*sin(b))**2)*(L2+L3*cos3)) * (1 if th1_flag else -1)
    th2 = atan2(sin2,cos2)
    th4 = b - th2 - th3
    th = [degrees(th1),degrees(th2),degrees(th3),degrees(th4),degrees(th5)] 
    print(th)
    return th

if __name__ == "__main__" :
    # air_toggle(True,2.0)
    # send_angles(i_k(0,0,L1+L2+L3+L4+L,0,0,8,True,True),3.0)
    # send_angles(i_k(269,0,291,0,180,8,True,True),1.0)
    # send_angles(i_k(338,0,262,0,140,8,True,True),2.0)
    # send_angles(i_k(368,0,250,0,100,8,True,True),2.0)
    # send_angles(i_k(389,0,180,0,90,8,True,True),2.0)
    # air_toggle(False,2.0)
    # send_angles(i_k(395,0,250,0,90,8,True,True),2.0)
    # send_angles(i_k(338,0,262,0,90,8,True,True),2.0)
    # send_angles(i_k(338,0,262,90,90,8,True,True),2.0)
    # send_angles(i_k(0,200,500,90,30,8,True,True),2.0)
    # send_angles(i_k(0,-482,300,90,-90,8,True,False),2.0)
    # send_angles(i_k(0,482,300,90,90,8,True,True),2.0)
    # air_toggle(True,2.0)

    air_toggle(True,2.0)
    send_angles(i_k(0,0,L1+L2+L3+L4+L,0,0,8,True,True),3.0)
    send_angles(i_k(270,0,170,0,180,8,True,True),3.0)
    send_angles(i_k(460,0,240,0,90,8,True,True),3.0)
    # send_angles(i_k(460,0,180,0,90,8,True,True),1.0)
    send_angles(i_k(460,0,100,0,90,8,True,True),3.0)
    air_toggle(False,2.0)
    send_angles(i_k(460,0,250,0,90,8,True,True),3.0)
    send_angles(i_k(0,460,250,90,90,8,True,True),3.0)
    send_angles(i_k(0,0,L1+L2+L3+L4+L,90,0,8,True,True),3.0)
    send_angles(i_k(0,-402,600,90,-90,8,True,False),2.0)
    send_angles(i_k(0,402,600,90,90,8,True,True),0.9)
    air_toggle(True,2.0)
