import numpy as np

c=299792458

def interp_pco_cs_func(gpstime,pcox_cs,pcoy_cs,pcoz_cs):
    pcox=gpstime*np.nan
    pcoy=gpstime*np.nan
    pcoz=gpstime*np.nan
    for i in range(gpstime.shape[1]):
        pcox[:,i]=pcox_cs[i](gpstime[:,i])
        pcoy[:,i]=pcoy_cs[i](gpstime[:,i])
        pcoz[:,i]=pcoz_cs[i](gpstime[:,i])
        
    return pcox,pcoy,pcoz
