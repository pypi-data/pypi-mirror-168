import numpy as np
from astropy import time
from astropy import units as u
from astropy import coordinates as coordastro
from astropy.utils import iers
iers.conf.auto_download = False  
from numpy.linalg import norm
from numpy import cross

epoch_j2000 = time.Time('2000-01-01T12:00:00.000',format='isot')  # UTC by default

GM = 3.986005e14
cr = 6.283185307179600

def gcrs2itrs(gpstime,x,y,z):
    epoch = time.Time(gpstime,format='gps') 
    cartrep = coordastro.CartesianRepresentation(x, y,z, unit=u.m)
    gcrs = coordastro.GCRS(cartrep, obstime=epoch)
    itrs = gcrs.transform_to(coordastro.ITRS(obstime=epoch))
    xest=itrs.x.value*1
    yest=itrs.y.value*1
    zest=itrs.z.value*1
    return xest,yest,zest

def fit_brdc_par_simple(t,lb,uk,ndegreet,ndegreeC):
    nobs=len(lb)
    upar=2+ndegreet*2+ndegreeC*2
    A=np.zeros((nobs,upar))
    A[:,0]=1
    A[:,1]=t*1
    k=2
    for i in range(ndegreet):
        A[:,k]=t*np.sin((i+1)*uk)
        A[:,k+1]=t*np.cos((i+1)*uk)
        k=k+2
    for i in range(ndegreeC):
        A[:,k]=np.sin((i+1)*uk)
        A[:,k+1]=np.cos((i+1)*uk)
        k=k+2
    N=np.dot(A.T, A)
    U=np.dot(A.T, lb)
    invN=np.linalg.inv(N)
    X=np.dot(invN,U)
    la=np.dot(A,X)
    
    return la, X

def interp_leo_brdc_itrs(tk,gpstime,A,ecc,m0,INC0,INC1,INC2,INC3,INC4,INC5,INC6,INC7,INC8,INC9,INC10,INC11,INC12,INC13,INC14,INC15,ARGP0,ARGP1,ARGP2,ARGP3,ARGP4,ARGP5,ARGP6,ARGP7,ARGP8,ARGP9,ARGP10,ARGP11,ARGP12,ARGP13,ARGP14,ARGP15,RAAN0,RAAN1,RAAN2,RAAN3,RAAN4,RAAN5,RAAN6,RAAN7,RAAN8,RAAN9,RAAN10,RAAN11,RAAN12,RAAN13,RAAN14,RAAN15,DIFR0,DIFR1,DIFR2,DIFR3,DIFR4,DIFR5,DIFR6,DIFR7,DIFR8,DIFR9,DIFR10,DIFR11,DIFR12,DIFR13,DIFR14,DIFR15):
    
    epoch = time.Time(tk+gpstime,format='gps') 
    M0=np.deg2rad(m0)
    
    n = np.sqrt(GM/(A**3))
    Mk = M0 + n*tk
    Mk = np.fmod(Mk+cr,cr)
    Ek = Mk*1
    
    max_iter = 12;
    for i in range(1,max_iter+1,1):
        Ek = Mk+ecc*np.sin(Ek);
    Ek = np.fmod(Ek+cr,cr)
    Mk_true = np.arctan2(np.sqrt(1-ecc*ecc)*np.sin(Ek), np.cos(Ek) - ecc)
    
    omega=ARGP0+ARGP1*tk+ARGP2*tk*np.sin(Mk_true)+ARGP3*tk*np.cos(Mk_true)+ARGP4*tk*np.sin(2*Mk_true)+ARGP5*tk*np.cos(2*Mk_true)+ARGP6*tk*np.sin(3*Mk_true)+ARGP7*tk*np.cos(3*Mk_true)+ARGP8*np.sin(Mk_true)+ARGP9*np.cos(Mk_true)+ARGP10*np.sin(2*Mk_true)+ARGP11*np.cos(2*Mk_true)+ARGP12*np.sin(3*Mk_true)+ARGP13*np.cos(3*Mk_true)+ARGP14*np.sin(4*Mk_true)+ARGP15*np.cos(4*Mk_true)
    diff_rk=DIFR0+DIFR1*tk+DIFR2*tk*np.sin(Mk_true)+DIFR3*tk*np.cos(Mk_true)+DIFR4*tk*np.sin(2*Mk_true)+DIFR5*tk*np.cos(2*Mk_true)+DIFR6*tk*np.sin(3*Mk_true)+DIFR7*tk*np.cos(3*Mk_true)+DIFR8*np.sin(Mk_true)+DIFR9*np.cos(Mk_true)+DIFR10*np.sin(2*Mk_true)+DIFR11*np.cos(2*Mk_true)+DIFR12*np.sin(3*Mk_true)+DIFR13*np.cos(3*Mk_true)+DIFR14*np.sin(4*Mk_true)+DIFR15*np.cos(4*Mk_true)
    ik=INC0+INC1*tk+INC2*tk*np.sin(Mk_true)+INC3*tk*np.cos(Mk_true)+INC4*tk*np.sin(2*Mk_true)+INC5*tk*np.cos(2*Mk_true)+INC6*tk*np.sin(3*Mk_true)+INC7*tk*np.cos(3*Mk_true)+INC8*np.sin(Mk_true)+INC9*np.cos(Mk_true)+INC10*np.sin(2*Mk_true)+INC11*np.cos(2*Mk_true)+INC12*np.sin(3*Mk_true)+INC13*np.cos(3*Mk_true)+INC14*np.sin(4*Mk_true)+INC15*np.cos(4*Mk_true)
    Omega0=RAAN0+RAAN1*tk+RAAN2*tk*np.sin(Mk_true)+RAAN3*tk*np.cos(Mk_true)+RAAN4*tk*np.sin(2*Mk_true)+RAAN5*tk*np.cos(2*Mk_true)+RAAN6*tk*np.sin(3*Mk_true)+RAAN7*tk*np.cos(3*Mk_true)+RAAN8*np.sin(Mk_true)+RAAN9*np.cos(Mk_true)+RAAN10*np.sin(2*Mk_true)+RAAN11*np.cos(2*Mk_true)+RAAN12*np.sin(3*Mk_true)+RAAN13*np.cos(3*Mk_true)+RAAN14*np.sin(4*Mk_true)+RAAN15*np.cos(4*Mk_true)
    
    phik = Mk_true + omega # argument of latitude
    phik = np.fmod(phik,cr)
    uk = phik *1
    rk = A*(1 - ecc*np.cos(Ek)) + diff_rk

    x1k = np.cos(uk)*rk
    y1k = np.sin(uk)*rk
    
    Omegak = Omega0*1
    Omegak = np.fmod(Omegak + cr, cr)
    
    xk = x1k*np.cos(Omegak) - y1k*np.cos(ik)*np.sin(Omegak)
    yk = x1k*np.sin(Omegak) + y1k*np.cos(ik)*np.cos(Omegak)
    zk = y1k*np.sin(ik)
    
    cartrep = coordastro.CartesianRepresentation(xk, yk,zk, unit=u.m)
    gcrs = coordastro.GCRS(cartrep, obstime=epoch)
    itrs = gcrs.transform_to(coordastro.ITRS(obstime=epoch))
    xs=itrs.x.value*1
    ys=itrs.y.value*1
    zs=itrs.z.value*1

    return xs,ys,zs

def interp_leo_brdc_gcrs(tk,A,ecc,m0,INC0,INC1,INC2,INC3,INC4,INC5,INC6,INC7,INC8,INC9,INC10,INC11,INC12,INC13,INC14,INC15,ARGP0,ARGP1,ARGP2,ARGP3,ARGP4,ARGP5,ARGP6,ARGP7,ARGP8,ARGP9,ARGP10,ARGP11,ARGP12,ARGP13,ARGP14,ARGP15,RAAN0,RAAN1,RAAN2,RAAN3,RAAN4,RAAN5,RAAN6,RAAN7,RAAN8,RAAN9,RAAN10,RAAN11,RAAN12,RAAN13,RAAN14,RAAN15,DIFR0,DIFR1,DIFR2,DIFR3,DIFR4,DIFR5,DIFR6,DIFR7,DIFR8,DIFR9,DIFR10,DIFR11,DIFR12,DIFR13,DIFR14,DIFR15):
    
    M0=np.deg2rad(m0)
    
    n = np.sqrt(GM/(A**3))
    Mk = M0 + n*tk
    Mk = np.fmod(Mk+cr,cr)
    Ek = Mk*1
    
    max_iter = 12;
    for i in range(1,max_iter+1,1):
        Ek = Mk+ecc*np.sin(Ek);
    Ek = np.fmod(Ek+cr,cr)
    Mk_true = np.arctan2(np.sqrt(1-ecc*ecc)*np.sin(Ek), np.cos(Ek) - ecc)
    
    omega=ARGP0+ARGP1*tk+ARGP2*tk*np.sin(Mk_true)+ARGP3*tk*np.cos(Mk_true)+ARGP4*tk*np.sin(2*Mk_true)+ARGP5*tk*np.cos(2*Mk_true)+ARGP6*tk*np.sin(3*Mk_true)+ARGP7*tk*np.cos(3*Mk_true)+ARGP8*np.sin(Mk_true)+ARGP9*np.cos(Mk_true)+ARGP10*np.sin(2*Mk_true)+ARGP11*np.cos(2*Mk_true)+ARGP12*np.sin(3*Mk_true)+ARGP13*np.cos(3*Mk_true)+ARGP14*np.sin(4*Mk_true)+ARGP15*np.cos(4*Mk_true)
    diff_rk=DIFR0+DIFR1*tk+DIFR2*tk*np.sin(Mk_true)+DIFR3*tk*np.cos(Mk_true)+DIFR4*tk*np.sin(2*Mk_true)+DIFR5*tk*np.cos(2*Mk_true)+DIFR6*tk*np.sin(3*Mk_true)+DIFR7*tk*np.cos(3*Mk_true)+DIFR8*np.sin(Mk_true)+DIFR9*np.cos(Mk_true)+DIFR10*np.sin(2*Mk_true)+DIFR11*np.cos(2*Mk_true)+DIFR12*np.sin(3*Mk_true)+DIFR13*np.cos(3*Mk_true)+DIFR14*np.sin(4*Mk_true)+DIFR15*np.cos(4*Mk_true)
    ik=INC0+INC1*tk+INC2*tk*np.sin(Mk_true)+INC3*tk*np.cos(Mk_true)+INC4*tk*np.sin(2*Mk_true)+INC5*tk*np.cos(2*Mk_true)+INC6*tk*np.sin(3*Mk_true)+INC7*tk*np.cos(3*Mk_true)+INC8*np.sin(Mk_true)+INC9*np.cos(Mk_true)+INC10*np.sin(2*Mk_true)+INC11*np.cos(2*Mk_true)+INC12*np.sin(3*Mk_true)+INC13*np.cos(3*Mk_true)+INC14*np.sin(4*Mk_true)+INC15*np.cos(4*Mk_true)
    Omega0=RAAN0+RAAN1*tk+RAAN2*tk*np.sin(Mk_true)+RAAN3*tk*np.cos(Mk_true)+RAAN4*tk*np.sin(2*Mk_true)+RAAN5*tk*np.cos(2*Mk_true)+RAAN6*tk*np.sin(3*Mk_true)+RAAN7*tk*np.cos(3*Mk_true)+RAAN8*np.sin(Mk_true)+RAAN9*np.cos(Mk_true)+RAAN10*np.sin(2*Mk_true)+RAAN11*np.cos(2*Mk_true)+RAAN12*np.sin(3*Mk_true)+RAAN13*np.cos(3*Mk_true)+RAAN14*np.sin(4*Mk_true)+RAAN15*np.cos(4*Mk_true)
    
    phik = Mk_true + omega # argument of latitude
    phik = np.fmod(phik,cr)
    uk = phik *1
    rk = A*(1 - ecc*np.cos(Ek)) + diff_rk

    x1k = np.cos(uk)*rk
    y1k = np.sin(uk)*rk
    
    Omegak = Omega0*1
    Omegak = np.fmod(Omegak + cr, cr)
    
    xk = x1k*np.cos(Omegak) - y1k*np.cos(ik)*np.sin(Omegak)
    yk = x1k*np.sin(Omegak) + y1k*np.cos(ik)*np.cos(Omegak)
    zk = y1k*np.sin(ik)
    
    xs=xk*1
    ys=yk*1
    zs=zk*1

    return xs,ys,zs

def est_leo_brdc_gcrs(tk,xleo,yleo,zleo,m0):
    
    M0=np.deg2rad(m0)
    
    # eccentricity
    r=np.sqrt(xleo**2+yleo**2+zleo**2)
    ra=np.nanmax(r)
    rp=np.nanmin(r)
    ecc=(ra-rp)/(ra+rp)
    
    # semi-major axis
    A  = (ra+rp)/2
    
    n = np.sqrt(GM/(A**3))
    Mk = M0 + n*tk
    Mk = np.fmod(Mk+cr,cr)
    Ek = Mk*1
    
    max_iter = 12;
    for i in range(1,max_iter+1,1):
        Ek = Mk+ecc*np.sin(Ek);
        
    Ek = np.fmod(Ek+cr,cr);
    Mk_true = np.arctan2(np.sqrt(1-ecc*ecc)*np.sin(Ek), np.cos(Ek) - ecc)
    
    Ek2=Ek[:-1]*1
    Mk_true2=Mk_true[:-1]*1
    x1=xleo[:-1]*1
    y1=yleo[:-1]*1
    z1=zleo[:-1]*1
    timek=tk[:-1]*1
    vx=np.diff(xleo)/np.diff(tk)
    vy=np.diff(yleo)/np.diff(tk)
    vz=np.diff(zleo)/np.diff(tk)
    
    r = np.array([ x1, y1, z1 ]).T
    v = np.array([ vx, vy, vz ]).T
    h = cross(r, v)
    
    inc = np.arccos(h[:,2] / norm(h,axis=1))
    n = cross([0, 0, 1], h)
    raan = np.arctan2(n[:,1], n[:,0]) % (2 * np.pi)
    px = np.array([r[i,:].dot(n[i,:]) for i in range(r.shape[0])])
    py = np.array([r[i,:].dot(cross(h[i,:], n[i,:])) / norm(h[i,:]) for i in range(r.shape[0])])
    argp = (np.arctan2(py, px) - Mk_true2) % (2 * np.pi)
    
    # models
    argp,argpX=fit_brdc_par_simple(timek,argp,Mk_true2,3,4)
    raan,raanX=fit_brdc_par_simple(timek,raan,Mk_true2,3,4)
    inc,incX=fit_brdc_par_simple(timek,inc,Mk_true2,3,4)
    rk = A*(1 - ecc*np.cos(Ek2)) 
    rs=np.sqrt(x1**2+y1**2+z1**2)
    diff_rk=rs-rk
    diff_rk,diff_rkX=fit_brdc_par_simple(timek,diff_rk,Mk_true2,3,4)

    Omega0=raan*1
    omega=argp*1
    ik=inc*1

    phik = Mk_true2 + omega # argument of latitude
    phik = np.fmod(phik,cr)
    uk = phik *1
    rk = A*(1 - ecc*np.cos(Ek2)) + diff_rk

    x1k = np.cos(uk)*rk
    y1k = np.sin(uk)*rk

    Omegak = Omega0*1
    Omegak = np.fmod(Omegak + cr, cr)

    x = x1k*np.cos(Omegak) - y1k*np.cos(ik)*np.sin(Omegak)
    y = x1k*np.sin(Omegak) + y1k*np.cos(ik)*np.cos(Omegak)
    z = y1k*np.sin(ik)
    resx=xleo[:-1]-x
    resy=yleo[:-1]-y
    resz=zleo[:-1]-z
    
    return A,ecc,M0,incX,raanX,argpX,diff_rkX,x,y,z,resx,resy,resz


def est_leo_brdc_gcrs_A(tk,xleo,yleo,zleo,m0,deltaecc,deltaA):
    
    M0=np.deg2rad(m0)
    
    # eccentricity
    r=np.sqrt(xleo**2+yleo**2+zleo**2)
    ra=np.nanmax(r)
    rp=np.nanmin(r)
    ecc=(ra-rp)/(ra+rp) + deltaecc
    
    # semi-major axis
    A  = (ra+rp)/2 + deltaA
    
    n = np.sqrt(GM/(A**3))
    Mk = M0 + n*tk
    Mk = np.fmod(Mk+cr,cr)
    Ek = Mk*1
    
    max_iter = 12;
    for i in range(1,max_iter+1,1):
        Ek = Mk+ecc*np.sin(Ek);
        
    Ek = np.fmod(Ek+cr,cr);
    Mk_true = np.arctan2(np.sqrt(1-ecc*ecc)*np.sin(Ek), np.cos(Ek) - ecc)
    
    Ek2=Ek[:-1]*1
    Mk_true2=Mk_true[:-1]*1
    x1=xleo[:-1]*1
    y1=yleo[:-1]*1
    z1=zleo[:-1]*1
    timek=tk[:-1]*1
    vx=np.diff(xleo)/np.diff(tk)
    vy=np.diff(yleo)/np.diff(tk)
    vz=np.diff(zleo)/np.diff(tk)
    
    r = np.array([ x1, y1, z1 ]).T
    v = np.array([ vx, vy, vz ]).T
    h = cross(r, v)
    
    inc = np.arccos(h[:,2] / norm(h,axis=1))
    n = cross([0, 0, 1], h)
    raan = np.arctan2(n[:,1], n[:,0]) % (2 * np.pi)
    px = np.array([r[i,:].dot(n[i,:]) for i in range(r.shape[0])])
    py = np.array([r[i,:].dot(cross(h[i,:], n[i,:])) / norm(h[i,:]) for i in range(r.shape[0])])
    argp = (np.arctan2(py, px) - Mk_true2) % (2 * np.pi)
    
    # models
    argp,argpX=fit_brdc_par_simple(timek,argp,Mk_true2,4)
    raan,raanX=fit_brdc_par_simple(timek,raan,Mk_true2,4)
    inc,incX=fit_brdc_par_simple(timek,inc,Mk_true2,4)
    rk = A*(1 - ecc*np.cos(Ek2)) 
    rs=np.sqrt(x1**2+y1**2+z1**2)
    diff_rk=rs-rk
    diff_rk,diff_rkX=fit_brdc_par_simple(timek,diff_rk,Mk_true2,4)

    Omega0=raan*1
    omega=argp*1
    ik=inc*1

    phik = Mk_true2 + omega # argument of latitude
    phik = np.fmod(phik,cr)
    uk = phik *1
    rk = A*(1 - ecc*np.cos(Ek2)) + diff_rk

    x1k = np.cos(uk)*rk
    y1k = np.sin(uk)*rk

    Omegak = Omega0*1
    Omegak = np.fmod(Omegak + cr, cr)

    x = x1k*np.cos(Omegak) - y1k*np.cos(ik)*np.sin(Omegak)
    y = x1k*np.sin(Omegak) + y1k*np.cos(ik)*np.cos(Omegak)
    z = y1k*np.sin(ik)
    resx=xleo[:-1]-x
    resy=yleo[:-1]-y
    resz=zleo[:-1]-z
    
    return A,ecc,M0,incX,raanX,argpX,diff_rkX,resx,resy,resz
