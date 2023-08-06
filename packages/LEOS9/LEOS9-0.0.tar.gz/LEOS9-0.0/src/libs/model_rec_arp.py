import numpy as np
from libs.convert_xyz_to_llh import convert_xyz_to_llh_func

def model_rec_arp_func(xr,yr,zr,arp_dx,arp_dy,arp_dz,ntimes):
    # for H/E/N
    xrcorr=xr*np.nan
    yrcorr=xr*np.nan
    zrcorr=xr*np.nan
    for i in range(ntimes):
        x=np.nanmean(xr[i,:])
        y=np.nanmean(yr[i,:])
        z=np.nanmean(zr[i,:])
        phi,lam,alt=convert_xyz_to_llh_func(x, y, z)

        R=np.zeros((3,3))
        R[0,0] = -np.sin(lam);             R[0,1]=np.cos(lam);              R[0,2]=0
        R[1,0] = -np.sin(phi)*np.cos(lam); R[1,1]=-np.sin(phi)*np.sin(lam); R[1,2]=np.cos(phi);
        R[2,0] = np.cos(phi)*np.cos(lam);  R[2,1]=np.cos(phi)*np.sin(lam);  R[2,2]=np.sin(phi);
        
        ant_dxyz=np.dot(np.linalg.inv(R),np.array((arp_dz,arp_dy,arp_dx)))

        xrcorr[i,:]=xr[i,:]-ant_dxyz[0]
        yrcorr[i,:]=yr[i,:]-ant_dxyz[1]
        zrcorr[i,:]=zr[i,:]-ant_dxyz[2]
    
    return xrcorr,yrcorr,zrcorr

    # for XYZ
    # xrcorr=xr*np.nan
    # yrcorr=xr*np.nan
    # zrcorr=xr*np.nan
    # for i in range(ntimes):
    #     x=np.nanmean(xr[i,:])
    #     y=np.nanmean(yr[i,:])
    #     z=np.nanmean(zr[i,:])
    #     phi,lam,alt=convert_xyz_to_llh_func(x, y, z)

    #     R=np.zeros((3,3))
    #     R[0,0] = -np.sin(lam);             R[0,1]=np.cos(lam);              R[0,2]=0
    #     R[1,0] = -np.sin(phi)*np.cos(lam); R[1,1]=-np.sin(phi)*np.sin(lam); R[1,2]=np.cos(phi);
    #     R[2,0] = np.cos(phi)*np.cos(lam);  R[2,1]=np.cos(phi)*np.sin(lam);  R[2,2]=np.sin(phi);
        
    #     ant_dxyz=np.dot(np.linalg.inv(R),np.array((arp_dx,arp_dy,arp_dz)))

    #     xrcorr[i,:]=xr[i,:]-ant_dxyz[0]
    #     yrcorr[i,:]=yr[i,:]-ant_dxyz[1]
    #     zrcorr[i,:]=zr[i,:]-ant_dxyz[2]
    
    # return xrcorr,yrcorr,zrcorr

