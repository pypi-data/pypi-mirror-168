import numpy as np
from scipy import interpolate

def interp_SP3_clks_func(gpstime,gpstimeclk5s,clk5s):
    
    clks=gpstime*np.nan
    for j in range(np.shape(gpstime)[1]):
        f=interpolate.interp1d(gpstimeclk5s[:,j], clk5s[:,j],'linear')
        idx=~np.isnan(gpstime[:,j])
        clks[idx,j]=f(gpstime[idx,j])
    
    return clks

#     idx=~np.isnan(clk5s[:,j])
#     f=np.poly1d(np.polyfit(gpstimeclk5s[idx,j], clk5s[idx,j], 3))