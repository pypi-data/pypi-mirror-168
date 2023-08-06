import numpy as np

c=299792458
smaj = 6378.137 #semimajor axis in km
smin = 6356.7523142 #semi minor axis in km
esq = 6.69437999014 * 0.001                                       
e1sq = 6.73949674228 * 0.001 
flat = 1 / 298.257223563 #flattening
REm = 6371211.266 #Earth's mean radius in meter

def run_ppp_initial_func(GPSTime,P1,P2,f1,f2,xsp3,ysp3,zsp3,clks,relativity_gravity):
    
    ntimes,nsats=GPSTime.shape

    xr=GPSTime*np.nan
    yr=GPSTime*np.nan
    zr=GPSTime*np.nan
    clkr=GPSTime*np.nan
    xs=GPSTime*np.nan
    ys=GPSTime*np.nan
    zs=GPSTime*np.nan
    residual=GPSTime*np.nan
    
    for itime in range(ntimes):
        idx=np.argwhere(~np.isnan(P1[itime,:]) & ~np.isnan(P2[itime,:]))
        idx=[int(idx[j][0]) for j in range(len(idx))]

        if(len(P1[itime,idx])<5):
            xr[itime,:]=np.nan
            yr[itime,:]=np.nan
            zr[itime,:]=np.nan
            clkr[itime,:]=np.nan
            xs[itime,:]=np.nan
            ys[itime,:]=np.nan
            zs[itime,:]=np.nan
            clks[itime,:]=np.nan
            residual[itime,:]=np.nan
            continue
        
        # Set Initial Parameters
        p1=P1[itime,idx]*1
        p2=P2[itime,idx]*1
        stdP=0.3
        Xr0=0
        Yr0=0
        Zr0=0
        Clkr0=0
        Xs0=xsp3[itime,idx]*1
        Ys0=ysp3[itime,idx]*1
        Zs0=zsp3[itime,idx]*1
        Clks0=clks[itime,idx]*1
        rel_grav=relativity_gravity[itime,idx]*1
        
        # Define Ionfree observations
        pIF = ( (f1**2)*p1 - (f2**2)*p2 ) / ((f1**2) - (f2**2))
        
        # Set vector of observations and Weight
        Lb= pIF*1
        P = pIF*0+1/(stdP**2)
        
        for it in range(5):
            r0=np.sqrt((Xs0-Xr0)**2+(Ys0-Yr0)**2+(Zs0-Zr0)**2)
            pIF0=r0+c*(Clkr0-Clks0)+rel_grav
            L0=pIF0*1
            L=L0-Lb
            
            # Set Size of Matrix during the Least Square Adjustment
            n=len(Lb)
            u=1+3
            A=np.zeros([n,u])
            AP=np.zeros([n,u])
            
            # Include Receiver Position in the Design Matrix
            A[:,0]=-(Xs0-Xr0)/r0
            A[:,1]=-(Ys0-Yr0)/r0
            A[:,2]=-(Zs0-Zr0)/r0
            
            # Include Receiver Clock in the Design Matrix
            A[:,3]=1
            
            # Weight
            for i in range(u):
                AP[:,i]=A[:,i]*P
                
            # Least Square Adjustment
            N=np.dot(AP.T, A)
            U=np.dot(AP.T, L)
            invN=np.linalg.inv(N)
            X=np.dot(-invN,U)
            
            # Update Initial Values of Receiver Position
            Xr0=Xr0+X[0]
            Yr0=Yr0+X[1]
            Zr0=Zr0+X[2]
            
            # Update Initial Values of Receiver Clock
            Clkr0=Clkr0+X[3]/c
            
            # Update remaining a priori information
            r0=np.sqrt((Xs0-Xr0)**2+(Ys0-Yr0)**2+(Zs0-Zr0)**2)
            pIF0=r0+c*(Clkr0-Clks0)

        xr[itime,:]=Xr0*1
        yr[itime,:]=Yr0*1
        zr[itime,:]=Zr0*1
        clkr[itime,idx]=Clkr0*1
        xs[itime,idx]=Xs0*1
        ys[itime,idx]=Ys0*1
        zs[itime,idx]=Zs0*1
        residual[itime,idx]=pIF0-pIF

    return xr,yr,zr,clkr,residual
