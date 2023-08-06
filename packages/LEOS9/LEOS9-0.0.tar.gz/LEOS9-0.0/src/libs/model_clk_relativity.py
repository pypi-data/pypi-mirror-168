import numpy as np

c = 299792458
we=7.2921151467E-5

def model_clk_relativity_func(xs,ys,zs,vxs,vys,vzs,ntimes,nsats):

    RelativitySP3=xs*np.nan
    for i in range(ntimes):
        for j in range(nsats):
            position=np.array((xs[i,j],ys[i,j],zs[i,j]))
            velocity=np.array((vxs[i,j],vys[i,j],vzs[i,j]))
            RelativitySP3[i,j]=-2*np.dot(position,velocity)/(float(c)**2)

    return RelativitySP3
