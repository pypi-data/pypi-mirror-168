import numpy as np
from scipy import interpolate
from astropy import time
from astropy import units as u
from astropy import coordinates as coordastro
from astropy.utils import iers
iers.conf.auto_download = False
import ctypes
from numpy.ctypeslib import ndpointer
import matplotlib.pyplot as plt
c=299792458

def interp_SP3_GPS_C_func(gpstime,timep,sp3min,sp3interval,xsp3gcrs,ysp3gcrs,zsp3gcrs,ntimes,nsats,DLLPATH):

    lib=ctypes.CDLL(DLLPATH)
    lib.interp_sp3.restype = ctypes.c_double
    lib.interp_sp3.argtypes = [ndpointer(ctypes.c_double), ndpointer(ctypes.c_double), ndpointer(ctypes.c_double), ndpointer(ctypes.c_int), ndpointer(ctypes.c_double), (ctypes.c_int), (ctypes.c_int)]

    n=12
    aux=gpstime*1+np.zeros((ntimes,nsats))
    
    # plt.plot(aux)
    
    idsp3=(np.floor(1+(aux-sp3min)/sp3interval))#.astype(int)
    iobs=np.array(6+((aux-sp3min)/sp3interval)-idsp3,dtype=np.float64)
    itime=np.arange(0,n,1, dtype=np.float64)

    xs_intp=np.zeros((ntimes,nsats))
    ys_intp=np.zeros((ntimes,nsats))
    zs_intp=np.zeros((ntimes,nsats))

    for j in range(nsats):
        x=np.zeros(ntimes)
        y=np.zeros(ntimes)
        z=np.zeros(ntimes)
        
        xs_sp3=np.array(xsp3gcrs[:,j], dtype=np.float64)
        ys_sp3=np.array(ysp3gcrs[:,j], dtype=np.float64)
        zs_sp3=np.array(zsp3gcrs[:,j], dtype=np.float64)
        
        lib.interp_sp3(xs_sp3,np.array(iobs[:,j], dtype=np.float64),x,np.array(idsp3[:,j], dtype=np.int32),itime,ntimes,n)
        xs_intp[:,j]=x.copy()
        lib.interp_sp3(ys_sp3,np.array(iobs[:,j], dtype=np.float64),y,np.array(idsp3[:,j], dtype=np.int32),itime,ntimes,n)
        ys_intp[:,j]=y.copy()
        lib.interp_sp3(zs_sp3,np.array(iobs[:,j], dtype=np.float64),z,np.array(idsp3[:,j], dtype=np.int32),itime,ntimes,n)
        zs_intp[:,j]=z.copy()
    
    xs=xs_intp*1
    ys=ys_intp*1
    zs=zs_intp*1
    
    ctypes.windll.kernel32.FreeLibrary(lib._handle)

    cartrep = coordastro.CartesianRepresentation(xs, ys, zs, unit=u.m)
    epoch = time.Time(aux,format='gps',scale='tai')
    gcrs = coordastro.GCRS(cartrep, obstime=epoch)
    itrs = gcrs.transform_to(coordastro.ITRS(obstime=epoch))
    xs=itrs.x.value*1
    ys=itrs.y.value*1
    zs=itrs.z.value*1
    
    return xs, ys, zs#, aux, epoch
