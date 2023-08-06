import numpy as np

c = 299792458

def model_DCB_p2c2_func(c2,p2c2_dcb):
    nsats=c2.shape[1]*1
    p2=c2*np.nan
    for i in range(nsats):
        p2[:,i]=c2[:,i]+p2c2_dcb[i]*c/1e9

    return p2
