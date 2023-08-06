import numpy as np
import datetime as dt

def read_SP3_clkr_func(fname_prev,fname_curr,fname_next,gpstime_day,mname,dsec,nsats):
    
    file=open(fname_prev, 'r')
    Lines = file.readlines()
    file.close()
    ntimes_sp3=len(np.arange(0,24*60*60,dsec))
    clk_sp3_prev=np.zeros((ntimes_sp3))*np.nan
    gpstime_clks_sp3_prev=np.zeros((ntimes_sp3))*np.nan
    for i in range(len(Lines)):
        if(Lines[i][0:7]=='AR '+mname): 
            year=int(Lines[i][8:12])
            month=int(Lines[i][13:15])
            day=int(Lines[i][16:18])
            hour=int(Lines[i][19:21])
            minute=int(Lines[i][22:24])
            second=float(Lines[i][25:34])
            date=dt.datetime.strptime('{} {} {} {} {} {}'.format(day, month, year, hour, minute, second),'%d %m %Y %H %M %S.%f')
            gpstime_tmp=(np.array(date,dtype='datetime64')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
            clk=float(Lines[i][38:59])
            itime=int((gpstime_tmp+24*3600-gpstime_day)/dsec)
            gpstime_clks_sp3_prev[itime]=gpstime_tmp*1
            clk_sp3_prev[itime]=clk*1

    file=open(fname_curr, 'r')
    Lines = file.readlines()
    file.close()
    ntimes_sp3=len(np.arange(0,24*60*60,dsec))
    clk_sp3_curr=np.zeros((ntimes_sp3))*np.nan
    gpstime_clks_sp3_curr=np.zeros((ntimes_sp3))*np.nan
    for i in range(len(Lines)):
        if(Lines[i][0:7]=='AR '+mname): 
            year=int(Lines[i][8:12])
            month=int(Lines[i][13:15])
            day=int(Lines[i][16:18])
            hour=int(Lines[i][19:21])
            minute=int(Lines[i][22:24])
            second=float(Lines[i][25:34])
            date=dt.datetime.strptime('{} {} {} {} {} {}'.format(day, month, year, hour, minute, second),'%d %m %Y %H %M %S.%f')
            gpstime_tmp=(np.array(date,dtype='datetime64')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
            clk=float(Lines[i][38:59])
            itime=int((gpstime_tmp-gpstime_day)/dsec)
            gpstime_clks_sp3_curr[itime]=gpstime_tmp*1
            clk_sp3_curr[itime]=clk*1

    file=open(fname_next, 'r')
    Lines = file.readlines()
    file.close()
    ntimes_sp3=len(np.arange(0,24*60*60,dsec))
    clk_sp3_next=np.zeros((ntimes_sp3))*np.nan
    gpstime_clks_sp3_next=np.zeros((ntimes_sp3))*np.nan
    for i in range(len(Lines)):
        if(Lines[i][0:7]=='AR '+mname): 
            year=int(Lines[i][8:12])
            month=int(Lines[i][13:15])
            day=int(Lines[i][16:18])
            hour=int(Lines[i][19:21])
            minute=int(Lines[i][22:24])
            second=float(Lines[i][25:34])
            date=dt.datetime.strptime('{} {} {} {} {} {}'.format(day, month, year, hour, minute, second),'%d %m %Y %H %M %S.%f')
            gpstime_tmp=(np.array(date,dtype='datetime64')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
            clk=float(Lines[i][38:59])
            itime=int((gpstime_tmp-24*3600-gpstime_day)/dsec)
            gpstime_clks_sp3_next[itime]=gpstime_tmp*1
            clk_sp3_next[itime]=clk*1
    
    gpstime_clks_sp3=np.append(gpstime_clks_sp3_prev,gpstime_clks_sp3_curr)
    gpstime_clks_sp3=np.append(gpstime_clks_sp3,gpstime_clks_sp3_next)
    clk_sp3=np.append(clk_sp3_prev,clk_sp3_curr)
    clk_sp3=np.append(clk_sp3,clk_sp3_next)

    return gpstime_clks_sp3,clk_sp3

