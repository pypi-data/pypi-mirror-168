#!/usr/bin/env python
"""
Modul mame:		
	ionofunclib.py
Description:	
	collection of used functions	
Version: v1	
Author:	Mainul Hoque
Created:	20.11.2014
Copyright:	(c) Mainul Hoque 2014
Mail:		Mainul.Hoque@dlr.de
Licence:	DLR
#-------------------------------------------------------------------------------
adapted by Fabricio Prol in Jan. 2020
    Functions included: stec2vtec, XYZtoAzEl

#-------------------------------------------------------------------------------
"""
import numpy as np
#import datetime
#import sys

smaj = 6378.137                                                     #semimajor axis in km
smin = 6356.7523142                                                  #semi minor axis in km
esq = 6.69437999014 * 0.001                                       
e1sq = 6.73949674228 * 0.001 
flat = 1 / 298.257223563                                             #flattening
REm = 6371211.266 #Earth's mean radius in meter

def xyz2azel(sx,sy,sz,x,y,z):
    [lat,lon,h]=XYZtoLLH(sx,sy,sz);
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

def XYZtoLLH(X,Y,Z):
#    np.warnings.filterwarnings('ignore')
    a=6378137;
    e2=0.0066943799013;
    L=np.array(np.arctan(abs(Y/X))); # lon
    idx1=tuple([(Y>0) & (X<=0)]);
    idx2=tuple([(Y<=0) & (X>0)]);
    idx3=tuple([(Y<=0) & (X<0)]);
    
    L[idx1]=  np.pi-L[idx1];
    L[idx2]=2*np.pi-L[idx2];
    L[idx3]=  np.pi+L[idx3];
    
    B0=np.arctan(Z/np.sqrt(X*X+Y*Y)); # lat
    B0Check=B0*1;
    for i in range(1,6+1,1):
        N=a/np.sqrt(1-e2*np.sin(B0)*np.sin(B0));
        H=Z/np.sin(B0)-N*(1-e2);
        B=np.array(np.arctan(Z*(N+H)/(np.sqrt(X*X+Y*Y)*(N*(1-e2)+H))));
        B0=B*1;
    
    B[B0Check==0]=0;
#    np.warnings.filterwarnings('default')
    return B,L,H

def LLHtoXYZ(lat,lon,h):
    # semi-major and minor axes
    a = 6378137.0;
    f = 1.0/298.2572235630;
    b = (1-f)*a;
    
    N = (a**2)/np.sqrt(a**2*np.cos(lat)**2 + b**2*np.sin(lat)**2);
    
    x = (N+h)*np.cos(lat)*np.cos(lon);
    y = (N+h)*np.cos(lat)*np.sin(lon);
    z = ( (b**2)*N/(a**2) + h )*np.sin(lat);
    
    return x,y,z

