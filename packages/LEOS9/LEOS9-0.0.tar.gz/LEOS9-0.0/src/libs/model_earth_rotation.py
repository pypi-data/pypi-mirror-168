import numpy as np

c = 299792458
we=7.2921151467E-5

def model_earth_rotation_func(r,xs,ys,zs):

    alfa=we*r/c
    XsRot=xs*np.cos(alfa) + ys*np.sin(alfa)
    YsRot=xs*-1*np.sin(alfa)+ys*np.cos(alfa)
    ZsRot=zs*1

    return XsRot, YsRot, ZsRot
