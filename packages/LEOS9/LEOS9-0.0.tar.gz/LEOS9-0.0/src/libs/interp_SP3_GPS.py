import numpy as np
from scipy import interpolate
from astropy import time
from astropy import units as u
from astropy import coordinates as coordastro
from astropy.utils import iers
iers.conf.auto_download = False

c=299792458

class LagrangePoly:

    def __init__(self, X, Y):
        self.n = len(X)
        self.X = np.array(X)
        self.Y = np.array(Y)

    def basis(self, x, j):
        b = [(x - self.X[m]) / (self.X[j] - self.X[m])
             for m in range(self.n) if m != j]
        return np.prod(b, axis=0) * self.Y[j]

    def interpolate(self, x):
        b = [self.basis(x, j) for j in range(self.n)]
        return np.sum(b, axis=0)

def neville(x, y, x_int):
    n = x.size
    q = np.zeros((n, n - 1))
    q = np.concatenate((y[:, None], q), axis=1)
    for i in range(1, n):
        for j in range(1, i + 1):
            q[i, j] = ((x_int - x[i - j]) * q[i, j - 1] -
                       (x_int - x[i]) * q[i - 1, j - 1]) / (x[i] - x[i - j])

    y_int = q[n - 1, n - 1]
    return y_int#[y_int, q]

def interp_lagrange(t,gpstimesp3,xsp3,ysp3,zsp3):
    npoints=6
    idx=np.abs(t-gpstimesp3)<15*60*npoints
    itime=np.arange(len(gpstimesp3[idx]))
    f=interpolate.interp1d(gpstimesp3[idx], itime,'linear')
    iobs=f(t)
    lp = LagrangePoly(itime,xsp3[idx]); x=lp.interpolate(iobs)
    lp = LagrangePoly(itime,ysp3[idx]); y=lp.interpolate(iobs)
    lp = LagrangePoly(itime,zsp3[idx]); z=lp.interpolate(iobs)

    return x, y, z

def interp_SP3_GPS_func(gpstime,nsats,gpstimesp3,xsp3gcrs,ysp3gcrs,zsp3gcrs):
    xs_gcrs=gpstime*np.nan
    ys_gcrs=gpstime*np.nan
    zs_gcrs=gpstime*np.nan
    for i in range(gpstime.shape[0]):
        print(i)
        for j in range(gpstime.shape[1]):
            xs_gcrs[i,j],ys_gcrs[i,j],zs_gcrs[i,j]=interp_lagrange(gpstime[i,j], gpstimesp3, xsp3gcrs[:,j], ysp3gcrs[:,j], zsp3gcrs[:,j])

    xs=xs_gcrs*1
    ys=ys_gcrs*1
    zs=zs_gcrs*1
    # cartrep = coordastro.CartesianRepresentation(xs_gcrs, ys_gcrs, zs_gcrs, unit=u.m)
    # epoch = time.Time(gpstime,format='gps',scale='tai')
    # gcrs = coordastro.GCRS(cartrep, obstime=epoch)
    # itrs = gcrs.transform_to(coordastro.ITRS(obstime=epoch))
    # xs=itrs.x.value*1
    # ys=itrs.y.value*1
    # zs=itrs.z.value*1
    
    return xs, ys, zs
