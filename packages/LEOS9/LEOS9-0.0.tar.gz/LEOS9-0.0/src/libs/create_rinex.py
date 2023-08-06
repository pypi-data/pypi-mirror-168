# pip install netcdf4 --proxy suoja-proxy.vyv.fi:8080

#%%
import sys
import numpy as np
import numpy.matlib
import georinex as gr
import matplotlib.pyplot as plt
from datetime import datetime
from netCDF4 import Dataset
import datetime as dt

libs_dir='D:\\INCUBATE\\codes\\PNT_simulation'; # dir where the model is located
sys.path.insert(0, libs_dir); # path of local libs
import funclib as func
from scipy.interpolate import interp1d

def inteprolateNavPar(time,par):
#    f=interp1d(time, par,'previous', bounds_error=False)
    idNoNan = tuple([~np.isnan(par)]);
    idNoNan[0][0]=np.array(True);
    f=interp1d(time[idNoNan], par[idNoNan],'previous', fill_value="extrapolate");
    return f

def inteprolateNavTime(time,par,parwithNan):
    idNoNan = tuple([~np.isnan(parwithNan)]);
    idNoNan[0][0]=np.array(True);
    f=interp1d(time[idNoNan], par[idNoNan],'previous', fill_value="extrapolate");
    return f

def check_t(time):
    #Function accounting for beginning or end of week crossover
    half_week = 302400;     # seconds
    corrTime = time*1;
    return corrTime

def inteprolateGPS(GPSTime,M0,DeltaN,sqrtA,Eccentricity,omega,Cuc,Cus,Crc,Crs,Io,IDOT,Cic,Cis,Omega0,OmegaDot,TGD,Toe,GPSWeek,SVclockBias,SVclockDrift,SVclockDriftRate,Toc):
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
    A  = roota*roota;              #semi-major axis
    tk=  check_t(t - time_eph); #time from the ephemerides reference epoch
    n0 = np.sqrt(GM/(A**3));             #computed mean motion [rad/sec]
    n  = n0 + deltan;              #corrected mean motion [rad/sec]
    Mk = M0 + n*tk;                #mean anomaly
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

#%% read rinex observation
fname='D:\\INCUBATE\\data\\COSMIC-2\\podRnx\\2021\\006\\podCrx_2021.006.006.36.02_crx.rnx'

nsatsGPS=32
nsats=nsatsGPS
sat_typesGPS=['G'+str(np.arange(1,nsatsGPS+1,1)[i]).zfill(2) for i in range(nsatsGPS)]
sat_types=np.array(sat_typesGPS)

# header
header = gr.rinexheader(fname)

# observations
obs = gr.load(fname)
obs_sats = obs.sv.values
obs_times = obs.time
obs_types = list(obs)
# coords = list(obs.coords)
ntimes=len(obs_times)

P1 = np.full((ntimes,nsats),np.nan);
P2 = np.full((ntimes,nsats),np.nan);
L1 = np.full((ntimes,nsats),np.nan);
L2 = np.full((ntimes,nsats),np.nan);

if( ('L1' in obs_types) & ('L2' in obs_types) & ('C1' in obs_types) & ('C2' in obs_types)):
    case='C1C2L1L2'

if(case=='C1C2L1L2'):
    for i in range(len(obs_sats)):
        constelation=obs.sv.values[i][0]
        prn=int(obs.sv.values[i][1:3])
        if constelation=='G':
            P1[:,prn-1] = obs.C1[:,i].values*1
            P2[:,prn-1] = obs.C2[:,i].values*1
            L1[:,prn-1] = obs.L1[:,i].values*1
            L2[:,prn-1] = obs.L2[:,i].values*1            

DATE    = obs_times.values.astype('datetime64[us]')
GPSTime = (DATE-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
GPSTime = np.matlib.repmat(GPSTime,nsats,1)
GPSTime = GPSTime.T*1
DATE=DATE.astype(datetime)

#%% read rinex navigation
nav_prev=gr.load('D:\\INCUBATE\\data\\GNSS\\BRDC\\brdc0050.21n')
nav_curr=gr.load('D:\\INCUBATE\\data\\GNSS\\BRDC\\brdc0060.21n')
nav_next=gr.load('D:\\INCUBATE\\data\\GNSS\\BRDC\\brdc0070.21n')

if(all((nav_prev.sv.values==nav_prev.sv.values) & (nav_prev.sv.values==nav_next.sv.values))==False): print('error between nav files');

nsat=nav_prev.dims['sv']
ntime=nav_prev.dims['time']+nav_curr.dims['time']+nav_next.dims['time']
SVclockBias=np.full((ntime,nsatsGPS),np.nan)
SVclockBias=np.full((ntime,nsatsGPS),np.nan)
SVclockDrift=np.full((ntime,nsatsGPS),np.nan) 
SVclockDriftRate=np.full((ntime,nsatsGPS),np.nan)
Crs=np.full((ntime,nsatsGPS),np.nan)
DeltaN=np.full((ntime,nsatsGPS),np.nan)
M0=np.full((ntime,nsatsGPS),np.nan)
Cuc=np.full((ntime,nsatsGPS),np.nan)
Eccentricity=np.full((ntime,nsatsGPS),np.nan) 
Cus=np.full((ntime,nsatsGPS),np.nan)
sqrtA=np.full((ntime,nsatsGPS),np.nan)
Toe=np.full((ntime,nsatsGPS),np.nan)
Cic=np.full((ntime,nsatsGPS),np.nan)
Omega0=np.full((ntime,nsatsGPS),np.nan)
Cis=np.full((ntime,nsatsGPS),np.nan)
Io=np.full((ntime,nsatsGPS),np.nan)
Crc=np.full((ntime,nsatsGPS),np.nan)
Omega=np.full((ntime,nsatsGPS),np.nan)
OmegaDot=np.full((ntime,nsatsGPS),np.nan)
IDOT=np.full((ntime,nsatsGPS),np.nan)
CodesL2=np.full((ntime,nsatsGPS),np.nan)
GPSWeek=np.full((ntime,nsatsGPS),np.nan)
SVacc=np.full((ntime,nsatsGPS),np.nan)
TGD=np.full((ntime,nsatsGPS),np.nan)
TransTime=np.full((ntime,nsatsGPS),np.nan)
NavTime=np.full((ntime,nsatsGPS),np.nan)
NavGPSTime=np.full((ntime,nsatsGPS),np.nan)

for i in range(nsat):
    prn=int(nav_prev['sv'].values[i][1:])
    SVclockBias[:,prn-1]=np.concatenate((nav_prev.SVclockBias[:,i].values,nav_curr.SVclockBias[:,i].values,nav_next.SVclockBias[:,i].values))
    SVclockDrift[:,prn-1]=np.concatenate((nav_prev.SVclockDrift[:,i].values,nav_curr.SVclockDrift[:,i].values,nav_next.SVclockDrift[:,i].values))
    SVclockDriftRate[:,prn-1]=np.concatenate((nav_prev.SVclockDriftRate[:,i].values,nav_curr.SVclockDriftRate[:,i].values,nav_next.SVclockDriftRate[:,i].values))
    Crs[:,prn-1]=np.concatenate((nav_prev.Crs[:,i].values,nav_curr.Crs[:,i].values,nav_next.Crs[:,i].values))
    DeltaN[:,prn-1]=np.concatenate((nav_prev.DeltaN[:,i].values,nav_curr.DeltaN[:,i].values,nav_next.DeltaN[:,i].values))
    M0[:,prn-1]=np.concatenate((nav_prev.M0[:,i].values,nav_curr.M0[:,i].values,nav_next.M0[:,i].values))
    Cuc[:,prn-1]=np.concatenate((nav_prev.Cuc[:,i].values,nav_curr.Cuc[:,i].values,nav_next.Cuc[:,i].values))
    Eccentricity[:,prn-1]=np.concatenate((nav_prev.Eccentricity[:,i].values,nav_curr.Eccentricity[:,i].values,nav_next.Eccentricity[:,i].values))
    Cus[:,prn-1]=np.concatenate((nav_prev.Cus[:,i].values,nav_curr.Cus[:,i].values,nav_next.Cus[:,i].values))
    sqrtA[:,prn-1]=np.concatenate((nav_prev.sqrtA[:,i].values,nav_curr.sqrtA[:,i].values,nav_next.sqrtA[:,i].values))
    Toe[:,prn-1]=np.concatenate((nav_prev.Toe[:,i].values,nav_curr.Toe[:,i].values,nav_next.Toe[:,i].values))
    Cic[:,prn-1]=np.concatenate((nav_prev.Cic[:,i].values,nav_curr.Cic[:,i].values,nav_next.Cic[:,i].values))
    Omega0[:,prn-1]=np.concatenate((nav_prev.Omega0[:,i].values,nav_curr.Omega0[:,i].values,nav_next.Omega0[:,i].values))
    Cis[:,prn-1]=np.concatenate((nav_prev.Cis[:,i].values,nav_curr.Cis[:,i].values,nav_next.Cis[:,i].values))
    Io[:,prn-1]=np.concatenate((nav_prev.Io[:,i].values,nav_curr.Io[:,i].values,nav_next.Io[:,i].values))
    Crc[:,prn-1]=np.concatenate((nav_prev.Crc[:,i].values,nav_curr.Crc[:,i].values,nav_next.Crc[:,i].values))
    Omega[:,prn-1]=np.concatenate((nav_prev.omega[:,i].values,nav_curr.omega[:,i].values,nav_next.omega[:,i].values))
    OmegaDot[:,prn-1]=np.concatenate((nav_prev.OmegaDot[:,i].values,nav_curr.OmegaDot[:,i].values,nav_next.OmegaDot[:,i].values))
    IDOT[:,prn-1]=np.concatenate((nav_prev.IDOT[:,i].values,nav_curr.IDOT[:,i].values,nav_next.IDOT[:,i].values))
    CodesL2[:,prn-1]=np.concatenate((nav_prev.CodesL2[:,i].values,nav_curr.CodesL2[:,i].values,nav_next.CodesL2[:,i].values))
    GPSWeek[:,prn-1]=np.concatenate((nav_prev.GPSWeek[:,i].values,nav_curr.GPSWeek[:,i].values,nav_next.GPSWeek[:,i].values))
    SVacc[:,prn-1]=np.concatenate((nav_prev.SVacc[:,i].values,nav_curr.SVacc[:,i].values,nav_next.SVacc[:,i].values))
    TGD[:,prn-1]=np.concatenate((nav_prev.TGD[:,i].values,nav_curr.TGD[:,i].values,nav_next.TGD[:,i].values))
    TransTime[:,prn-1]=np.concatenate((nav_prev.TransTime[:,i].values,nav_curr.TransTime[:,i].values,nav_next.TransTime[:,i].values))
    NavTime_prev = (nav_prev.time.values.astype('datetime64[us]')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
    NavTime_curr = (nav_curr.time.values.astype('datetime64[us]')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
    NavTime_next = (nav_next.time.values.astype('datetime64[us]')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
    NavGPSTime[:,prn-1]=np.concatenate((NavTime_prev,NavTime_curr,NavTime_next))
Toc=SVclockBias*0

gpsweek=GPSTime*0; toc=GPSTime*0; svclockbias=GPSTime*0; svclockdrift=GPSTime*0; svclockdriftrate=GPSTime*0; crs=GPSTime*0;
deltaN=GPSTime*0; m0=GPSTime*0; cuc=GPSTime*0; eccentricity=GPSTime*0; cus=GPSTime*0; sqrta=GPSTime*0; toe=GPSTime*0
cic=GPSTime*0; omega0=GPSTime*0; cis=GPSTime*0; io=GPSTime*0; crc=GPSTime*0; omega=GPSTime*0; omegadot=GPSTime*0
idot=GPSTime*0; codesL2=GPSTime*0; svacc=GPSTime*0; tgd=GPSTime*0; transtime=GPSTime*0

for i in range(0,nsat,1):
    
    f = inteprolateNavPar(NavGPSTime[:,i], GPSWeek[:,i]);
    gpsweek[:,i]=f(GPSTime[:,i]);
    
    f = inteprolateNavTime(NavGPSTime[:,i], NavGPSTime[:,i], SVclockBias[:,i]);
    toc[:,i]=f(GPSTime[:,i]);
    
    f = inteprolateNavPar(NavGPSTime[:,i], SVclockBias[:,i])
    svclockbias[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], SVclockDrift[:,i])
    svclockdrift[:,i]=f(GPSTime[:,i])

    f = inteprolateNavPar(NavGPSTime[:,i], SVclockDriftRate[:,i])
    svclockdriftrate[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], Crs[:,i])
    crs[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], DeltaN[:,i])
    deltaN[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], M0[:,i])
    m0[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], Cuc[:,i])
    cuc[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], Eccentricity[:,i])
    eccentricity[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], Cus[:,i])
    cus[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], sqrtA[:,i])
    sqrta[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], Toe[:,i])
    toe[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], Cic[:,i])
    cic[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], Omega0[:,i])
    omega0[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], Cis[:,i])
    cis[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], Io[:,i])
    io[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], Crc[:,i])
    crc[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], Omega[:,i])
    omega[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], OmegaDot[:,i])
    omegadot[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], IDOT[:,i])
    idot[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], CodesL2[:,i])
    codesL2[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], SVacc[:,i])
    svacc[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], TGD[:,i])
    tgd[:,i]=f(GPSTime[:,i])
    
    f = inteprolateNavPar(NavGPSTime[:,i], TransTime[:,i])
    transtime[:,i]=f(GPSTime[:,i])

xs,ys,zs,clks = inteprolateGPS(GPSTime,m0,deltaN,sqrta,eccentricity,omega,cuc,cus,crc,crs,io,idot,cic,cis,omega0,omegadot,tgd,toe,gpsweek,svclockbias,svclockdrift,svclockdriftrate,toc)

#%% read podTEC
GPSTimeR=[]; TEC=[]; XS=[]; YS=[]; ZS=[]; XR=[]; YR=[]; ZR=[]; UT=[]; ID_mission=[]

fname='D:\\INCUBATE\\data\\COSMIC-2\\podTec\\2021\\006\\podTc2_C2E6.2021.006.22.16.0016.G08.01_0001.0001_nc'
dataset = Dataset(fname);
DATE=dt.datetime.strptime('{} {} {}'.format(dataset.day, dataset.month, dataset.year),'%d %m %Y')
GPSTIME=(np.array(DATE,dtype='datetime64')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')

GPSTimeR.append(np.array(dataset.variables.get('time')[:]))
XR.append(np.array(dataset.variables.get('x_LEO')[:])*1e3)
YR.append(np.array(dataset.variables.get('y_LEO')[:])*1e3)
ZR.append(np.array(dataset.variables.get('z_LEO')[:])*1e3)
XS.append(np.array(dataset.variables.get('x_GPS')[:])*1e3)
YS.append(np.array(dataset.variables.get('y_GPS')[:])*1e3)
ZS.append(np.array(dataset.variables.get('z_GPS')[:])*1e3)
prnpod=dataset.prn_id*1
dataset.close()

gpstimepod=np.hstack(GPSTimeR)
utpod=(gpstimepod-GPSTIME)/3600
xrpod=np.hstack(XR)
yrpod=np.hstack(YR)
zrpod=np.hstack(ZR)
xspod=np.hstack(XS)
yspod=np.hstack(YS)
zspod=np.hstack(ZS)

# plt.plot(gpstimepod,xspod,'ko')
# plt.plot(GPSTime[:,prnpod-1],xs[:,prnpod-1],'r.')

#%% create rinex_obs header
rnx_version='{:9.2f}'.format(header['version'])+'           '
systems=header['systems']+' (MIXED)           '
line1=rnx_version+'OBSERVATION DATA    '+systems+'RINEX VERSION / TYPE\n'
line2=header['PGM / RUN BY / DATE']+'PGM / RUN BY / DATE\n'
line3=header['MARKER NAME']+'MARKER NAME\n'
line4=header['MARKER TYPE']+'MARKER TYPE\n'
line5=header['OBSERVER / AGENCY']+'OBSERVER / AGENCY\n'
line6=header['REC # / TYPE / VERS']+'REC # / TYPE / VERS\n'
line7=header['ANT # / TYPE']+'ANT # / TYPE\n'
line8=header['ANTENNA: DELTA X/Y/Z']+'ANTENNA: DELTA X/Y/Z\n'
line9=header['ANTENNA: B.SIGHT XYZ']+'ANTENNA: B.SIGHT XYZ\n'
line10=header['CENTER OF MASS: XYZ']+'CENTER OF MASS: XYZ\n'
line11=header['WAVELENGTH FACT L1/2']+'WAVELENGTH FACT L1/2\n'
if(case=='C1C2L1L2'): line12='     4'+'    C1'+'    C2'+'    L1'+'    L2'+'      '+'      '+'      '+'      '+'      '+'# / TYPES OF OBSERV\n'
line13=header['TIME OF FIRST OBS']+'TIME OF FIRST OBS\n'
line14=header['TIME OF LAST OBS']+'TIME OF LAST OBS\n'
line15='                                                            END OF HEADER\n'
header_msg=line1+line2+line3+line4+line5+line6+line7+line8+line9+line10+line11+line12+line13+line14+line15

#%% create rinex_obs observations
# https://gage.upc.edu/sites/default/files/gLAB/HTML/Observation_Rinex_v2.11.html

rinex_msg=''
fname_rinex='D:\\INCUBATE\\codes\\PNT_simulation\\rinex_LEO.txt'

for i in range(ntimes):
    idx=np.argwhere(~np.isnan(P1[i,:]) & ~np.isnan(P2[i,:]) & ~np.isnan(L1[i,:]) & ~np.isnan(L2[i,:]))
    idx=[int(idx[j][0]) for j in range(len(idx))]
    
    YY=' '+'{:2d}'.format(DATE[i].year-2000)
    MM=' '+'{:2d}'.format(DATE[i].month)
    DD=' '+'{:2d}'.format(DATE[i].day)
    hh=' '+'{:2d}'.format(DATE[i].hour)
    mm=' '+'{:2d}'.format(DATE[i].minute)
    ss=' '+'{:10.7f}'.format(DATE[i].second+DATE[i].microsecond/1e6)
    epoch_flag='  0'
    num_sats='{:3d}'.format(len(idx))
    sats=''
    for j in range(len(idx)):
        if(j>11):
            sats=sats+'\n                                '
        sats=sats+sat_types[idx[j]]
    hdr=YY+MM+DD+hh+mm+ss+epoch_flag+num_sats+sats+'\n'
    rinex_msg=rinex_msg+hdr
    for j in idx:
        p1='{:14.3f}'.format(P1[i,j])+'  '
        p2='{:14.3f}'.format(P2[i,j])+'  '
        l1='{:14.3f}'.format(L1[i,j])+'  '
        l2='{:14.3f}'.format(L2[i,j])+'\n'
        rinex_msg=rinex_msg+p1+p2+l1+l2

#%% write rinex
f = open(fname_rinex, 'w')
f.write(header_msg+rinex_msg)
f.close()


#%%















