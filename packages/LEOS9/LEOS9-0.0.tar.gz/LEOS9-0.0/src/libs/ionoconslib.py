#!/usr/bin/env python
"""
Module name:		
	ionoconslib.py
Description:	
	collection of used constants	
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

#used for Earth's geographic to geomagnetic latitude conversion
phi_GNP		= np.deg2rad(79.74)                                 #latitude of geomagnetic North Pole used
lambda_GNP	= np.deg2rad(-71.78)                                #longitude of geomagnetic North Pole use		
		
# Constants defined by the World Geodetic System 1984 (WGS84)
smaj = 6378.137                                                     #semimajor axis in km
smin = 6356.7523142                                                  #semi minor axis in km
esq = 6.69437999014 * 0.001                                       
e1sq = 6.73949674228 * 0.001 
flat = 1 / 298.257223563                                             #flattening
REm = 6371211.266 #Earth's mean radius in meter
Lpp = 5 #position of the plasmapause measured in units of Earth radius
N_ms = 1.e-5 #in 10^1^2 el/m^3, plasmapause density
hI = 350000 #peak density height assumption for NPSM model below which NPSM contribution is set to zero 
c = 299792458;
eps0 = 1 / (4e-7 * np.pi * c**2);
e = 1.60217646e-19;
me = 9.10938188e-31;
K = e**2 / (8 * np.pi**2 * eps0 * me);
f1 = 154 * 10.23e6;
f2 = 120 * 10.23e6;
