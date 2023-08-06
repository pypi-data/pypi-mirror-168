import numpy as np
import georinex as gr

def read_rinex_obs_header_func(fname):
    
    x=0
    y=0
    z=0
    
    ant_dx=0
    ant_dy=0
    ant_dz=0

    bsight_dx=0
    bsight_dy=0
    bsight_dz=0

    header = gr.rinexheader(fname)
    mname=header['MARKER NAME'][:4]
    antname=header['ANT # / TYPE'][20:40]
    
    antena_delta_type='NONE'
    bsight_delta_type='NONE'
    
    try: 
        header['APPROX POSITION XYZ']
        x=float(header['APPROX POSITION XYZ'][:15])
        y=float(header['APPROX POSITION XYZ'][16:30])
        z=float(header['APPROX POSITION XYZ'][30:45])
    except:
        counter=0
        
    try: 
        header['ANTENNA: DELTA X/Y/Z']
        ant_dx=float(header['ANTENNA: DELTA X/Y/Z'][:15])
        ant_dy=float(header['ANTENNA: DELTA X/Y/Z'][16:30])
        ant_dz=float(header['ANTENNA: DELTA X/Y/Z'][31:45])
        antena_delta_type='ANTENNA: DELTA X/Y/Z'
    except:
        counter=0
    
    try: 
        header['ANTENNA: DELTA H/E/N']
        ant_dx=float(header['ANTENNA: DELTA H/E/N'][:15])
        ant_dy=float(header['ANTENNA: DELTA H/E/N'][16:30])
        ant_dz=float(header['ANTENNA: DELTA H/E/N'][31:45])
        antena_delta_type='ANTENNA: DELTA H/E/N'
    except:
        counter=0
        
    try: 
        header['ANTENNA: B.SIGHT XYZ']
        bsight_dx=float(header['ANTENNA: B.SIGHT XYZ'][:15])
        bsight_dy=float(header['ANTENNA: B.SIGHT XYZ'][16:30])
        bsight_dz=float(header['ANTENNA: B.SIGHT XYZ'][31:45])
        bsight_delta_type='AANTENNA: B.SIGHT XYZ'
    except:
        counter=0
    
    arp_dxyz=np.array((ant_dx,ant_dy,ant_dz))
    bsight_dxyz=np.array((bsight_dx,bsight_dy,bsight_dz))
    
    return mname, x,y,z, antname, arp_dxyz, bsight_dxyz, antena_delta_type, bsight_delta_type


