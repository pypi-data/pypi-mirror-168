import numpy as np
import datetime as dt

def read_sat_pco_func(fname,doy,year):
    
    file=open(fname, 'r')
    Lines = file.readlines()
    file.close()
    
    date_day=dt.datetime.strptime('{} {}'.format(doy, year),'%j %Y')
    pcoNL1=np.zeros((32))*np.nan
    pcoEL1=np.zeros((32))*np.nan
    pcoUL1=np.zeros((32))*np.nan
    pcoNL2=np.zeros((32))*np.nan
    pcoEL2=np.zeros((32))*np.nan
    pcoUL2=np.zeros((32))*np.nan
    pcvL1=np.zeros((32,18))*np.nan
    pcvL2=np.zeros((32,18))*np.nan
    for i in range(len(Lines)):
        if((Lines[i][:5]=='BLOCK') & (Lines[i][20:21]=='G')  & (Lines[i][60:76]=='TYPE / SERIAL NO') ):
            prn=int(Lines[i][21:23])
            dateinit=dt.datetime(year=9999,month=1,day=1)
            dateend=dt.datetime(year=9999,month=1,day=1)
            for j in range(1,500,1):
    
                if(Lines[i+j][60:70]=='VALID FROM'): dateinit=dt.datetime.strptime(format(Lines[i+j][2:42]),'%Y %m %d %H %M %S.%f')
                if(Lines[i+j][60:71]=='VALID UNTIL'): dateend=dt.datetime.strptime(format(Lines[i+j][2:42]),'%Y %m %d %H %M %S.%f')
    
                if(Lines[i+j][60:78]=='ZEN1 / ZEN2 / DZEN'): 
                    zen1=float(Lines[i+j][4:8])
                    zen2=float(Lines[i+j][9:14])
                    dzen=float(Lines[i+j][16:20])
                    zenstep=np.arange(zen1,zen2+dzen,dzen)
    
                if(Lines[i+j][3:78]=='G01                                                      START OF FREQUENCY'):
                    N=float(Lines[i+j+1][2:10]);  E=float(Lines[i+j+1][12:20]);  U=float(Lines[i+j+1][22:30]); 
                    pcv=(Lines[i+j+2][11:]).split()
                    if(dateinit<date_day<dateend): 
                        pcoNL1[prn-1]=N/1e3; pcoEL1[prn-1]=E/1e3; pcoUL1[prn-1]=U/1e3; 
                        pcvL1[prn-1,:]=np.array(pcv).astype(float)/1e3
                        
                if(Lines[i+j][3:78]=='G02                                                      START OF FREQUENCY'):
                    N=float(Lines[i+j+1][2:10]);  E=float(Lines[i+j+1][12:20]);  U=float(Lines[i+j+1][22:30]); 
                    pcv=(Lines[i+j+2][11:]).split()
                    if(dateinit<date_day<dateend): 
                        pcoNL2[prn-1]=N/1e3; pcoEL2[prn-1]=E/1e3; pcoUL2[prn-1]=U/1e3; 
                        pcvL2[prn-1,:]=np.array(pcv).astype(float)/1e3
                    
                if(Lines[i+j][60:74]=='END OF ANTENNA'):
                    break 

    return pcoEL1,pcoNL1,pcoUL1,pcvL1.T,pcoEL2,pcoNL2,pcoUL2,pcvL2.T,zenstep