import numpy as np
import datetime as dt

def read_SP3_clks_5s_func(fname_prev,fname_curr,fname_next,gpstime_day,nsats):
    
    file=open(fname_prev, 'r')
    Lines = file.readlines()
    file.close()
    ntimes_sp3=len(np.arange(0,24*60*60,5))
    clk_sp3_prev=np.zeros((ntimes_sp3,nsats))*np.nan
    gpstime_clks_sp3_prev=np.zeros((ntimes_sp3,nsats))*np.nan
    for i in range(len(Lines)):
        if(Lines[i][0:4]=='AS G'): 
            prn=int(Lines[i][4:6])
            year=int(Lines[i][8:12])
            month=int(Lines[i][13:15])
            day=int(Lines[i][16:18])
            hour=int(Lines[i][19:21])
            minute=int(Lines[i][22:24])
            second=float(Lines[i][25:34])
            date=dt.datetime.strptime('{} {} {} {} {} {}'.format(day, month, year, hour, minute, second),'%d %m %Y %H %M %S.%f')
            gpstime_tmp=(np.array(date,dtype='datetime64')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
            clk=float(Lines[i][38:59])
            itime=int((gpstime_tmp+24*3600-gpstime_day)/5)
            gpstime_clks_sp3_prev[itime,prn-1]=gpstime_tmp*1
            clk_sp3_prev[itime,prn-1]=clk*1

    file=open(fname_curr, 'r')
    Lines = file.readlines()
    file.close()
    ntimes_sp3=len(np.arange(0,24*60*60,5))
    clk_sp3_curr=np.zeros((ntimes_sp3,nsats))*np.nan
    gpstime_clks_sp3_curr=np.zeros((ntimes_sp3,nsats))*np.nan
    for i in range(len(Lines)):
        if(Lines[i][0:4]=='AS G'): 
            prn=int(Lines[i][4:6])
            year=int(Lines[i][8:12])
            month=int(Lines[i][13:15])
            day=int(Lines[i][16:18])
            hour=int(Lines[i][19:21])
            minute=int(Lines[i][22:24])
            second=float(Lines[i][25:34])
            date=dt.datetime.strptime('{} {} {} {} {} {}'.format(day, month, year, hour, minute, second),'%d %m %Y %H %M %S.%f')
            gpstime_tmp=(np.array(date,dtype='datetime64')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
            clk=float(Lines[i][38:59])
            itime=int((gpstime_tmp-gpstime_day)/5)
            gpstime_clks_sp3_curr[itime,prn-1]=gpstime_tmp*1
            clk_sp3_curr[itime,prn-1]=clk*1

    file=open(fname_next, 'r')
    Lines = file.readlines()
    file.close()
    ntimes_sp3=len(np.arange(0,24*60*60,5))
    clk_sp3_next=np.zeros((ntimes_sp3,nsats))*np.nan
    gpstime_clks_sp3_next=np.zeros((ntimes_sp3,nsats))*np.nan
    for i in range(len(Lines)):
        if(Lines[i][0:4]=='AS G'): 
            prn=int(Lines[i][4:6])
            year=int(Lines[i][8:12])
            month=int(Lines[i][13:15])
            day=int(Lines[i][16:18])
            hour=int(Lines[i][19:21])
            minute=int(Lines[i][22:24])
            second=float(Lines[i][25:34])
            date=dt.datetime.strptime('{} {} {} {} {} {}'.format(day, month, year, hour, minute, second),'%d %m %Y %H %M %S.%f')
            gpstime_tmp=(np.array(date,dtype='datetime64')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
            clk=float(Lines[i][38:59])
            itime=int((gpstime_tmp-24*3600-gpstime_day)/5)
            gpstime_clks_sp3_next[itime,prn-1]=gpstime_tmp*1
            clk_sp3_next[itime,prn-1]=clk*1
    
    gpstime_clks_sp3=np.vstack([gpstime_clks_sp3_prev,gpstime_clks_sp3_curr])
    gpstime_clks_sp3=np.vstack([gpstime_clks_sp3,gpstime_clks_sp3_next])
    clk_sp3=np.vstack([clk_sp3_prev,clk_sp3_curr])
    clk_sp3=np.vstack([clk_sp3,clk_sp3_next])

    return gpstime_clks_sp3,clk_sp3