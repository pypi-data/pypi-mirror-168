import numpy as np

c=299792458
smaj = 6378.137 #semimajor axis in km
smin = 6356.7523142 #semi minor axis in km
esq = 6.69437999014 * 0.001                                       
e1sq = 6.73949674228 * 0.001 
flat = 1 / 298.257223563 #flattening
REm = 6371211.266 #Earth's mean radius in meter

def pps_brdc_GPS_initial(GPSTime,P1,P2,f1,f2,nav):
    
    ntimes,nsats=GPSTime.shape
    m0,deltaN,sqrta,eccentricity,omega,cuc,cus,crc,crs,io,idot,cic,cis,omega0,omegadot,tgd,toe,gpsweek,svclockbias,svclockdrift,svclockdriftrate,toc=nav
    xs0,ys0,zs0,clks0 = interp_brdc_GPS_itrs(GPSTime,m0,deltaN,sqrta,eccentricity,omega,cuc,cus,crc,crs,io,idot,cic,cis,omega0,omegadot,tgd,toe,gpsweek,svclockbias,svclockdrift,svclockdriftrate,toc)

    xr=GPSTime*np.nan
    yr=GPSTime*np.nan
    zr=GPSTime*np.nan
    clkr=GPSTime*np.nan
    xs=GPSTime*np.nan
    ys=GPSTime*np.nan
    zs=GPSTime*np.nan
    clks=GPSTime*np.nan
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
        Xs0=xs0[itime,idx]*1
        Ys0=ys0[itime,idx]*1
        Zs0=zs0[itime,idx]*1
        Clks0=clks0[itime,idx]*1
        gpstime=GPSTime[itime,idx]*1
        
        # Define Ionfree observations
        pIF = ( (f1**2)*p1 - (f2**2)*p2 ) / ((f1**2) - (f2**2))
        
        # Set vector of observations and Weight
        Lb= pIF*1
        P = pIF*0+1/(stdP**2)
        
        for it in range(5):
            r0=np.sqrt((Xs0-Xr0)**2+(Ys0-Yr0)**2+(Zs0-Zr0)**2)
            pIF0=r0+c*(Clkr0-Clks0)
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
            if(it>2):
                gpstime=GPSTime[itime,idx]-r0/c
                Xs0,Ys0,Zs0,Clks0 = interp_brdc_GPS_itrs(gpstime,m0[itime,idx],deltaN[itime,idx],sqrta[itime,idx],eccentricity[itime,idx],omega[itime,idx],cuc[itime,idx],cus[itime,idx],crc[itime,idx],crs[itime,idx],io[itime,idx],idot[itime,idx],cic[itime,idx],cis[itime,idx],omega0[itime,idx],omegadot[itime,idx],tgd[itime,idx],toe[itime,idx],gpsweek[itime,idx],svclockbias[itime,idx],svclockdrift[itime,idx],svclockdriftrate[itime,idx],toc[itime,idx])
        
        xr[itime,:]=Xr0*1
        yr[itime,:]=Yr0*1
        zr[itime,:]=Zr0*1
        clkr[itime,idx]=Clkr0*1
        xs[itime,idx]=Xs0*1
        ys[itime,idx]=Ys0*1
        zs[itime,idx]=Zs0*1
        clks[itime,idx]=Clks0*1
        residual[itime,idx]=pIF0-pIF

    return xr,yr,zr,clkr,xs,ys,zs,clks,residual

def pps_brdc_GPS_initial_gcrs(GPSTime,P1,P2,f1,f2,nav):
    
    ntimes,nsats=GPSTime.shape
    m0,deltaN,sqrta,eccentricity,omega,cuc,cus,crc,crs,io,idot,cic,cis,omega0,omegadot,tgd,toe,gpsweek,svclockbias,svclockdrift,svclockdriftrate,toc=nav
    xs0,ys0,zs0,clks0 = interp_brdc_GPS_gcrs(GPSTime,m0,deltaN,sqrta,eccentricity,omega,cuc,cus,crc,crs,io,idot,cic,cis,omega0,omegadot,tgd,toe,gpsweek,svclockbias,svclockdrift,svclockdriftrate,toc)

    xr=GPSTime*np.nan
    yr=GPSTime*np.nan
    zr=GPSTime*np.nan
    clkr=GPSTime*np.nan
    xs=GPSTime*np.nan
    ys=GPSTime*np.nan
    zs=GPSTime*np.nan
    clks=GPSTime*np.nan
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
        Xs0=xs0[itime,idx]*1
        Ys0=ys0[itime,idx]*1
        Zs0=zs0[itime,idx]*1
        Clks0=clks0[itime,idx]*1
        gpstime=GPSTime[itime,idx]*1
        
        # Define Ionfree observations
        pIF = ( (f1**2)*p1 - (f2**2)*p2 ) / ((f1**2) - (f2**2))
        
        # Set vector of observations and Weight
        Lb= pIF*1
        P = pIF*0+1/(stdP**2)
        
        for it in range(5):
            r0=np.sqrt((Xs0-Xr0)**2+(Ys0-Yr0)**2+(Zs0-Zr0)**2)
            pIF0=r0+c*(Clkr0-Clks0)
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
            if(it>2):
                gpstime=GPSTime[itime,idx]-r0/c
                Xs0,Ys0,Zs0,Clks0 = interp_brdc_GPS_gcrs(gpstime,m0[itime,idx],deltaN[itime,idx],sqrta[itime,idx],eccentricity[itime,idx],omega[itime,idx],cuc[itime,idx],cus[itime,idx],crc[itime,idx],crs[itime,idx],io[itime,idx],idot[itime,idx],cic[itime,idx],cis[itime,idx],omega0[itime,idx],omegadot[itime,idx],tgd[itime,idx],toe[itime,idx],gpsweek[itime,idx],svclockbias[itime,idx],svclockdrift[itime,idx],svclockdriftrate[itime,idx],toc[itime,idx])
        
        xr[itime,:]=Xr0*1
        yr[itime,:]=Yr0*1
        zr[itime,:]=Zr0*1
        clkr[itime,idx]=Clkr0*1
        xs[itime,idx]=Xs0*1
        ys[itime,idx]=Ys0*1
        zs[itime,idx]=Zs0*1
        clks[itime,idx]=Clks0*1
        residual[itime,idx]=pIF0-pIF

    return xr,yr,zr,clkr,xs,ys,zs,clks,residual

def pps_brdc_GPS_final_gcrs(GPSTime,P1,P2,f1,f2,nav,xr,yr,zr,clkr,xs,ys,zs,clks,elmask):
    
    ntimes,nsats=GPSTime.shape
    m0,deltaN,sqrta,eccentricity,omega,cuc,cus,crc,crs,io,idot,cic,cis,omega0,omegadot,tgd,toe,gpsweek,svclockbias,svclockdrift,svclockdriftrate,toc=nav
    elrad,azrad=xyz2azel(xr,yr,zr,xs,ys,zs)
    el=np.rad2deg(elrad)

    residual=GPSTime*np.nan
    ts=GPSTime*np.nan
    
    for itime in range(ntimes):
        idx=np.argwhere(~np.isnan(P1[itime,:]) & ~np.isnan(P2[itime,:]) & (el[itime,:]>=elmask))
        idx=[int(idx[j][0]) for j in range(len(idx))]
        
        if(len(P1[itime,idx])<5): 
            xr[itime,:]=np.nan
            yr[itime,:]=np.nan
            zr[itime,:]=np.nan
            clkr[itime,:]=np.nan
            ts[itime,:]=np.nan
            xs[itime,:]=np.nan
            ys[itime,:]=np.nan
            zs[itime,:]=np.nan
            clks[itime,:]=np.nan
            residual[itime,:]=np.nan
            continue

        idx_el=el[itime,:]<elmask
        xr[itime,idx_el]=np.nan
        yr[itime,idx_el]=np.nan
        zr[itime,idx_el]=np.nan
        clkr[itime,idx_el]=np.nan
        ts[itime,idx_el]=np.nan
        xs[itime,idx_el]=np.nan
        ys[itime,idx_el]=np.nan
        zs[itime,idx_el]=np.nan
        clks[itime,idx_el]=np.nan
        residual[itime,idx_el]=np.nan
        
        # Set Initial Parameters
        p1=P1[itime,idx]*1
        p2=P2[itime,idx]*1
        stdP=0.3
        Xr0=xr[itime,idx][0]
        Yr0=yr[itime,idx][0]
        Zr0=zr[itime,idx][0]
        Clkr0=clkr[itime,idx][0]
        Xs0=xs[itime,idx]*1
        Ys0=ys[itime,idx]*1
        Zs0=zs[itime,idx]*1
        Clks0=clks[itime,idx]*1
        gpstime=GPSTime[itime,idx]*1
        
        # Define Ionfree observations
        pIF = ( (f1**2)*p1 - (f2**2)*p2 ) / ((f1**2) - (f2**2))
        
        # Set vector of observations and Weight
        Lb= pIF*1
        P = pIF*0+1/(stdP**2)
        
        for it in range(5):
            r0=np.sqrt((Xs0-Xr0)**2+(Ys0-Yr0)**2+(Zs0-Zr0)**2);
            pIF0=r0+c*(Clkr0-Clks0)
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
            if(it>2):
                gpstime=GPSTime[itime,idx]-r0/c
                Xs0,Ys0,Zs0,Clks0 = interp_brdc_GPS_itrs(gpstime,m0[itime,idx],deltaN[itime,idx],sqrta[itime,idx],eccentricity[itime,idx],omega[itime,idx],cuc[itime,idx],cus[itime,idx],crc[itime,idx],crs[itime,idx],io[itime,idx],idot[itime,idx],cic[itime,idx],cis[itime,idx],omega0[itime,idx],omegadot[itime,idx],tgd[itime,idx],toe[itime,idx],gpsweek[itime,idx],svclockbias[itime,idx],svclockdrift[itime,idx],svclockdriftrate[itime,idx],toc[itime,idx])
        
        xr[itime,:]=Xr0*1
        yr[itime,:]=Yr0*1
        zr[itime,:]=Zr0*1
        clkr[itime,:]=Clkr0*1
        ts[itime,idx]=gpstime*1
        xs[itime,idx]=Xs0*1
        ys[itime,idx]=Ys0*1
        zs[itime,idx]=Zs0*1
        clks[itime,idx]=Clks0*1
        residual[itime,idx]=pIF0-pIF

    return xr,yr,zr,clkr,xs,ys,zs,ts,clks,residual

def pps_brdc_GPS_filter(GPSTime,P1,P2,f1,f2,nav,xr,yr,zr,clkr,xs,ys,zs,clks,elmask,residual):
    
    ntimes,nsats=GPSTime.shape
    m0,deltaN,sqrta,eccentricity,omega,cuc,cus,crc,crs,io,idot,cic,cis,omega0,omegadot,tgd,toe,gpsweek,svclockbias,svclockdrift,svclockdriftrate,toc=nav
    elrad,azrad=xyz2azel(xr,yr,zr,xs,ys,zs)
    el=np.rad2deg(elrad)

    for itime in range(ntimes):
        idx_core=np.argwhere(~np.isnan(P1[itime,:]) & ~np.isnan(P2[itime,:]) & (el[itime,:]>=elmask))
        if(len(P1[itime,idx_core])<5): continue
        if(np.abs(residual[itime,idx_core]).max()<100): continue
        
        for iidx in range(len(idx_core)):
            idx=[int(idx_core[j][0]) for j in range(len(idx_core))]
            idx.pop(iidx)
            
            # Set Initial Parameters
            p1=P1[itime,idx]*1
            p2=P2[itime,idx]*1
            stdP=0.3
            Xr0=xr[itime,idx][0]
            Yr0=yr[itime,idx][0]
            Zr0=zr[itime,idx][0]
            Clkr0=clkr[itime,idx][0]
            Xs0=xs[itime,idx]*1
            Ys0=ys[itime,idx]*1
            Zs0=zs[itime,idx]*1
            Clks0=clks[itime,idx]*1
            gpstime=GPSTime[itime,idx]*1
            
            # Define Ionfree observations
            pIF = ( (f1**2)*p1 - (f2**2)*p2 ) / ((f1**2) - (f2**2))
            
            # Set vector of observations and Weight
            Lb= pIF*1
            P = pIF*0+1/(stdP**2)
            
            for it in range(5):
                r0=np.sqrt((Xs0-Xr0)**2+(Ys0-Yr0)**2+(Zs0-Zr0)**2);
                pIF0=r0+c*(Clkr0-Clks0)
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
                if(it>2):
                    gpstime=GPSTime[itime,idx]-r0/c
                    Xs0,Ys0,Zs0,Clks0 = interp_brdc_GPS_itrs(gpstime,m0[itime,idx],deltaN[itime,idx],sqrta[itime,idx],eccentricity[itime,idx],omega[itime,idx],cuc[itime,idx],cus[itime,idx],crc[itime,idx],crs[itime,idx],io[itime,idx],idot[itime,idx],cic[itime,idx],cis[itime,idx],omega0[itime,idx],omegadot[itime,idx],tgd[itime,idx],toe[itime,idx],gpsweek[itime,idx],svclockbias[itime,idx],svclockdrift[itime,idx],svclockdriftrate[itime,idx],toc[itime,idx])
        
            res=pIF0-pIF
            
            if(np.abs(res).max()<15): 
                P1[itime,idx_core[iidx]]=np.nan
                P2[itime,idx_core[iidx]]=np.nan
                break
            
            if(iidx==len(idx_core)-1):
                idx_res=np.nanargmax(np.abs(residual[itime,idx_core]))
                P1[itime,idx_core[idx_res]]=np.nan
                P2[itime,idx_core[idx_res]]=np.nan
                break

    return P1,P2

def pps_brdc_GPS_final(GPSTime,P1,P2,f1,f2,nav,xr,yr,zr,clkr,xs,ys,zs,clks,elmask):
    
    ntimes,nsats=GPSTime.shape
    m0,deltaN,sqrta,eccentricity,omega,cuc,cus,crc,crs,io,idot,cic,cis,omega0,omegadot,tgd,toe,gpsweek,svclockbias,svclockdrift,svclockdriftrate,toc=nav
    elrad,azrad=xyz2azel(xr,yr,zr,xs,ys,zs)
    el=np.rad2deg(elrad)

    residual=GPSTime*np.nan
    ts=GPSTime*np.nan
    
    for itime in range(ntimes):
        idx=np.argwhere(~np.isnan(P1[itime,:]) & ~np.isnan(P2[itime,:]) & (el[itime,:]>=elmask))
        idx=[int(idx[j][0]) for j in range(len(idx))]
        
        if(len(P1[itime,idx])<5): 
            xr[itime,:]=np.nan
            yr[itime,:]=np.nan
            zr[itime,:]=np.nan
            clkr[itime,:]=np.nan
            ts[itime,:]=np.nan
            xs[itime,:]=np.nan
            ys[itime,:]=np.nan
            zs[itime,:]=np.nan
            clks[itime,:]=np.nan
            residual[itime,:]=np.nan
            continue

        idx_el=el[itime,:]<elmask
        xr[itime,idx_el]=np.nan
        yr[itime,idx_el]=np.nan
        zr[itime,idx_el]=np.nan
        clkr[itime,idx_el]=np.nan
        ts[itime,idx_el]=np.nan
        xs[itime,idx_el]=np.nan
        ys[itime,idx_el]=np.nan
        zs[itime,idx_el]=np.nan
        clks[itime,idx_el]=np.nan
        residual[itime,idx_el]=np.nan
        
        # Set Initial Parameters
        p1=P1[itime,idx]*1
        p2=P2[itime,idx]*1
        stdP=0.3
        Xr0=xr[itime,idx][0]
        Yr0=yr[itime,idx][0]
        Zr0=zr[itime,idx][0]
        Clkr0=clkr[itime,idx][0]
        Xs0=xs[itime,idx]*1
        Ys0=ys[itime,idx]*1
        Zs0=zs[itime,idx]*1
        Clks0=clks[itime,idx]*1
        gpstime=GPSTime[itime,idx]*1
        
        # Define Ionfree observations
        pIF = ( (f1**2)*p1 - (f2**2)*p2 ) / ((f1**2) - (f2**2))
        
        # Set vector of observations and Weight
        Lb= pIF*1
        P = pIF*0+1/(stdP**2)
        
        for it in range(5):
            r0=np.sqrt((Xs0-Xr0)**2+(Ys0-Yr0)**2+(Zs0-Zr0)**2);
            pIF0=r0+c*(Clkr0-Clks0)
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
            if(it>2):
                gpstime=GPSTime[itime,idx]-r0/c
                Xs0,Ys0,Zs0,Clks0 = interp_brdc_GPS_itrs(gpstime,m0[itime,idx],deltaN[itime,idx],sqrta[itime,idx],eccentricity[itime,idx],omega[itime,idx],cuc[itime,idx],cus[itime,idx],crc[itime,idx],crs[itime,idx],io[itime,idx],idot[itime,idx],cic[itime,idx],cis[itime,idx],omega0[itime,idx],omegadot[itime,idx],tgd[itime,idx],toe[itime,idx],gpsweek[itime,idx],svclockbias[itime,idx],svclockdrift[itime,idx],svclockdriftrate[itime,idx],toc[itime,idx])
        
        xr[itime,:]=Xr0*1
        yr[itime,:]=Yr0*1
        zr[itime,:]=Zr0*1
        clkr[itime,:]=Clkr0*1
        ts[itime,idx]=gpstime*1
        xs[itime,idx]=Xs0*1
        ys[itime,idx]=Ys0*1
        zs[itime,idx]=Zs0*1
        clks[itime,idx]=Clks0*1
        residual[itime,idx]=pIF0-pIF

    return xr,yr,zr,clkr,xs,ys,zs,ts,clks,residual

def interp_brdc_GPS_itrs(GPSTime,M0,DeltaN,sqrtA,Eccentricity,omega,Cuc,Cus,Crc,Crs,Io,IDOT,Cic,Cis,Omega0,OmegaDot,TGD,Toe,GPSWeek,SVclockBias,SVclockDrift,SVclockDriftRate,Toc):
    # Constants
    GM = 3.986005e14;
    cr = 6.283185307179600; # CIRCLE_RAD;
    Omegae_dot = 7.2921151467e-5; # angular velocity of the Earth rotation [rad/s]
    
    # Parameters for satellite positions
    M0        = M0*1;
    deltan    = DeltaN*1;
    roota     = sqrtA*1;
    ecc       = Eccentricity*1;
    omega     = omega*1;
    cuc       = Cuc*1;
    cus       = Cus*1;
    crc       = Crc*1;
    crs       = Crs*1;
    i0        = Io*1;
    IDOT      = IDOT*1;
    cic       = Cic*1;
    cis       = Cis*1;
    Omega0    = Omega0*1;
    Omega_dot = OmegaDot*1;
    tgd       = TGD*1;
    toe       = Toe*1;
    time_eph  = GPSWeek*7*86400 + Toe;
    t         = GPSTime*1;

    # Parameters for clocks
    af0     = SVclockBias*1;
    af1     = SVclockDrift*1;
    af2     = SVclockDriftRate*1;
    ref_toc = Toc*1;
    
    # Calculations
    A  = roota*roota;              # semi-major axis
    tk=  check_t(t - time_eph);    # time from the ephemerides reference epoch
    n0 = np.sqrt(GM/(A**3));       # computed mean motion [rad/sec]
    n  = n0 + deltan;              # corrected mean motion [rad/sec]
    Mk = M0 + n*tk;                # mean anomaly
    Mk = np.fmod(Mk+cr,cr);
    Ek = Mk*1;
    
    max_iter = 12;
    for i in range(1,max_iter+1,1):
        Ek_old = Ek*1;
        Ek = Mk+ecc*np.sin(Ek);
        dEk = np.fmod(Ek-Ek_old,cr);
        dEkNoNan=dEk[~np.isnan(dEk)];
        treshold=np.where(np.abs(dEkNoNan)>1e-12); treshold=treshold[0];
        if len(treshold)==0:
            break
        
        if i==12:
            print('WARNING: Eccentric anomaly does not converge.')
            
    Ek = np.fmod(Ek+cr,cr);
    tk = check_t(t - time_eph);  #time from the ephemeris reference epoch
    
    fk = np.arctan2(np.sqrt(1-ecc*ecc)*np.sin(Ek), np.cos(Ek) - ecc); # true anomaly
    phik = fk + omega; # argument of latitude
    phik = np.fmod(phik,cr);
    
    uk = phik + cuc*np.cos(2*phik) + cus*np.sin(2*phik); # corrected argument of latitude
    rk = A*(1 - ecc*np.cos(Ek)) + crc*np.cos(2*phik) + crs*np.sin(2*phik); # corrected radial distance
    ik = i0 + IDOT*tk + cic*np.cos(2*phik) + cis*np.sin(2*phik); # corrected inclination of the orbital plane
    
    # satellite positions in the orbital plane
    x1k = np.cos(uk)*rk;
    y1k = np.sin(uk)*rk;
    
    # corrected longitude of the ascending node
    Omegak = Omega0 + (Omega_dot - Omegae_dot)*tk - Omegae_dot*toe;
    Omegak = np.fmod(Omegak + cr, cr);
    
    # satellite Earth-fixed coordinates (X,Y,Z)
    xk = x1k*np.cos(Omegak) - y1k*np.cos(ik)*np.sin(Omegak);
    yk = x1k*np.sin(Omegak) + y1k*np.cos(ik)*np.cos(Omegak);
    zk = y1k*np.sin(ik);
    
    # Interpolation of clocks for the given GPSTime
    dt   = check_t(GPSTime - ref_toc);
    clks = (af2*dt + af1)*dt + af0;
    
    # Relativity calculation
    Relativity = -4.442807633e-10 * ecc * roota * np.sin(Ek);
    
    # Clks correction from relativity and tgd
    clks=clks+Relativity-tgd;
    
    return xk, yk, zk, clks

def interp_brdc_GPS_gcrs(GPSTime,M0,DeltaN,sqrtA,Eccentricity,omega,Cuc,Cus,Crc,Crs,Io,IDOT,Cic,Cis,Omega0,OmegaDot,TGD,Toe,GPSWeek,SVclockBias,SVclockDrift,SVclockDriftRate,Toc):
    # Constants
    GM = 3.986005e14;
    cr = 6.283185307179600; # CIRCLE_RAD;
    Omegae_dot = 7.2921151467e-5; # angular velocity of the Earth rotation [rad/s]
    Omegae_dot=0
    
    # Parameters for satellite positions
    M0        = M0*1;
    deltan    = DeltaN*1;
    roota     = sqrtA*1;
    ecc       = Eccentricity*1;
    omega     = omega*1;
    cuc       = Cuc*1;
    cus       = Cus*1;
    crc       = Crc*1;
    crs       = Crs*1;
    i0        = Io*1;
    IDOT      = IDOT*1;
    cic       = Cic*1;
    cis       = Cis*1;
    Omega0    = Omega0*1;
    Omega_dot = OmegaDot*1;
    tgd       = TGD*1;
    toe       = Toe*1;
    time_eph  = GPSWeek*7*86400 + Toe;
    t         = GPSTime*1;
    
    # Parameters for clocks
    af0     = SVclockBias*1;
    af1     = SVclockDrift*1;
    af2     = SVclockDriftRate*1;
    ref_toc = Toc*1;
    
    # Calculations
    A  = roota*roota;              # semi-major axis
    tk=  check_t(t - time_eph);    # time from the ephemerides reference epoch
    n0 = np.sqrt(GM/(A**3));       # computed mean motion [rad/sec]
    n  = n0 + deltan;              # corrected mean motion [rad/sec]
    Mk = M0 + n*tk;                # mean anomaly
    Mk = np.fmod(Mk+cr,cr);
    Ek = Mk*1;
    
    max_iter = 12;
    for i in range(1,max_iter+1,1):
        Ek_old = Ek*1;
        Ek = Mk+ecc*np.sin(Ek);
        dEk = np.fmod(Ek-Ek_old,cr);
        dEkNoNan=dEk[~np.isnan(dEk)];
        treshold=np.where(np.abs(dEkNoNan)>1e-12); treshold=treshold[0];
        if len(treshold)==0:
            break
        
        if i==12:
            print('WARNING: Eccentric anomaly does not converge.')
            
    Ek = np.fmod(Ek+cr,cr);
    tk = check_t(t - time_eph);  #time from the ephemeris reference epoch
    
    fk = np.arctan2(np.sqrt(1-ecc*ecc)*np.sin(Ek), np.cos(Ek) - ecc); # true anomaly
    phik = fk + omega; # argument of latitude
    phik = np.fmod(phik,cr);
    
    uk = phik + cuc*np.cos(2*phik) + cus*np.sin(2*phik); # corrected argument of latitude
    rk = A*(1 - ecc*np.cos(Ek)) + crc*np.cos(2*phik) + crs*np.sin(2*phik); # corrected radial distance
    ik = i0 + IDOT*tk + cic*np.cos(2*phik) + cis*np.sin(2*phik); # corrected inclination of the orbital plane
    
    # satellite positions in the orbital plane
    x1k = np.cos(uk)*rk;
    y1k = np.sin(uk)*rk;
    
    # corrected longitude of the ascending node
    Omegak = Omega0 + (Omega_dot - Omegae_dot)*tk - Omegae_dot*toe;
    Omegak = np.fmod(Omegak + cr, cr);
    
    # satellite Earth-fixed coordinates (X,Y,Z)
    xk = x1k*np.cos(Omegak) - y1k*np.cos(ik)*np.sin(Omegak);
    yk = x1k*np.sin(Omegak) + y1k*np.cos(ik)*np.cos(Omegak);
    zk = y1k*np.sin(ik);
    
    # Interpolation of clocks for the given GPSTime
    dt   = check_t(GPSTime - ref_toc);
    clks = (af2*dt + af1)*dt + af0;
    
    # Relativity calculation
    Relativity = -4.442807633e-10 * ecc * roota * np.sin(Ek);
    
    # Clks correction from relativity and tgd
    clks=clks+Relativity-tgd;
    
    return xk, yk, zk, clks

def check_t(time):
    #Function accounting for beginning or end of week crossover (not doing anything for now)
    # half_week = 302400;     # seconds
    corrTime = time*1;
    return corrTime

def xyz2azel(sx,sy,sz,x,y,z):

    [lat,lon,h]=ecef2geodetic(sx,sy,sz);
    dx=x-sx;
    dy=y-sy;
    dz=z-sz;
    
    dn = (-(np.sin(lat)*np.cos(lon))*dx) - ((np.sin(lat)*np.sin(lon))*dy) + (np.cos(lat)*dz);
    de = ((-np.sin(lon)*dx)+(np.cos(lon))*dy);
    du = (((np.cos(lat)*np.cos(lon)))*dx) + ((np.cos(lat)*np.sin(lon))*dy) + (np.sin(lat)*dz);
    
    ro = np.sqrt(de*de + dn*dn);
    
    az=np.arctan(de/dn);
    el=np.arctan(du/ro);
    
    # checking of the quadrant
    with np.errstate(invalid='ignore'):
        az[(de>0) & (dn<0)] =   np.pi - abs(az[(de>0) & (dn<0)]);
        az[(de<0) & (dn<0)] =   np.pi + abs(az[(de<0) & (dn<0)]);
        az[(de<0) & (dn>0)] = 2*np.pi - abs(az[(de<0) & (dn>0)]);
        az[az<0]    = 2*np.pi + az[az<0];
        az[az>2*np.pi] = az[az>2*np.pi] - 2*np.pi
    
    return el,az


def ecef2geodetic(x, y, z):
    x = x/1000. #km
    y = y/1000. #km
    z = z/1000. #km   
    r = np.sqrt(x **2 + y **2)
    Esq = smaj **2 - smin **2
    F = 54 * smin **2 * z **2
    G = r **2 + (1 - esq) * z **2 - esq * Esq
    C = (esq **2 * F * r **2) / (np.power(G, 3))
    S = np.sqrt(1 + C + np.sqrt(C **2 + 2 * C))
    P = F / (3 * np.power((S + 1 / S + 1), 2) * G **2)
    Q = np.sqrt(1 + 2 * esq **2 * P)
    r_0 =  (-(P * esq * r) / (1 + Q) + np.sqrt(0.5 * smaj **2 *(1 + 1.0 / Q) -  P * (1 - esq) * z **2 / (Q * (1 + Q)) - 0.5 * P * r **2))
    U = np.sqrt(np.power((r - esq * r_0), 2) + z **2)
    V = np.sqrt(np.power((r - esq * r_0), 2) + (1 - esq) * z **2)
    Z_0 = smin **2 * z / (smaj * V)
    h = U * (1 - smin **2 / (smaj * V))
    lat = np.arctan((z + e1sq * Z_0) / r)
    lon = np.arctan2(y, x)
    return lat, lon, h*1000.
