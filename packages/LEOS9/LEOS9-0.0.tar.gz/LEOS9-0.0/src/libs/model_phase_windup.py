import numpy as np
from libs.convert_xyz_to_llh import convert_xyz_to_llh_func

c = 299792458

def model_phase_windup_func(f1,f2,lIF,xr,yr,zr,xs,ys,zs,xsun,ysun,zsun,ntimes,nsats):

    ml1=(f1**2)/(f1**2-f2**2);
    ml2=-(f1*f2)/(f1**2-f2**2);
    wIF=c/(ml1*f1+ml2*f2) # ionofree
    wIF=c/f1 # L1
    lam = wIF*1
    r=np.sqrt((xs-xr)**2+(ys-yr)**2+(zs-zr)**2)
    windup=np.zeros((xr.shape[0],xr.shape[1]))
    rotation=np.zeros((xr.shape[0],xr.shape[1]))
    for i in range(1,ntimes-1):
        for j in range(nsats):# nsats
            if( (~np.isnan(r[i-1,j])) & (~np.isnan(lIF[i-1,j])) &  (~np.isnan(r[i,j])) & (~np.isnan(lIF[i,j]))):#& ((gpstime[i,j]-gpstime_day)/3600>8)  & ((gpstime[i,j]-gpstime_day)/3600<10)
        
                r_rec=np.array((xr[i,j],yr[i,j],zr[i,j]))
                # r_rec1=np.array((xr[i+1,j],yr[i+1,j],zr[i+1,j]))
                r_sat=np.array((xs[i,j],ys[i,j],zs[i,j]))
                # r_sat1=np.array((xs[i+1,j],ys[i+1,j],zs[i+1,j]))
                r_sun=np.array((xsun[i],ysun[i],zsun[i]))
                
                kk=-(r_sat-r_rec)/np.linalg.norm(r_sat-r_rec)

                k=-r_sat/np.linalg.norm(r_sat)
                e=(r_sun-r_sat)/np.linalg.norm(r_sun-r_sat)
                # e=(r_sat1-r_sat)/np.linalg.norm(r_sat1-r_sat)
                jj=np.cross(k,e)/np.linalg.norm(np.cross(k,e))
                ii=np.cross(jj,k)/np.linalg.norm(np.cross(jj,k))
                D_sat = ii - kk * np.dot(kk, ii) - np.cross(kk, jj)
                # print(D_sat)

                # E[0]=-sinl;      E[3]=cosl;       E[6]=0.0;
                # E[1]=-sinp*cosl; E[4]=-sinp*sinl; E[7]=cosp;
                # E[2]=cosp*cosl;  E[5]=cosp*sinl;  E[8]=sinp;
                lat,lon,alt=convert_xyz_to_llh_func(r_rec[0],r_rec[1],r_rec[2])
                sinp=np.sin(lat)
                cosp=np.cos(lat)
                sinl=np.sin(lon)
                cosl=np.cos(lon)
                ii=np.array([-sinp*cosl,-sinp*sinl,cosp])
                jj=np.array([sinl,-cosl,0.0])

                # lat,lon,alt=convert_xyz_to_llh_func(r_rec[0],r_rec[1],r_rec[2])
                # R=np.zeros((3,3))
                # R[0,0] = -np.sin(lon);             R[0,1]=np.cos(lon);              R[0,2]=0
                # R[1,0] = -np.sin(lat)*np.cos(lon); R[1,1]=-np.sin(lat)*np.sin(lon); R[1,2]=np.cos(lat);
                # R[2,0] = np.cos(lat)*np.cos(lon);  R[2,1]=np.cos(lat)*np.sin(lon);  R[2,2]=np.sin(lat);
                # ii=np.array([R[1,0],R[1,1],R[1,2]])
                # jj=np.array([-R[0,0],-R[0,1],-R[0,2]])
                # k=-(r_rec)/np.linalg.norm(r_rec)
                # e=(r_rec1-r_rec)/np.linalg.norm(r_rec1-r_rec)
                # e=(r_sun-r_rec)/np.linalg.norm(r_sun-r_rec)
                # jj=np.cross(kk,e)/np.linalg.norm(np.cross(kk,e))
                # ii=np.cross(jj,kk)
                D_rec = ii - kk * np.dot(kk, ii) + np.cross(kk, jj)
                
                comega = np.dot(D_sat, D_rec) / (np.linalg.norm(D_sat)*np.linalg.norm(D_rec)) # or np.dot(np.linalg.norm(D_sat),np.linalg.norm(D_rec))
                if(comega <-1): comega =-1
                elif(comega >1): comega =1
                
                omega = np.arccos(comega)#/ (2 *np.pi)
                
                gamma = np.dot(kk, np.cross(D_sat, D_rec))
                if gamma < 0: omega = -omega*1
                
                if(i>0):
                    N = np.floor( (windup[i-1,j] - omega )/(2*np.pi) + 0.5 )
                    # Nrot = np.floor( (rotation[i-1,j] - omega )/(2*np.pi) + 0.5 )

                else:
                    N = 0

                # if(omega + N>1):
                #     windup[i,j] = omega + N-2#*2*np.pi
                # elif(omega + N<-1):
                #     windup[i,j] = omega + N+2#*2*np.pi
                # else:
                #     windup[i,j] = omega + N#*2*np.pi
                
                windup[i,j] = omega + N*2*np.pi
                rotation[i,j] = omega/(2*np.pi)

                
    windup=lam*windup/(2*np.pi),rotation
    
    return windup

def model_phase_windup_rotation(f1,f2,lIF,xr,yr,zr,xs,ys,zs,xsun,ysun,zsun,ntimes,nsats):

    ml1=(f1**2)/(f1**2-f2**2);
    ml2=-(f1*f2)/(f1**2-f2**2);
    wIF=c/(ml1*f1+ml2*f2) # ionofree
    wIF=c/f1 # L1
    lam = wIF*1
    r=np.sqrt((xs-xr)**2+(ys-yr)**2+(zs-zr)**2)
    windup=np.zeros((xr.shape[0],xr.shape[1]))
    rotation=np.zeros(xr.shape[1])
    for i in range(1,ntimes-1):
        for j in range(nsats):# nsats
            if( (~np.isnan(r[i-1,j])) & (~np.isnan(lIF[i-1,j])) &  (~np.isnan(r[i,j])) & (~np.isnan(lIF[i,j]))):#& ((gpstime[i,j]-gpstime_day)/3600>8)  & ((gpstime[i,j]-gpstime_day)/3600<10)
        
                r_rec=np.array((xr[i,j],yr[i,j],zr[i,j]))
                # r_rec1=np.array((xr[i+1,j],yr[i+1,j],zr[i+1,j]))
                r_sat=np.array((xs[i,j],ys[i,j],zs[i,j]))
                # r_sat1=np.array((xs[i+1,j],ys[i+1,j],zs[i+1,j]))
                r_sun=np.array((xsun[i],ysun[i],zsun[i]))
                
                kk=-(r_sat-r_rec)/np.linalg.norm(r_sat-r_rec)

                k=-r_sat/np.linalg.norm(r_sat)
                e=(r_sun-r_sat)/np.linalg.norm(r_sun-r_sat)
                # e=(r_sat1-r_sat)/np.linalg.norm(r_sat1-r_sat)
                jj=np.cross(k,e)/np.linalg.norm(np.cross(k,e))
                ii=np.cross(jj,k)/np.linalg.norm(np.cross(jj,k))
                D_sat = ii - kk * np.dot(kk, ii) - np.cross(kk, jj)
                # print(D_sat)

                # E[0]=-sinl;      E[3]=cosl;       E[6]=0.0;
                # E[1]=-sinp*cosl; E[4]=-sinp*sinl; E[7]=cosp;
                # E[2]=cosp*cosl;  E[5]=cosp*sinl;  E[8]=sinp;
                lat,lon,alt=convert_xyz_to_llh_func(r_rec[0],r_rec[1],r_rec[2])
                sinp=np.sin(lat)
                cosp=np.cos(lat)
                sinl=np.sin(lon)
                cosl=np.cos(lon)
                ii=np.array([-sinp*cosl,-sinp*sinl,cosp])
                jj=np.array([sinl,-cosl,0.0])

                D_rec = ii - kk * np.dot(kk, ii) + np.cross(kk, jj)
                
                comega = np.dot(D_sat, D_rec) / (np.linalg.norm(D_sat)*np.linalg.norm(D_rec)) # or np.dot(np.linalg.norm(D_sat),np.linalg.norm(D_rec))
                if(comega <-1): comega =-1
                elif(comega >1): comega =1
                
                omega = np.arccos(comega)/ (2 *np.pi)
                
                gamma = np.dot(kk, np.cross(D_sat, D_rec))
                if gamma < 0: omega = -omega*1
                
                if(i>0):
                    N = np.floor( (windup[i-1,j] - omega ) + 0.5 )

                else:
                    N = 0

                if(omega + N>1):
                    rotation[j]=rotation[j]+1
                    windup[i,j] = omega + N-2
                elif(omega + N<-1):
                    rotation[j]=rotation[j]+1
                    windup[i,j] = omega + N+2
                else:
                    windup[i,j] = omega + N
                
    windup=lam*windup
    
    return windup,rotation


# def model_phase_windup_func(f1,f2,lIF,xr,yr,zr,xs,ys,zs,xsun,ysun,zsun,ntimes,nsats):

#     ml1=(f1**2)/(f1**2-f2**2);
#     ml2=-(f1*f2)/(f1**2-f2**2);
#     wIF=c/(ml1*f1+ml2*f2)
    
#     lam = wIF*1
#     r=np.sqrt((xs-xr)**2+(ys-yr)**2+(zs-zr)**2)
#     windup=np.zeros((xr.shape[0],xr.shape[1]))
#     for i in range(ntimes):
#         for j in range(nsats):
#             if( (~np.isnan(r[i,j])) & (~np.isnan(lIF[i,j])) ):#& ((gpstime[i,j]-gpstime_day)/3600>8)  & ((gpstime[i,j]-gpstime_day)/3600<10)
        
#                 rec=np.array((xr[i,j],yr[i,j],zr[i,j]))
#                 r_sat=np.array((xs[i,j],ys[i,j],zs[i,j]))
#                 r_sun=np.array((xsun[i,j],ysun[i,j],zsun[i,j]))
                
#                 diff = rec - r_sat 
#                 k = diff / np.linalg.norm(diff)
                
#                 # from deg to rad for lat, lon
#                 lat,lon,alt=convert_xyz_to_llh_func(rec[0],rec[1],rec[2])
                
#                 # ee, en, eu unit vecotrs in ENU ref frame
#                 # ee = np.array([-np.sin(lon), +np.cos(lon),+0])
#                 # en = np.array([-np.cos(lon) * np.sin(lat),-np.sin(lon) * np.sin(lat),+np.cos(lat)])
                
#                 # Computation of the ex, ey, ez unit vectors
#                 ez = -r_sat / np.linalg.norm(r_sat)
#                 # ey = -np.cross(r_sat, vel) / np.linalg.norm(np.cross(r_sat, vel))
#                 e=(r_sun-r_sat)/np.linalg.norm(r_sun-r_sat)
#                 ey=np.cross(ez,e)/np.linalg.norm(np.cross(ez,e))
#                 ex = np.cross(ey, ez)
                
#                 # Effective dipole
#                 D_rec = ex - k * np.dot(k, ex) + np.cross(k, ey) # WindUp.compute_eff_dipole(k, ee, en, flag)
#                 D_sat = ex - k * np.dot(k, ex) - np.cross(k, ey) # WindUp.compute_eff_dipole(k, ee, en, flag)
                
#                 # Wind up computation
#                 # gamma = np.dot(k, np.cross(D_sat, D_rec))
#                 # omega = np.arccos(np.dot(D_sat, D_rec) / (np.linalg.norm(D_sat) * np.linalg.norm(D_rec)))
#                 # omega = -omega / (2 * np.pi)
                
#                 # if gamma < 0:
#                 #     omega = -omega
                
#                 # windup[i,j] = windup[i,j] + omega * lam
                
#                 # Wind up computation
#                 gamma = np.dot(k, np.cross(D_sat, D_rec))
#                 comega = np.dot(D_sat, D_rec) / (np.linalg.norm(D_sat) * np.linalg.norm(D_rec))
#                 if(comega <-1): comega =-1
#                 elif(comega >1): comega =1
#                 omega = -np.arccos(comega)/ (2 * np.pi)
                
#                 if gamma < 0: omega = -omega
                
#                 if(i>0):
#                     N = np.floor( (windup[i-1,j] - omega)/(2*np.pi) + 0.5 )
#                 else:
#                     N = 0
                    
#                 windup[i,j] = omega + N*2*np.pi
    
#     windup=windup*lam/2
#     return windup

# elrad,azrad=convert_xyz_to_azel_func(xr, yr, zr, xs, ys, zs)

# ml1=(f1**2)/(f1**2-f2**2);
# ml2=-(f1*f2)/(f1**2-f2**2);
# wIF=c/(ml1*f1+ml2*f2)
# windup=np.zeros((ntimes,nsats))
# azrad[np.isnan(azrad)]=0
# for i in range(1,ntimes):
#     for j in range(nsats):
#         satelliteInc=azrad[i,j]-windup[i-1,j]
#         windup[i,j]=windup[i-1,j]+np.arctan2(np.sin(satelliteInc),np.cos(satelliteInc))
# windup=windup*wIF/(2*np.pi)
# plt.plot(xr[:,:]*0+windup[:,:],'k.')



############################################ way RTKlib does


# phw=0
# OMGE=7.2921151467E-5
# i=1022
# j=0

# rr=np.array((xr[i,j],yr[i,j],zr[i,j]))
# rs=np.array((xs[i,j],ys[i,j],zs[i,j]))
# vrs=np.array((vxs[i,j],vys[i,j],vzs[i,j]))
# rsun=np.array((xsun[i,j],ysun[i,j],zsun[i,j]))

# # set yaw
# ri=rs*1
# vri=vrs*1
# vri[0]=vri[0]-OMGE*ri[1]
# vri[1]=vri[1]+OMGE*ri[0]
# n=np.cross(ri,vri)
# p=np.cross(rsun,n)
# es=rs/np.linalg.norm(rs)
# esun=rsun/np.linalg.norm(rsun)
# en=n/np.linalg.norm(n)
# ep=p/np.linalg.norm(p)
# beta=np.pi/2.0-np.arccos(np.dot(esun,en))
# E=np.arccos(np.dot(es,ep))
# if (np.dot(es,esun))<=0: mu=np.pi/2.0-E
# else: mu=np.pi/2.0+E
# if (mu<-np.pi/2.0): mu=mu+2.0*np.pi
# elif (mu>=np.pi/2.0): mu-=2.0*np.pi
# yaw=np.arctan2(-np.tan(beta),np.sin(mu))+np.pi
# ex=np.cross(en,es)
# cosy=np.cos(yaw)
# siny=np.sin(yaw)
# exs=-siny*en+cosy*ex
# eys=-cosy*en-siny*ex

# diffr = rr - rs 
# ek = diffr / np.linalg.norm(diffr)

# lat,lon,alt=convert_xyz_to_llh_func(rr[0],rr[1],rr[2])
# sinp=np.sin(lat)
# cosp=np.cos(lat)
# sinl=np.sin(lon)
# cosl=np.cos(lon)
# # E[0]=-sinl;      E[3]=cosl;       E[6]=0.0;
# # E[1]=-sinp*cosl; E[4]=-sinp*sinl; E[7]=cosp;
# # E[2]=cosp*cosl;  E[5]=cosp*sinl;  E[8]=sinp;
# exr=np.array([-sinp*cosl,-sinp*sinl,cosp])
# eyr=np.array([sinl,-cosl,0.0])

# eks=np.cross(ek,eys)
# ekr=np.cross(ek,eyr)

# ds=exs-ek*np.dot(ek,exs)-eks
# dr=exr-ek*np.dot(ek,exr)+ekr

# cosp=np.dot(ds,dr)/np.linalg.norm(ds)/np.linalg.norm(dr)
# if(cosp<-1.0): cosp=-1.0
# elif(cosp> 1.0): cosp= 1.0

# ph=np.arccos(cosp)/2.0/np.pi
# drs=np.cross(ds,dr)

# if(np.dot(ek,drs)<0.0): ph=-ph

# phw=ph+np.floor(phw-ph+0.5)

# print(phw)

