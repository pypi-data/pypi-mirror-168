import numpy as np

c = 299792458

def model_DCB_p1c1_func(c1,p1c1_dcb):
    nsats=c1.shape[1]*1
    p1=c1*np.nan
    for i in range(nsats):
        p1[:,i]=c1[:,i]+p1c1_dcb[i]*c/1e9

    return p1
