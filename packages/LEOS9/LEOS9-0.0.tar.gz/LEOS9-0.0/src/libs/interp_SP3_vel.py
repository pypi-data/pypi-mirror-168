import numpy as np
from scipy import interpolate
from scipy.interpolate import lagrange
from astropy import time
from astropy import units as u
from astropy import coordinates as coordastro
from astropy.utils import iers
iers.conf.auto_download = False

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
    
def interp_lagrange(t,gpstimesp3,xsp3,ysp3,zsp3):
    npoints=6
    idx=np.abs(t-gpstimesp3)<15*60*npoints
    itime=np.arange(len(gpstimesp3[idx]))
    f=interpolate.interp1d(gpstimesp3[idx], itime,'linear')
    iobs=f(t)
    # f =lagrange(itime,xsp3[idx]); x=f(iobs)*1
    # f =lagrange(itime,ysp3[idx]); y=f(iobs)*1
    # f =lagrange(itime,zsp3[idx]); z=f(iobs)*1
    lp = LagrangePoly(itime,xsp3[idx]); x=lp.interpolate(iobs)
    lp = LagrangePoly(itime,ysp3[idx]); y=lp.interpolate(iobs)
    lp = LagrangePoly(itime,zsp3[idx]); z=lp.interpolate(iobs)

    return x, y, z

def interp_SP3_vel_func(gpstime,ntimes,nsats,gpstimesp3,xsp3gcrs,ysp3gcrs,zsp3gcrs):
    ds=2
    xs_gcrs1=np.zeros((ntimes,nsats))*np.nan
    ys_gcrs1=np.zeros((ntimes,nsats))*np.nan
    zs_gcrs1=np.zeros((ntimes,nsats))*np.nan
    xs_gcrs2=np.zeros((ntimes,nsats))*np.nan
    ys_gcrs2=np.zeros((ntimes,nsats))*np.nan
    zs_gcrs2=np.zeros((ntimes,nsats))*np.nan
    for i in range(len(gpstime)):
        for j in range(nsats):
            xs_gcrs1[i,j],ys_gcrs1[i,j],zs_gcrs1[i,j]=interp_lagrange(gpstime[i,j]-ds/2, gpstimesp3, xsp3gcrs[:,j], ysp3gcrs[:,j], zsp3gcrs[:,j])
            xs_gcrs2[i,j],ys_gcrs2[i,j],zs_gcrs2[i,j]=interp_lagrange(gpstime[i,j]+ds/2, gpstimesp3, xsp3gcrs[:,j], ysp3gcrs[:,j], zsp3gcrs[:,j])
    
    vxs=xs_gcrs1*np.nan
    vys=xs_gcrs1*np.nan
    vzs=xs_gcrs1*np.nan
    epoch1 = time.Time(gpstime-ds/2,format='gps')
    epoch2 = time.Time(gpstime+ds/2,format='gps')

    cartrep1 = coordastro.CartesianRepresentation(xs_gcrs1, ys_gcrs1, zs_gcrs1, unit=u.m)
    gcrs1 = coordastro.GCRS(cartrep1, obstime=epoch1)
    itrs1 = gcrs1.transform_to(coordastro.ITRS(obstime=epoch1))
    cartrep2 = coordastro.CartesianRepresentation(xs_gcrs2, ys_gcrs2, zs_gcrs2, unit=u.m)
    gcrs2 = coordastro.GCRS(cartrep2, obstime=epoch2)
    itrs2 = gcrs2.transform_to(coordastro.ITRS(obstime=epoch2))

    vxs=(itrs2.x.value-itrs1.x.value)/ds
    vys=(itrs2.y.value-itrs1.y.value)/ds
    vzs=(itrs2.z.value-itrs1.z.value)/ds
    
    return vxs, vys, vzs
