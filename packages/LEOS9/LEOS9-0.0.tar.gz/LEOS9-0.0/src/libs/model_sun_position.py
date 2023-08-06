import numpy as np
from scipy import interpolate
from scipy.interpolate import lagrange
from astropy import time
from astropy import units as u
from astropy import coordinates as coordastro
from astropy.utils import iers
iers.conf.auto_download = False

def model_sun_position_func(gpstime):
    
    x_sun=gpstime*np.nan
    y_sun=gpstime*np.nan
    z_sun=gpstime*np.nan
    idx=~np.isnan(gpstime)
    epoch = time.Time(gpstime[idx],format='gps')
    xyz_sun_gcrs=coordastro.get_sun(epoch)
    x=xyz_sun_gcrs.cartesian.x.value*149597870700
    y=xyz_sun_gcrs.cartesian.y.value*149597870700
    z=xyz_sun_gcrs.cartesian.z.value*149597870700
    cartrep = coordastro.CartesianRepresentation(x, y, z, unit=u.m)
    gcrs = coordastro.GCRS(cartrep, obstime=epoch)
    itrs = gcrs.transform_to(coordastro.ITRS(obstime=epoch))
    x_sun[idx]=itrs.x.value*1
    y_sun[idx]=itrs.y.value*1
    z_sun[idx]=itrs.z.value*1

    return x_sun, y_sun, z_sun
