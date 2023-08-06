import numpy as np

smaj = 6378.137                                                     #semimajor axis in km
smin = 6356.7523142                                                  #semi minor axis in km
esq = 6.69437999014 * 0.001                                       
e1sq = 6.73949674228 * 0.001 
flat = 1 / 298.257223563                                             #flattening
REm = 6371211.266 #Earth's mean radius in meter

def convert_xyz_to_llh_func(x, y, z):
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
    Esq = smaj **2 - smin **2
    F = 54 * smin **2 * z **2
    G = r **2 + (1 - esq) * z **2 - esq * Esq
    C = (esq **2 * F * r **2) / (np.power(G, 3))
    S = np.sqrt(1 + C + np.sqrt(C **2 + 2 * C))
    P = F / (3 * np.power((S + 1 / S + 1), 2) * G **2)
    Q = np.sqrt(1 + 2 * esq **2 * P)
    r_0 =  (-(P * esq * r) / (1 + Q) + np.sqrt(0.5 * smaj **2 *(1 + 1.0 / Q) -  P * (1 - esq) * z **2 / (Q * (1 + Q)) - 0.5 * P * r **2))
    U = np.sqrt(np.power((r - esq * r_0), 2) + z **2)
    V = np.sqrt(np.power((r - esq * r_0), 2) + (1 - esq) * z **2)
    Z_0 = smin **2 * z / (smaj * V)
    h = U * (1 - smin **2 / (smaj * V))
    lat = np.arctan((z + e1sq * Z_0) / r)
    lon = np.arctan2(y, x)
    return lat, lon, h*1000.

