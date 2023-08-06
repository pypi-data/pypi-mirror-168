#!/usr/bin/env python
"""
Modul mame:		
	ionofunclib.py
Description:	
	collection of used functions	
Version: v1	
Author:		Mainul Hoque
Created:	20.11.2014
Copyright:	(c) Mainul Hoque 2014
Mail:		Mainul.Hoque@dlr.de
Licence:	DLR
#-------------------------------------------------------------------------------
"""
import numpy as np
import datetime
import sys
import libs.ionoconslib as mycons

def XYZtoAzEl(sx,sy,sz,x,y,z):
    [lat,lon,h]=ecef2geodetic(sx,sy,sz);
    dx=x-sx;
    dy=y-sy;
    dz=z-sz;
    
    dn = (-(np.sin(lat)*np.cos(lon))*dx) - ((np.sin(lat)*np.sin(lon))*dy) + (np.cos(lat)*dz);
    de = ((-np.sin(lon)*dx)+(np.cos(lon))*dy);
    du = (((np.cos(lat)*np.cos(lon)))*dx) + ((np.cos(lat)*np.sin(lon))*dy) + (np.sin(lat)*dz);
    
    ro = np.sqrt(de*de + dn*dn);
    
    az=np.arctan(de/dn);
    el=np.arctan(du/ro);
    
    # checking of the quadrant
    with np.errstate(invalid='ignore'):
        az[(de>0) & (dn<0)] =   np.pi - abs(az[(de>0) & (dn<0)]);
        az[(de<0) & (dn<0)] =   np.pi + abs(az[(de<0) & (dn<0)]);
        az[(de<0) & (dn>0)] = 2*np.pi - abs(az[(de<0) & (dn>0)]);
        az[az<0]    = 2*np.pi + az[az<0];
        az[az>2*np.pi] = az[az>2*np.pi] - 2*np.pi
    
    return el,az

def stec2vtecsat(latr,lonr,altr,elrad,azrad,hion,stec):
    Re=6371000.0;

    temp   = (np.pi/2) - (elrad) - (np.arcsin((Re/(Re+hion)*np.cos(elrad))));
    latrad = np.arcsin((np.sin(latr*np.pi/180.0)*np.cos(temp)) + (np.cos(latr*np.pi/180.0)*np.sin(temp)*np.cos(azrad)));
    lonrad = lonr*np.pi/180.0 + (np.arcsin((np.sin(temp)*np.sin(azrad))/np.cos(latrad)));
    latipp =latrad*180/np.pi;
    lonipp = (lonrad*180/np.pi) - np.floor( (lonrad*180/np.pi) / 360 + 0.5) * 360
    
    R=(Re+altr)/(Re+hion);
    MF=(np.sin(elrad)+np.sqrt(R**(-2)-np.cos(elrad)**2))/(1+R**(-1));
    vtecipp=stec*MF;
    
    return latipp,lonipp,vtecipp

def stec2vtecgrd(latr,lonr,altr,elrad,azrad,hion,stec):
    Re=6371000.0;

    temp   = (np.pi/2) - (elrad) - (np.arcsin((Re/(Re+hion)*np.cos(elrad))));
    latrad = np.arcsin((np.sin(latr*np.pi/180.0)*np.cos(temp)) + (np.cos(latr*np.pi/180.0)*np.sin(temp)*np.cos(azrad)));
    lonrad = lonr*np.pi/180.0 + (np.arcsin((np.sin(temp)*np.sin(azrad))/np.cos(latrad)));
    latipp =latrad*180/np.pi;
    lonipp = (lonrad*180/np.pi) - np.floor( (lonrad*180/np.pi) / 360 + 0.5) * 360
   
    zenit     = (np.pi/2) - elrad;
    zenitvtec = np.arcsin((Re/(Re+hion))*np.sin(zenit));
    vtecipp   = stec*np.cos(zenitvtec);
    
    return latipp,lonipp,vtecipp
    
def UT2LT(UT_hrs, lon_deg):
		"""Universal Time to Local Time  conversion in hours
		Syntax:
			LT = UT2LT(UT_hrs, lon_deg)
		Description:
			UT_hrs = universal time Vector in hours
			lon_deg = geographic longitude Vector in degrees
			LT = local time Vector in hours
		"""
		LT = UT_hrs + lon_deg/360. * 24.
		LT = np.select([LT < 0, LT >= 0], [LT + 24, LT])
		return np.select([LT > 24, LT <= 24], [LT - 24, LT])
		
def geoLat2magLat(lat_rad, lon_deg):
		"""geodetic latitude to geomagnetic latitude conversion using Dipole Approximation
		Syntax:
			latm_rad = geoLat2magLat(lat_rad, lon_deg)
		Description
			lat_rad = geographic latitude Vector in radians
			lon_deg = geographic longitude Vector in degrees
			latm_rad = geomagnetic latitude Vector in radians
		"""		
		return np.arcsin(np.sin(lat_rad) * np.sin(mycons.phi_GNP) + np.cos(lat_rad) * np.cos(mycons.phi_GNP) * np.cos(np.deg2rad(lon_deg) - mycons.lambda_GNP)) #in radians
		
	
def sunDecl(doy):
		"""sun declination in radians
		Syntax: 
			delta = sunDecl(doy)
		Description:
			doy = day of year Vector
			delta = sun dctlination angle Vector in radians
		"""
		
		return 23.44 * np.sin(0.9856 * (doy - 80.7) * np.pi/180.) * np.pi/180. 
		
def sunZenith(doy, lat_rad):
		"""solar zenith angle parameters
	    Syntax:
	    	cos_solzenith, solzenith_factor = sunZenith(doy, lat_rad)
		Description:
			doy = day of year Vector
			lat_rad = WGS84 geographic 
		"""
		delta = sunDecl(doy)
		cos_solzenith 		= np.sin(lat_rad) * np.sin(delta) + np.cos(lat_rad) * np.cos(delta) - lat_rad*2./np.pi*np.sin(delta)
		cos_solzenith_ch 	= np.sin(lat_rad) * np.sin(delta) + np.cos(lat_rad) * np.cos(delta)
		solzenith_factor 	= cos_solzenith_ch + 0.4                    # square root is omitted, it was a printing mistake in Jakowski et al .[2011] 
		return cos_solzenith, solzenith_factor
	

def geodetic2ecef(latrad, lonrad, altm):	
    """Convert geodetic coordinates to ECEF.
    Syntax:
		x, y, z = geodetic2ecef(latrad, lonrad, altm)
	Description:
		latrad = geographic latitude Vector in radians
		lonrad = geographic longitude Vector in radians
		altm = altitude Vector in meter (height above Earth's surface)
		x = ECEF x coordinate Vector in meters
		y = ECEF y coordinate Vector in meters
		z = ECEF z coordinate Vector in meters
    """
    altkm = altm/1000.
    xi = np.sqrt(1 - mycons.esq * np.sin(latrad) * np.sin(latrad))
    x = (mycons.smaj / xi + altkm) * np.cos(latrad) * np.cos(lonrad)
    y = (mycons.smaj / xi + altkm) * np.cos(latrad) * np.sin(lonrad)
    z = (mycons.smaj / xi * (1 - mycons.esq) + altkm) * np.sin(latrad)
    return x*1000., y*1000., z*1000.

def ecef2geodetic(x, y, z):
    """
    Syntax:
		latrad, lonrad, altm = ecef2geodetic(x, y, z)
    Description:
		x = ECEF x coordinate Vector in meters
		y = ECEF y coordinate Vector in meters
		z = ECEF z coordinate Vector in meters 
		latrad = geographic latitude Vector in radians
		lonrad = geographic longitude Vector inradians
		altm = altitude Vector in meter (height above Earth's surface)		
	Ref:
	Convert ECEF coordinates to geodetic.
    J. Zhu, "Conversion of Earth-centered Earth-fixed coordinates \
    to geodetic coordinates," IEEE Transactions on Aerospace and \
    Electronic Systems, vol. 30, pp. 957-961, 1994.
    
    """
    x = x/1000. #km
    y = y/1000. #km
    z = z/1000. #km   
    r = np.sqrt(x **2 + y **2)
    Esq = mycons.smaj **2 - mycons.smin **2
    F = 54 * mycons.smin **2 * z **2
    G = r **2 + (1 - mycons.esq) * z **2 - mycons.esq * Esq
    C = (mycons.esq **2 * F * r **2) / (np.power(G, 3))
    S = np.sqrt(1 + C + np.sqrt(C **2 + 2 * C))
    P = F / (3 * np.power((S + 1 / S + 1), 2) * G **2)
    Q = np.sqrt(1 + 2 * mycons.esq **2 * P)
    r_0 =  (-(P * mycons.esq * r) / (1 + Q) + np.sqrt(0.5 * mycons.smaj **2 *(1 + 1.0 / Q) -  P * (1 - mycons.esq) * z **2 / (Q * (1 + Q)) - 0.5 * P * r **2))
    U = np.sqrt(np.power((r - mycons.esq * r_0), 2) + z **2)
    V = np.sqrt(np.power((r - mycons.esq * r_0), 2) + (1 - mycons.esq) * z **2)
    Z_0 = mycons.smin **2 * z / (mycons.smaj * V)
    h = U * (1 - mycons.smin **2 / (mycons.smaj * V))
    lat = np.arctan((z + mycons.e1sq * Z_0) / r)
    lon = np.arctan2(y, x)
    return lat, lon, h*1000.


def rayinterpoints(x1, y1, z1, x2, y2, z2,  parset):
	"""
	Syntax:
		x, y, z, dsm = rayinterpoints(x1, y1, z1, x2, y2, z2,  parset)
	Description:
		x1 = ECEF x coordinate of point P1 (e.g., Rx at ground)
	    y1 = ECEF y coordinate of point P1
	    z1 = ECEF z coordinate of point P1
		x2 = ECEF x coordinate of point P2 (e.g., GNSS Tx)
	    y2 = ECEF y coordinate of point P2
	    z2 = ECEF z coordinate of point P2
	    parset 	= {	"IonLimitm" : IonLimitm,	"IonStepm" : IonStepm,	"PlasmaStepm" : PlasmaStepm}
	    IonLimitm = altitude limit of ionosphere in meter (above Earth's surfface)
	    IonStepm = step size of each layer in meter 
	    PlasmaStepm = step size of the plasmasphere which extends from IonLimitm until Tx height
	    x = ECEF x coordinate Vector of ray inter points between P1 & P2
	    y = ECEF y coordinate Vector of ray inter points between P1 & P2
	    z = ECEF z coordinate of ray inter points between P1 & P2		
	"""
	
	rangeLoSm = np.sqrt( (x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) #m

	
	a = np.arange(0, parset['IonLimitm']*4, parset['IonStepm']) 
	
	k = a*100./rangeLoSm
	
	x = ( (100 - k)*x1 + k*x2 )/100.
	y = ( (100 - k)*y1 + k*y2 )/100.
	z = ( (100 - k)*z1 + k*z2 )/100.
	r = np.sqrt(x**2 + y**2 + z**2)

	indices = np.nonzero( r < (mycons.REm + parset['IonLimitm']))
	
# 	print (np.shape(a), np.shape(indices))
	x = x[indices]
	y = y[indices]
	z = z[indices]

	dsm = np.tile(parset['IonStepm'], np.shape(x))
	#print np.shape(dsm), np.shape(x)

	a = np.arange(a[np.amax(indices) + 1], rangeLoSm, parset['PlasmaStepm']) #after one step 
	k = a*100/rangeLoSm


	x = np.hstack( (x, ((100 -k)*x1 + k*x2 )/100, x2) )
	y = np.hstack( (y, ((100-k)*y1 + k*y2 )/100, y2) )
	z = np.hstack( (z, ((100-k)*z1 + k*z2 )/100, z2) )

	tmp = np.tile(parset['PlasmaStepm'], (np.size(a)-1, 1))
	
	dsm = np.hstack( (dsm, np.squeeze(tmp), rangeLoSm - np.amax(a), 0) )
	
	
	if np.fabs(np.sum(dsm) - rangeLoSm) > 1. :
		print('Error in myfunc.rayinterpoints:', np.fabs(np.sum(dsm) - rangeLoSm))
	
	return x, y, z, dsm

def getVTECntcm42(doy, tsecday, Latdeg, Londeg, xsoln):
     """
     This function returns VTEC compute from operation NTCM model (42 coefficients) at IPP location 
     """        
                
     Latmrad = geoLat2magLat(np.deg2rad(Latdeg), np.deg2rad(Londeg))  
     LT = UT2LT(tsecday/3600., Londeg)
     [cos_solzenith, solzenith_factor] = sunZenith(doy, np.deg2rad(Latdeg))
    
     Diurnal = np.concatenate((solzenith_factor, np.cos(2.*np.pi*LT/24.), np.sin(2.*np.pi*LT/24.), np.cos(2.*np.pi*LT/12.), np.sin(2.*np.pi*LT/12.), np.cos(2.*np.pi*LT/8.), np.sin(2.*np.pi*LT/8.)), axis=0)
            
     Diurnal = Diurnal.transpose() * np.concatenate((np.ones(LT.shape).transpose(), np.tile(cos_solzenith.transpose(), (1, 6))), axis=1)   
     Geomlat = Diurnal * np.tile(np.cos(Latmrad).transpose(), [1, 7])            
     Crest1 = np.tile(np.exp(-(Latmrad * 180./np.pi - 16.) ** 2./288.).transpose(),[1, 14]) * np.concatenate((Diurnal, Geomlat), axis=1)
     Crest2 = np.tile(np.exp(-(Latmrad * 180./np.pi + 10.) ** 2./338.).transpose(), [1, 14]) * np.concatenate((Diurnal, Geomlat), axis=1)
            
     #xsoln =  parset['ionomodcoeff']       
            
     vTECmodel =  np.sum(np.concatenate((Diurnal, Geomlat, Crest1, Crest2), axis=1) * np.tile(xsoln, [len(Diurnal), 1]), axis=1)
     Latmrad = np.squeeze(Latmrad)
     return Latmrad, vTECmodel      

def getGeomHeight(h0):
     """
     This function returns height array determined by geometric series 
     start height h0 in km
     """        
                
     #h0 = 350
     dh1 = 2 
     q = 1.05
     #n = 0: 127
     n = np.arange(0, 127, 1) 
     hkm = h0 + dh1 * (q**n  - 1)/(q -1)
     
     
     
     return hkm      
