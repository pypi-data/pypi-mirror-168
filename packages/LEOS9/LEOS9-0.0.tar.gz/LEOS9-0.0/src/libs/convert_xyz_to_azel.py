import sys
import numpy as np

from convert_xyz_to_llh import convert_xyz_to_llh_func

smaj = 6378.137                                                     #semimajor axis in km
smin = 6356.7523142                                                  #semi minor axis in km
esq = 6.69437999014 * 0.001                                       
e1sq = 6.73949674228 * 0.001 
flat = 1 / 298.257223563                                             #flattening
REm = 6371211.266 #Earth's mean radius in meter

def convert_xyz_to_azel_func(sx,sy,sz,x,y,z):
    lat,lon,h=convert_xyz_to_llh_func(sx,sy,sz);
    
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
