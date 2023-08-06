import numpy as np

nsatsGPS=32
c = 299792458

def positioning_phase_SP3_MeanTropo_kin_func(gpstime,lIF,windup,pcv_sat,relativity_gravity,xs,ys,zs,clks,tropo_dry,mfunc_tropo,el,elmask,Flags,gpstime_day):

    hrinit=8
    hrend=20

    idxobs=(~np.isnan(lIF)) & (~np.isnan(xs)) & (~np.isnan(clks)) & (el>=elmask) & (~np.isnan(Flags)) & ((gpstime-gpstime_day)/3600>hrinit) & ((gpstime-gpstime_day)/3600<hrend)
    GPSTime=gpstime[idxobs]*1
    Xr0=gpstime[idxobs]*0
    Yr0=gpstime[idxobs]*0
    Zr0=gpstime[idxobs]*0
    Clkr0=gpstime[idxobs]*0
    Xs0=xs[idxobs]*1
    Ys0=ys[idxobs]*1
    Zs0=zs[idxobs]*1
    Clks0=clks[idxobs]*1
    LIF=lIF[idxobs]*1
    tropo0=xs[idxobs]*0
    Tropo_dry=tropo_dry[idxobs]*1
    mtropo=mfunc_tropo[idxobs]*1
    amb0=lIF[idxobs]*0
    flags=Flags[idxobs]*1
    Windup=windup[idxobs]*1
    Relativity_gravity=relativity_gravity[idxobs]*1
    elevation=el[idxobs]*1
    PCV_sat=pcv_sat[idxobs]*1

    uniquetimes=np.unique(GPSTime)
    uniqueflags=np.unique(flags)

    Lb= LIF*1    
    # stdL=0.003*np.cos(np.deg2rad(elevation))**2
    stdL=(0.003*3)**2+(0.003*3/np.sin(np.deg2rad(elevation)))**2
    injTrop=0.25
    stdinjTrop=1e-4
    
    P = LIF*0+1/(stdL**2)
    tmin=GPSTime.min()
    tmax=GPSTime.max()
    dtime=1*3600
    npartropo=int(np.round(1+(tmax-tmin)/dtime))

    nobs=len(LIF)
    npar=len(uniquetimes)*4-1+npartropo+len(uniqueflags)
    X=np.zeros([npar])
    XX=np.zeros([npar])
    for it_pos in range(10):
        print(it_pos)
        A=np.zeros([nobs,npar])
        AP=np.zeros([nobs,npar])
        
        r0=np.sqrt((Xs0-Xr0)**2+(Ys0-Yr0)**2+(Zs0-Zr0)**2)
        L0=r0+c*(Clkr0-Clks0)+Tropo_dry+tropo0*mtropo+amb0+Windup+Relativity_gravity+PCV_sat
        L=L0-Lb

        Ai=np.zeros([npar,npar])
        Pi=np.zeros([npar])+1
        AiP=np.zeros([npar,npar])
        Lbi=np.zeros([npar])
        L0i=np.zeros([npar])
        for i in range(npar): Ai[i,i]=1

        k=0
        idx=GPSTime==uniquetimes[0]
        A[idx,k+0]=-(Xs0[idx]-Xr0[idx])/r0[idx]
        A[idx,k+1]=-(Ys0[idx]-Yr0[idx])/r0[idx]
        A[idx,k+2]=-(Zs0[idx]-Zr0[idx])/r0[idx]
        # Pi[k+0]=1/(1000**2)
        # Pi[k+1]=1/(1000**2)
        # Pi[k+2]=1/(1000**2)
        k=k+3
        for i in range(1,len(uniquetimes),1):
            idx=GPSTime==uniquetimes[i]
            A[idx,k+0]=-(Xs0[idx]-Xr0[idx])/r0[idx]
            A[idx,k+1]=-(Ys0[idx]-Yr0[idx])/r0[idx]
            A[idx,k+2]=-(Zs0[idx]-Zr0[idx])/r0[idx]
            A[idx,k+3]=1
            # Pi[k+0]=1/(1000**2)
            # Pi[k+1]=1/(1000**2)
            # Pi[k+2]=1/(1000**2)
            # Pi[k+3]=1/(1000**2)
            k=k+4
        
        L0i[k]=XX[k]*1
        Lbi[k]=injTrop*1
        Pi[k]=1/(stdinjTrop**2)
        L0i[k+1]=XX[k+1]*1
        Lbi[k+1]=0.0*1
        Pi[k+1]=1/((1e-7)**2)
        Li=L0i-Lbi
        
        # A[:,k]=mtropo*1
        # A[:,k+1]=mtropo*(GPSTime-GPSTime.min())
        # A[:,k+2]=mtropo*(GPSTime-GPSTime.min())**2
        # k=k+3

        # kk=k*1
        A[:,k]=mtropo*1
        k=k+1
        for t in np.arange(tmin,tmax,dtime):
            idx=(GPSTime>t)
            A[idx,k]=mtropo[idx]*(GPSTime[idx]-t)
            k=k+1
        # print(npartropo,k,kk,k-kk)
        
        # B=A[:,0]*0
        # for i in range(0,len(uniquetimes),1):
        #     idx=(GPSTime>=uniquetimes[i]-100) & (GPSTime<=uniquetimes[i]+100)
        #     A[idx,k]=mtropo[idx]*1
        #     B[idx]=B[idx]+1
        #     k=k+1
        # for i in range(k-len(uniquetimes),k,1):
        #     A[:,i]=A[:,i]/(B)
        
        # B=A[:,0]*0
        # for t in np.arange(tmin,tmax+dtime,dtime):
        #     idx=(GPSTime>=t-dtime-100) & (GPSTime<=t+dtime+100)
        #     A[idx,k]=mtropo[idx]*1
        #     A[idx,k+1]=mtropo[idx]*(GPSTime[idx]-t)
        #     B[idx]=B[idx]+1
        #     k=k+2
        # for i in range(k-npartropo,k,1):
        #     A[:,i]=A[:,i]/(B)
        
        # A[:,k]=mtropo*1
        # k=k+1
        # for i in range(0,len(uniquetimes)-1,1):
        #     idx=GPSTime>uniquetimes[i]
        #     A[idx,k]=mtropo[idx]*30
        #     if(it_pos>0):
        #         L0i[k]=X[k]*1
        #         Lbi[k]=injTrop*1
        #         Pi[k]=1/(stdinjTrop**2)
        #     k=k+1
        # Li=L0i-Lbi
        
        for i in range(len(uniqueflags)):
            idx=flags==uniqueflags[i]
            A[idx,k]=1
            # Pi[k]=1/(1000**2)
            k=k+1
        
        # Weight
        for i in range(npar):
            AP[:,i]=A[:,i]*P
            AiP[:,i]=Ai[:,i]*Pi
        
        # Least Square Adjustment
        N=np.dot(AP.T, A)
        U=np.dot(AP.T, L)
        Ni=np.dot(AiP.T, Ai)
        Ui=np.dot(AiP.T, Li)
        invN=np.linalg.inv(N)
        X=np.dot(-invN,U)
        
        k=0
        idx=GPSTime==uniquetimes[0]
        Xr0[idx]=Xr0[idx]+X[k+0]
        Yr0[idx]=Yr0[idx]+X[k+1]
        Zr0[idx]=Zr0[idx]+X[k+2]
        k=k+3
        for i in range(1,len(uniquetimes),1):
            idx=GPSTime==uniquetimes[i]
            Xr0[idx]=Xr0[idx]+X[k+0]
            Yr0[idx]=Yr0[idx]+X[k+1]
            Zr0[idx]=Zr0[idx]+X[k+2]
            Clkr0[idx]=Clkr0[idx]+X[k+3]/c
            k=k+4

        # tropo0=tropo0+X[k]+X[k+1]*(GPSTime-GPSTime.min())+X[k+2]*(GPSTime-GPSTime.min())**2
        # k=k+3
        
        tropo0=tropo0+X[k]
        k=k+1
        for t in np.arange(tmin,tmax,dtime):
            idx=(GPSTime>t)
            tropo0[idx]=tropo0[idx]+X[k]*(GPSTime[idx]-t)
            k=k+1
        # for i in range(0,len(uniquetimes),1):
        #     idx=(GPSTime>=uniquetimes[i]-100) & (GPSTime<=uniquetimes[i]+100)
        #     tropo0[idx]=tropo0[idx]+X[k]#/(B[idx])
        #     # tropo0[idx]=tropo0[idx]+X[k]+X[k+1]*(GPSTime[idx]-t)
        #     k=k+1
                
        # for i in range(0,len(uniquetimes)-1,1):
        #     idx=GPSTime>uniquetimes[i]
        #     trop[idx]=trop[idx]+X[k]*30
        #     k=k+1
        # tropo0=tropo0+trop
        
        for i in range(len(uniqueflags)):
            idx=flags==uniqueflags[i]
            amb0[idx]=amb0[idx]+X[k]
            k=k+1
        XX=XX+X
        
    xr=xs*np.nan
    yr=xs*np.nan
    zr=xs*np.nan
    clkr=xs*np.nan
    residual=xs*np.nan
    tropo=xs*np.nan
    amb=xs*np.nan
    
    xr[idxobs]=Xr0*1
    yr[idxobs]=Yr0*1
    zr[idxobs]=Zr0*1
    clkr[idxobs]=Clkr0*1
    tropo[idxobs]=tropo0*1
    amb[idxobs]=amb0*1
    residual[idxobs]=L0-Lb
    
    return xr, yr, zr, clkr, tropo, amb, residual,XX

# linear piece wise
# DT=10
# a0=2
# t1=np.arange(0,10,0.2)
# b1=0.1
# t2=np.arange(10,20,0.2)
# b2=0.5
# t3=np.arange(20,30+0.2,0.2)
# b3=-0.2

# data0=a0+b1*(t1-0)
# data1=a0+b1*DT+b2*(t2-t2[0])
# data2=a0+(b1+b2)*DT+b3*(t3-t3[0])

# t=np.append(t1,t2)
# t=np.append(t,t3)
# data=np.append(data0,data1)
# data=np.append(data,data2)

# tlb=np.array((t[0],t[50],t[100],t[150]))
# lb=np.array((data[0],data[50],data[100],data[150]))

# A=np.zeros((len(lb),4))
# A[:,0]=1
# A[1:,1]=10
# A[2:,2]=10
# A[3:,3]=10

# N=np.dot(A.T, A)
# U=np.dot(A.T, lb)
# invN=np.linalg.inv(N)
# X=np.dot(invN,U)
# print(X)

# # plt.plot(t,data,'ko')
# # plt.plot(tlb,lb,'r.')
