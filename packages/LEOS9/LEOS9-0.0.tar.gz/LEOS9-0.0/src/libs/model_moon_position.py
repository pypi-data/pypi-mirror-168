import numpy as np
from astropy import time
from astropy import units as u
from astropy import coordinates as coordastro
from astropy.utils import iers
iers.conf.auto_download = False

def model_moon_position_func(gpstime):
    
    x_moon=gpstime*np.nan
    y_moon=gpstime*np.nan
    z_moon=gpstime*np.nan
    idx=~np.isnan(gpstime)
    epoch = time.Time(gpstime[idx],format='gps')
    xyz_moon_gcrs=coordastro.get_moon(epoch)
    x=xyz_moon_gcrs.cartesian.x.value*1e3
    y=xyz_moon_gcrs.cartesian.y.value*1e3
    z=xyz_moon_gcrs.cartesian.z.value*1e3
    cartrep = coordastro.CartesianRepresentation(x, y, z, unit=u.m)
    gcrs = coordastro.GCRS(cartrep, obstime=epoch)
    itrs = gcrs.transform_to(coordastro.ITRS(obstime=epoch))
    x_moon[idx]=itrs.x.value*1
    y_moon[idx]=itrs.y.value*1
    z_moon[idx]=itrs.z.value*1

    return x_moon, y_moon, z_moon
