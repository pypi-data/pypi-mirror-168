import numpy as np

nsatsGPS=32
c = 299792458

def positioning_code_SP3_func(gpstime,pIF,xs,ys,zs,clks):

    idxobs=(~np.isnan(pIF)) & (~np.isnan(xs)) & (~np.isnan(clks))
    GPSTime=gpstime[idxobs]*1
    Xr0=0
    Yr0=0
    Zr0=0
    Clkr0=xs[idxobs]*0
    Xs0=xs[idxobs]*1
    Ys0=ys[idxobs]*1
    Zs0=zs[idxobs]*1
    Clks0=clks[idxobs]*1
    PIF=pIF[idxobs]*1

    uniquetimes=np.unique(GPSTime)

    Lb= PIF*1    
    nobs=len(PIF)
    npar=len(uniquetimes)*1+3
    for it_pos in range(10):
        print(it_pos)
        A=np.zeros([nobs,npar])
        r0=np.sqrt((Xs0-Xr0)**2+(Ys0-Yr0)**2+(Zs0-Zr0)**2)
        L0=r0+c*(Clkr0-Clks0)
        L=L0-Lb
        
        k=0
        A[:,k+0]=-(Xs0-Xr0)/r0
        A[:,k+1]=-(Ys0-Yr0)/r0
        A[:,k+2]=-(Zs0-Zr0)/r0
        k=k+3
        for i in range(0,len(uniquetimes),1):
            idx=GPSTime==uniquetimes[i]
            A[idx,k]=1
            k=k+1
            
        # Least Square Adjustment
        N=np.dot(A.T, A)
        U=np.dot(A.T, L)
        invN=np.linalg.inv(N)
        X=np.dot(-invN,U)
        
        k=0
        Xr0=Xr0+X[k+0]
        Yr0=Yr0+X[k+1]
        Zr0=Zr0+X[k+2]
        k=k+3
        for i in range(0,len(uniquetimes),1):
            idx=GPSTime==uniquetimes[i]
            Clkr0[idx]=Clkr0[idx]+X[k]/c
            k=k+1

    clkr=xs*np.nan
    residual=xs*np.nan
    xr=Xr0+xs*0
    yr=Yr0+xs*0
    zr=Zr0+xs*0
    clkr[idxobs]=Clkr0*1
    residual[idxobs]=L0-Lb
    
    return xr, yr, zr, clkr, residual
