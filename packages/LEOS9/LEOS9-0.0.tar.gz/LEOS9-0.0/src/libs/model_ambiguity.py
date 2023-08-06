import numpy as np
import random

c = 299792458

def simu_ambiguity_func(p1,ntimes,nsats):
    
    minnumber=-1000
    maxnumber=1000
    
    N=p1*np.nan
    randomnumber = random.randint(minnumber,maxnumber)
    for isat in range(nsats):
        randomnumber = random.randint(minnumber,maxnumber)
        for itime in range(ntimes):
            if(itime>0):
                if(np.isnan(p1[itime,isat])): N[itime,isat]=np.nan
                if(np.isnan(p1[itime-1,isat])): randomnumber = random.randint(minnumber,maxnumber)
                if(~np.isnan(p1[itime,isat])): N[itime,isat]=randomnumber*1
            elif(itime==0):
                if(np.isnan(p1[itime,isat])): N[itime,isat]=np.nan
                if(~np.isnan(p1[itime,isat])): N[itime,isat]=randomnumber*1
        
    return N


def model_ambiguity_func(gpstime,f1,f2,p1,p2,l1,l2,n_continuos_obs,ntimes,nsats):
    
    k=40.308193
    F=((f1*f1)*(f2*f2))/(k*(f1*f1-f2*f2))
    stec=F*(l2-l1)/1e16
    stec_lim=2
    l1_lim=100e3
    l2_lim=100e3
    
    flag=np.zeros((ntimes,nsats))
    for i in range(1,ntimes):
        for j in range(1,nsats):
            if(np.isnan(stec[i,j])): flag[i:,j]=flag[i:,j]+1
            elif(np.isnan(stec[i-1,j])): flag[i:,j]=flag[i:,j]+1
            elif(np.abs(stec[i,j]-stec[i-1,j])>stec_lim): flag[i:,j]=flag[i:,j]+1
            elif(np.abs(l1[i,j]-l1[i-1,j])>l1_lim): flag[i:,j]=flag[i:,j]+1
            elif(np.abs(l2[i,j]-l2[i-1,j])>l2_lim): flag[i:,j]=flag[i:,j]+1
    
    l=0
    flag_amb=flag*np.nan
    for j in range(1,nsats):
        uniqueflags=np.unique(flag[:,j])
        for k in range(len(uniqueflags)):
            idx=flag[:,j]==uniqueflags[k]
            if(len(flag[idx,j])<n_continuos_obs): flag_amb[idx,j]=np.nan
            else: flag_amb[idx,j]=l; l=l+1
        
    return flag_amb

# def model_ambiguity_func(gpstime,pIF,lIF,n_continuos_obs):
    
#     ntimes,nsats=pIF.shape*1
#     lif=lIF*1
#     time=gpstime*1
    
#     # create ambiguities
#     for i in range(nsats):
#         vIF=np.append(np.diff(pIF[:,i]-lIF[:,i])/np.diff(gpstime[:,i]),np.nan)
#         lif[np.abs(vIF)>=1]=np.nan
#         vIF=np.append(np.nan,np.diff(pIF[:,i]-lIF[:,i])/np.diff(gpstime[:,i]))
#         lif[np.abs(vIF)>=1]=np.nan
#     time[np.isnan(lif)]=np.nan
    
#     flag=lif*0
#     for j in range(nsats):
#         for i in range(ntimes-1):
#             if( (np.isnan(time[i+1,j])) & (~np.isnan(time[i,j]))):
#                 flag[i+1:,j]=flag[i+1:,j]+1
#         flag[-1,j]=np.nan
#         idx=~np.isnan(flag[:,j])
#         all_flags=np.unique(flag[idx,j])
        
#         for i in range(len(all_flags)):
#             idx=flag[:,j]==all_flags[i]
#             if(len(flag[idx,j])<n_continuos_obs):
#                 flag[idx,j]=np.nan
#         #         ambIF[idx,j]=np.nanmean(lif[idx,j]-pIF[idx,j])
#     flag[np.isnan(time)]=np.nan
    
#     return flag
