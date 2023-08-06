import numpy as np
import datetime as dt
from scipy.interpolate import griddata

def readF107(fnamef107):
    lineList = [line.rstrip('\n') for line in open(fnamef107)]

    yearF107 = np.asarray([i[0:3] for i in lineList]).astype(int);
    yearF107[yearF107>=58]=yearF107[yearF107>=58]+1900;
    yearF107[yearF107<58]=yearF107[yearF107<58]+2000;
    
    mthF107 = np.asarray([i[3:6] for i in lineList]).astype(int);
    dayF107 = np.asarray([i[6:9] for i in lineList]).astype(int);
    F107_001 = np.asarray([i[39:44] for i in lineList]).astype(float);
    F107_081 = np.asarray([i[44:49] for i in lineList]).astype(float);
    F107_365 = np.asarray([i[49:54] for i in lineList]).astype(float);
    
    doyF107=yearF107*0;
    gpstF107=yearF107*0;
    for i in range(len(yearF107)):
        DATE=dt.datetime.strptime('{} {} {}'.format(dayF107[i], mthF107[i], yearF107[i]),'%d %m %Y');
        doyF107[i]=DATE.timetuple().tm_yday;
        gpstF107[i]=(np.array(DATE,dtype='datetime64')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
    
    return doyF107,yearF107,gpstF107,F107_001,F107_081,F107_365

def interpF107(gpstF107,allf107,doy,year):
    if np.isscalar(doy):
        dates_list=(str(int(doy))+' '+str(year));
        doy=np.array([doy]);
        year=np.array([year]);

    datestr = [None] * doy.shape[0]
    for i in range(doy.shape[0]):
        datestr[i]=(str(int(doy[i]))+' '+str(int(year[i])));
    
    dates_list = [dt.datetime.strptime(date, '%j %Y') for date in datestr]
    gpstime=(np.array(dates_list,dtype='datetime64')-np.datetime64('1980-01-06T00:00:00'))/ np.timedelta64(1,'s')
    f107=griddata((gpstF107),allf107,gpstime,'nearest',fill_value="extrapolate");

    return f107
