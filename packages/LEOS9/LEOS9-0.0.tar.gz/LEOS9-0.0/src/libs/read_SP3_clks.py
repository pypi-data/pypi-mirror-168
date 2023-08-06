import numpy as np
import datetime as dt

def read_SP3_clks_func(fname_prev,fname_curr,fname_next,gpstime_day,dsec,nsats):
    
    file=open(fname_prev, 'r')
    Lines = file.readlines()
    file.close()
    ntimes_sp3=len(np.arange(0,24*60*60,dsec))
    clk_sp3_prev=np.zeros((ntimes_sp3,nsats))*np.nan
    gpstime_clks_sp3_prev=np.zeros((ntimes_sp3,nsats))*np.nan
    for i in range(len(Lines)):
        if(Lines[i][0:4]=='AS G'): 
            line=Lines[i].split()
            prn=int(line[1][1:])
            year=int(line[2])
            month=int(line[3])
            day=int(line[4])
            hour=int(line[5])
            minute=int(line[6])
            second=float(line[7])
            date=dt.datetime.strptime('{} {} {} {} {} {}'.format(day, month, year, hour, minute, second),'%d %m %Y %H %M %S.%f')
            gpstime_tmp=(np.array(date,dtype='datetime64')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
            clk=float(line[9])
            itime=int((gpstime_tmp+24*3600-gpstime_day)/dsec)
            gpstime_clks_sp3_prev[itime,prn-1]=gpstime_tmp*1
            clk_sp3_prev[itime,prn-1]=clk*1
    
    file=open(fname_curr, 'r')
    Lines = file.readlines()
    file.close()
    ntimes_sp3=len(np.arange(0,24*60*60,dsec))
    clk_sp3_curr=np.zeros((ntimes_sp3,nsats))*np.nan
    gpstime_clks_sp3_curr=np.zeros((ntimes_sp3,nsats))*np.nan
    for i in range(len(Lines)):
        if(Lines[i][0:4]=='AS G'): 
            line=Lines[i].split()
            prn=int(line[1][1:])
            year=int(line[2])
            month=int(line[3])
            day=int(line[4])
            hour=int(line[5])
            minute=int(line[6])
            second=float(line[7])
            date=dt.datetime.strptime('{} {} {} {} {} {}'.format(day, month, year, hour, minute, second),'%d %m %Y %H %M %S.%f')
            gpstime_tmp=(np.array(date,dtype='datetime64')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
            clk=float(line[9])
            itime=int((gpstime_tmp-gpstime_day)/dsec)
            gpstime_clks_sp3_curr[itime,prn-1]=gpstime_tmp*1
            clk_sp3_curr[itime,prn-1]=clk*1

    file=open(fname_next, 'r')
    Lines = file.readlines()
    file.close()
    ntimes_sp3=len(np.arange(0,24*60*60,dsec))
    clk_sp3_next=np.zeros((ntimes_sp3,nsats))*np.nan
    gpstime_clks_sp3_next=np.zeros((ntimes_sp3,nsats))*np.nan
    for i in range(len(Lines)):
        if(Lines[i][0:4]=='AS G'): 
            line=Lines[i].split()
            prn=int(line[1][1:])
            year=int(line[2])
            month=int(line[3])
            day=int(line[4])
            hour=int(line[5])
            minute=int(line[6])
            second=float(line[7])
            date=dt.datetime.strptime('{} {} {} {} {} {}'.format(day, month, year, hour, minute, second),'%d %m %Y %H %M %S.%f')
            gpstime_tmp=(np.array(date,dtype='datetime64')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
            clk=float(line[9])
            itime=int((gpstime_tmp-24*3600-gpstime_day)/dsec)
            gpstime_clks_sp3_next[itime,prn-1]=gpstime_tmp*1
            clk_sp3_next[itime,prn-1]=clk*1
    
    gpstime_clks_sp3=np.vstack([gpstime_clks_sp3_prev,gpstime_clks_sp3_curr])
    gpstime_clks_sp3=np.vstack([gpstime_clks_sp3,gpstime_clks_sp3_next])
    clk_sp3=np.vstack([clk_sp3_prev,clk_sp3_curr])
    clk_sp3=np.vstack([clk_sp3,clk_sp3_next])

    return gpstime_clks_sp3,clk_sp3