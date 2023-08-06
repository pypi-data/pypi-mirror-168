import numpy as np
import numpy.matlib
import georinex as gr
from astropy import time
from astropy import units as u
from astropy import coordinates as coordastro
from astropy.utils import iers
iers.conf.auto_download = False

nsatsGPS=32

def read_SP3_GPS_func(fnameprev,fnamecurr,fnamenext):
    
    gpstimesp3=[]; xsp3=[]; ysp3=[]; zsp3=[];
    for fname in [fnameprev,fnamecurr,fnamenext]:
        sp3=gr.load(fname)
        dates=sp3['time'].values
        xyz=sp3['position'].values
        gpstime=(dates-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
        x=xyz[:,:,0]*1e3
        y=xyz[:,:,1]*1e3
        z=xyz[:,:,2]*1e3
        
        if(len(xsp3)>0):
            gpstimesp3=np.append(gpstimesp3,gpstime)
            xsp3=np.vstack([xsp3,x])
            ysp3=np.vstack([ysp3,y])
            zsp3=np.vstack([zsp3,z])

        else:
            gpstimesp3=gpstime*1
            xsp3=x*1
            ysp3=y*1
            zsp3=z*1
            
    for i in range(32):
        x=xsp3[:,i]*1
        y=ysp3[:,i]*1
        z=zsp3[:,i]*1
       
        cartrep = coordastro.CartesianRepresentation(x, y, z, unit=u.m)
        epoch = time.Time(gpstimesp3,format='gps')
        itrs = coordastro.ITRS(cartrep, obstime=epoch)
        gcrs = itrs.transform_to(coordastro.GCRS(obstime=epoch))
        xsp3[:,i]=gcrs.cartesian.x.value*1
        ysp3[:,i]=gcrs.cartesian.y.value*1
        zsp3[:,i]=gcrs.cartesian.z.value*1
    
    return gpstimesp3, xsp3, ysp3, zsp3
