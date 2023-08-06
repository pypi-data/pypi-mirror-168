import numpy as np
import numpy.matlib
import georinex as gr
from datetime import datetime
from scipy.interpolate import interp1d

nsatsGPS=32

def read_rinex_obs_GPS(fname):
    nsats=nsatsGPS
    sat_typesGPS=['G'+str(np.arange(1,nsatsGPS+1,1)[i]).zfill(2) for i in range(nsatsGPS)]
    sat_types=np.array(sat_typesGPS)
    
    # header
    header = gr.rinexheader(fname)
    mname=header['MARKER NAME'][:4]
    
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

    return DATE,GPSTime,P1,P2,L1,L2,mname

def read_rinex_nav_GPS(fnameprev,fnamecurr,fnamenext,GPSTime):

    nav_prev=gr.load(fnameprev)
    nav_curr=gr.load(fnamecurr)
    nav_next=gr.load(fnamenext)
    
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
    
    return m0,deltaN,sqrta,eccentricity,omega,cuc,cus,crc,crs,io,idot,cic,cis,omega0,omegadot,tgd,toe,gpsweek,svclockbias,svclockdrift,svclockdriftrate,toc

def inteprolateNavPar(time,par):
#    f=interp1d(time, par,'previous', bounds_error=False)
    idNoNan = tuple([~np.isnan(par)]);
    idNoNan[0][0]=np.array(True);
    f=interp1d(time[idNoNan], par[idNoNan],'previous', fill_value="extrapolate");
    return f

def inteprolateNavPar_linear(time,par):
#    f=interp1d(time, par,'previous', bounds_error=False)
    idNoNan = tuple([~np.isnan(par)]);
    idNoNan[0][0]=np.array(True);
    f=interp1d(time[idNoNan], par[idNoNan],'linear', fill_value="extrapolate");
    return f

def inteprolateNavTime(time,par,parwithNan):
    idNoNan = tuple([~np.isnan(parwithNan)]);
    idNoNan[0][0]=np.array(True);
    f=interp1d(time[idNoNan], par[idNoNan],'previous', fill_value="extrapolate");
    return f
