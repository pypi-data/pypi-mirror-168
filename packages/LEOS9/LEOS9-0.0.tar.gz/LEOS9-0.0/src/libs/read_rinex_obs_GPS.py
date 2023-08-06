import numpy as np
import georinex as gr
from datetime import datetime

nsatsGPS=32

def read_rinex_obs_GPS_func(fname):
    
    nsats=nsatsGPS
    sat_typesGPS=['G'+str(np.arange(1,nsatsGPS+1,1)[i]).zfill(2) for i in range(nsatsGPS)]
    sat_types=np.array(sat_typesGPS)
    
    # observations
    obs = gr.load(fname)
    obs_sats = obs.sv.values
    obs_times = obs.time
    obs_types = list(obs)
    # coords = list(obs.coords)
    ntimes=len(obs_times)

    case='NONE'
    P1 = np.full((ntimes,nsats),np.nan);
    P2 = np.full((ntimes,nsats),np.nan);
    L1 = np.full((ntimes,nsats),np.nan);
    L2 = np.full((ntimes,nsats),np.nan);
    D1 = np.full((ntimes,nsats),np.nan);
    D2 = np.full((ntimes,nsats),np.nan);

    if( ('D1' in obs_types) & ('D2' in obs_types) & ('L1' in obs_types) & ('L2' in obs_types) & ('C1' in obs_types) & ('C2' in obs_types)):
        case='D1D2C1C2L1L2'

    elif( ('D1' in obs_types) & ('D2' in obs_types) & ('L1' in obs_types) & ('L2' in obs_types) & ('C1' in obs_types) & ('P2' in obs_types)):
        case='D1D2C1P2L1L2'

    elif( ('L1' in obs_types) & ('L2' in obs_types) & ('C1' in obs_types) & ('P2' in obs_types)):
        case='C1P2L1L2'
        
    elif( ('L1' in obs_types) & ('L2' in obs_types) & ('C1' in obs_types) & ('C2' in obs_types)):
        case='C1C2L1L2'

    elif( ('L1C' in obs_types) & ('L2W' in obs_types) & ('C1W' in obs_types) & ('C2W' in obs_types)):
        case='C1WC2WL1CL2C'


    if(case=='D1D2C1C2L1L2'):
        for i in range(len(obs_sats)):
            constelation=obs.sv.values[i][0]
            prn=int(obs.sv.values[i][1:3])
            if constelation=='G':
                D1[:,prn-1] = obs.D1[:,i].values*1
                D2[:,prn-1] = obs.D2[:,i].values*1
                P1[:,prn-1] = obs.C1[:,i].values*1
                P2[:,prn-1] = obs.C2[:,i].values*1
                L1[:,prn-1] = obs.L1[:,i].values*1
                L2[:,prn-1] = obs.L2[:,i].values*1   

    if(case=='D1D2C1P2L1L2'):
        for i in range(len(obs_sats)):
            constelation=obs.sv.values[i][0]
            prn=int(obs.sv.values[i][1:3])
            if constelation=='G':
                D1[:,prn-1] = obs.D1[:,i].values*1
                D2[:,prn-1] = obs.D2[:,i].values*1
                P1[:,prn-1] = obs.C1[:,i].values*1
                P2[:,prn-1] = obs.P2[:,i].values*1
                L1[:,prn-1] = obs.L1[:,i].values*1
                L2[:,prn-1] = obs.L2[:,i].values*1   
                
    if(case=='C1C2L1L2'):
        for i in range(len(obs_sats)):
            constelation=obs.sv.values[i][0]
            prn=int(obs.sv.values[i][1:3])
            if constelation=='G':
                P1[:,prn-1] = obs.C1[:,i].values*1
                P2[:,prn-1] = obs.C2[:,i].values*1
                L1[:,prn-1] = obs.L1[:,i].values*1
                L2[:,prn-1] = obs.L2[:,i].values*1            
            
    if(case=='C1P2L1L2'):
        for i in range(len(obs_sats)):
            constelation=obs.sv.values[i][0]
            prn=int(obs.sv.values[i][1:3])
            if constelation=='G':
                P1[:,prn-1] = obs.C1[:,i].values*1
                P2[:,prn-1] = obs.P2[:,i].values*1
                L1[:,prn-1] = obs.L1[:,i].values*1
                L2[:,prn-1] = obs.L2[:,i].values*1            
    # print(obs_types)
    if(case=='C1WC2WL1CL2C'):
        for i in range(len(obs_sats)):
            constelation=obs.sv.values[i][0]
            prn=int(obs.sv.values[i][1:3])
            if constelation=='G':
                P1[:,prn-1] = obs.C1W[:,i].values*1
                P2[:,prn-1] = obs.C2W[:,i].values*1
                L1[:,prn-1] = obs.L1C[:,i].values*1
                L2[:,prn-1] = obs.L2W[:,i].values*1   
                
    DATE    = obs_times.values.astype('datetime64[us]')
    GPSTime = (DATE-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
    GPSTime = np.matlib.repmat(GPSTime,nsats,1)
    GPSTime = GPSTime.T*1
    DATE=DATE.astype(datetime)
    
    D1[D1==0]=np.nan
    D2[D2==0]=np.nan
    P1[P1==0]=np.nan
    P2[P2==0]=np.nan
    L1[L1==0]=np.nan
    L2[L2==0]=np.nan

    return DATE,GPSTime,D1,D2,P1,P2,L1,L2,case
