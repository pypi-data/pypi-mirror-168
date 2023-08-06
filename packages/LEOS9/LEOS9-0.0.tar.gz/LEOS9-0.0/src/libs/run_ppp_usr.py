import numpy as np
import libs.funclib as func

c=299792458
f1 = 1575.420*1e6
f2 = 1227.600*1e6

def run_ppp_usr_func(gpstime,P1,P2,relativity_gravity,xs,ys,zs,ntimes,nsats):
    
    xr=np.zeros((ntimes,nsats))*np.nan
    yr=np.zeros((ntimes,nsats))*np.nan
    zr=np.zeros((ntimes,nsats))*np.nan
    clkr=np.zeros((ntimes,nsats))*np.nan
    residual=np.zeros((ntimes,nsats))*np.nan
    pdop=np.zeros((ntimes))*np.nan
    nsat_curr=np.zeros((ntimes))*np.nan
    
    for itime in range(ntimes):#ntimes
        idx=(~np.isnan(P1[itime,:])) & (~np.isnan(P2[itime,:]))
        GPSTime=gpstime[itime]*1
        p1=P1[itime,idx]*1
        p2=P2[itime,idx]*1
        Xr0=0*1
        Yr0=0*1
        Zr0=0*1
        Xs0=xs[itime,idx]*1
        Ys0=ys[itime,idx]*1
        Zs0=zs[itime,idx]*1
        relativity=relativity_gravity[itime,idx]*1
    
        if(len(p1)<4): continue
    
        # Define Ionfree observations
        pIF = ( (f1**2)*p1 - (f2**2)*p2 ) / ((f1**2) - (f2**2))
        
        
        # Set vector of observations and Weight
        Lb= pIF*1
        
        for it in range(10):
            r0=np.sqrt((Xs0-Xr0)**2+(Ys0-Yr0)**2+(Zs0-Zr0)**2);
            pIF0=r0+relativity*1#+c*(Clkr0-Clks0)
            L0=pIF0*1
            L=L0-Lb
            # plt.plot(r0/1e3)
            # Set Size of Matrix during the Least Square Adjustment
            n=len(Lb)
            u=3#1+3
            A=np.zeros([n,u])
            
            # Include Receiver Position in the Design Matrix
            A[:,0]=-(Xs0-Xr0)/r0
            A[:,1]=-(Ys0-Yr0)/r0
            A[:,2]=-(Zs0-Zr0)/r0
            
            # Include Receiver Clock in the Design Matrix
            # A[:,3]=1
                
            # Least Square Adjustment
            N=np.dot(A.T, A)
            U=np.dot(A.T, L)
            invN=np.linalg.inv(N)
            X=np.dot(-invN,U)
            Ndop=np.dot(A.T, A)
            invNdop=np.linalg.inv(Ndop)
            PDOP=np.sqrt(np.sum(np.diag(invNdop)**2))
            
            # Update Initial Values of Receiver Position
            Xr0=Xr0+X[0]
            Yr0=Yr0+X[1]
            Zr0=Zr0+X[2]
            
            # Update Initial Values of Receiver Clock
            # Clkr0=Clkr0+X[3]/c
            
            # Update satellite position
            dist=np.sqrt((Xs0-Xr0)**2+(Ys0-Yr0)**2+(Zs0-Zr0)**2);

            latu0rad,lonu0rad,altu0=func.ecef2geodetic(Xr0, Yr0, Zr0)
            latu0=np.rad2deg(latu0rad)
            lonu0=np.rad2deg(lonu0rad)            
            if(np.abs(altu0)>100000): Xr0, Yr0, Zr0=func.geodetic2ecef(latu0rad, lonu0rad, 0)

        xr[itime,:]=Xr0*1
        yr[itime,:]=Yr0*1
        zr[itime,:]=Zr0*1
        clkr[itime,idx]=0*1
        xs[itime,idx]=Xs0*1
        ys[itime,idx]=Ys0*1
        zs[itime,idx]=Zs0*1
        residual[itime,idx]=pIF0-pIF
        pdop[itime]=PDOP*1
        nsat_curr[itime]=len(p1)
        
    return xr,yr,zr,clkr,residual,pdop,nsat_curr
