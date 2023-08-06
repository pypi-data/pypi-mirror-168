import numpy as np
from libs.convert_xyz_to_llh import convert_xyz_to_llh_func

h0 =  0.6078
h2 = -0.0006
h3 =  0.292
l0 =  0.0847
l2 =  0.0002
l3 =  0.015
MS2E = 332946.0
MM2E = 0.01230002

def model_tides_func(xr,yr,zr,x_moon,y_moon,z_moon,x_sun,y_sun,z_sun,ntimes):

    tidex=xr*np.nan
    tidey=xr*np.nan
    tidez=xr*np.nan
    
    for i in range(ntimes):
        x=np.nanmean(xr[i,:])
        y=np.nanmean(yr[i,:])
        z=np.nanmean(zr[i,:])
        xsun=np.nanmean(x_sun[i,:])
        ysun=np.nanmean(y_sun[i,:])
        zsun=np.nanmean(z_sun[i,:])
        xmoon=np.nanmean(x_moon[i,:])
        ymoon=np.nanmean(y_moon[i,:])
        zmoon=np.nanmean(z_moon[i,:])
        
        lat,lon,alt=convert_xyz_to_llh_func(x,y,z)
        en = np.array([-np.cos(lon) * np.sin(lat),-np.sin(lon) * np.sin(lat),+np.cos(lat)])
        
        r_sun=np.array((xsun,ysun,zsun))
        r_moon=np.array((xmoon,ymoon,zmoon))
        r_rec=np.array((x,y,z))
        
        sunDistance = np.sqrt(r_sun[0]*r_sun[0] + r_sun[1]*r_sun[1] + r_sun[2]*r_sun[2])
        moonDistance = np.sqrt(r_moon[0]*r_moon[0] + r_moon[1]*r_moon[1] + r_moon[2]*r_moon[2]);
        receiverDistance = np.sqrt(r_rec[0]*r_rec[0] + r_rec[1]*r_rec[1] + r_rec[2]*r_rec[2]);
        
        h = h0 + h2*(3*np.sin(en)*np.sin(en) - 1)/2;
        l = l0 + l2*(3*np.sin(en)*np.sin(en) - 1)/2;
        
        
        sunPosUni=r_sun/sunDistance
        moonPosUni=r_moon/moonDistance
        receiverPosUni=r_rec/receiverDistance
        
        scalarSunRec=np.dot(sunPosUni,receiverPosUni)
        scalarMoonRec = np.dot(moonPosUni,receiverPosUni)
        
        auxSun = sunPosUni - scalarSunRec*receiverPosUni
        auxMoon = moonPosUni - scalarMoonRec*receiverPosUni
        
        RecPos2SunPos = receiverDistance/sunDistance
        RecPos2MoonPos = receiverDistance/moonDistance
        
        solidTideDisplacement=0
        
        solidTideDisplacement=solidTideDisplacement+MS2E * RecPos2SunPos * RecPos2SunPos * RecPos2SunPos * receiverDistance *( 	h * receiverPosUni * (3.0/2.0*scalarSunRec*scalarSunRec - 1.0/2.0) + 3.0 * l * scalarSunRec * auxSun) + MM2E * RecPos2MoonPos * RecPos2MoonPos * RecPos2MoonPos * receiverDistance *( h * receiverPosUni * (3.0/2.0*scalarMoonRec*scalarMoonRec - 1.0/2.0) + 3.0 * l * scalarMoonRec * auxMoon)
        solidTideDisplacement=solidTideDisplacement+MM2E * RecPos2MoonPos * RecPos2MoonPos * RecPos2MoonPos * RecPos2MoonPos * receiverDistance *( h3 * receiverPosUni * (5.0/2.0*scalarMoonRec*scalarMoonRec*scalarMoonRec - 3.0/2.0*scalarMoonRec) + l3 * (15.0/2.0*scalarMoonRec*scalarMoonRec - 3.0/2.0) * auxMoon)
        
        tidex[i,:]=solidTideDisplacement[0]*1
        tidey[i,:]=solidTideDisplacement[1]*1
        tidez[i,:]=solidTideDisplacement[2]*1

    return tidex, tidey, tidez
