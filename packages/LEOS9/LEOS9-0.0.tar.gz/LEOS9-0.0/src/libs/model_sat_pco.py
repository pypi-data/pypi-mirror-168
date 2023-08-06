import numpy as np

c = 299792458
MU = 3.986005e+14

def model_sat_pco_func(xs,ys,zs,xsun,ysun,zsun,pcoN,pcoE,pcoU,nsat):
    
    # xscorr=xs*np.nan
    # yscorr=xs*np.nan
    # zscorr=xs*np.nan
    pcoX=xs*np.nan
    pcoY=xs*np.nan
    pcoZ=xs*np.nan
    for j in range(nsat):
        r_sat=np.array((xs[:,j],ys[:,j],zs[:,j])).T
        r_sun=np.array((xsun,ysun,zsun)).T
        k=-np.array([r_sat[i,:]/np.linalg.norm(r_sat[i,:]) for i in range(len(r_sat))])
        e=np.array([(r_sun[i,:]-r_sat[i,:])/np.linalg.norm(r_sun[i,:]-r_sat[i,:]) for i in range(len(r_sat))])
        jj=np.array([np.cross(k[i,:],e[i,:])/np.linalg.norm(np.cross(k[i,:],e[i,:])) for i in range(len(r_sat))])
        ii=np.cross(jj,k)

        pco=ii*(pcoN[j])+jj*(pcoE[j])+k*(pcoU[j])
        
        # xscorr[:,j]=xs[:,j]+pco[:,0]*1
        # yscorr[:,j]=ys[:,j]+pco[:,1]*1
        # zscorr[:,j]=zs[:,j]+pco[:,2]*1

        pcoX[:,j]=pco[:,0]*1
        pcoY[:,j]=pco[:,1]*1
        pcoZ[:,j]=pco[:,2]*1
    
    return pcoX,pcoY,pcoZ
