import numpy as np

c=299792458

def interp_SP3_cs_func(gpstime,nsats,xsp3_cs,ysp3_cs,zsp3_cs):
    xs=gpstime*np.nan
    ys=gpstime*np.nan
    zs=gpstime*np.nan
    for i in range(nsats):
        xs[:,i]=xsp3_cs[i](gpstime[:,i])
        ys[:,i]=ysp3_cs[i](gpstime[:,i])
        zs[:,i]=zsp3_cs[i](gpstime[:,i])
        
    return xs, ys, zs
