#!/usr/bin/env python

"""
Module name:        
	nedm2020funclib.py
Description:    
	Neustrelitz Electron Density Model (NEDM) after merging with Neustrelitz Plasmasphere Model (NPSM). The NPSM is developed
	combining different 2D plasmaspheric key parameter models such as basic density models (Np0) and
	scale height models (Hp) etc.
Version:    v1
Author:     Mainul Hoque
Created:    11.12.2020
Copyright:  (c) Mainul Hoque 2020
Mail:       Mainul.Hoque@dlr.de
Licence:    DLR
"""
import numpy as np
import numpy.matlib as npmatlib 
#import datetime
#import sys
import libs.ionofunclib as myfunc
import libs.ionoconslib as mycons
import pylab as pl


def ionpar(lat_deg, lon_deg, UT_hrs, doy):
	"""
	usage: used for initialization
	syntax:
	(LT, latm_rad, cos_solzenith, szfact, cosDVmsz, cosDVsz, sinDVsz, cosSDVsz, sinSDVsz, cosTDVsz, sinTDVsz, cosAV, sinAV,
	cosSAV, sinSAV) = ionpar(lat_deg, lon_deg, UT_hrs, doy)

	Description:
		inputs:
		lat_deg: geographic latitude Vector in degrees
		lon_deg: geographic longitude Vector in degrees
		UT_hrs: universal time (UT) Vector in hours
		doy: day of year Vector (or scaler)
		outputs:
		LT = Local Time Vector in hours
		latm_rad = geomagnetic latitude Vector in radians
		cos_solzenith = cosine of solar zenith angle Vector
		szfact = solar zenith factor Vector
		cosDVmsz = cosine of modified diurnal variation multiply with szfact Vector
		cosDVsz = cosine of diurnal variation multiply with szfact Vector
		sinDVsz = sine of diurnal variation multiply with szfact Vector
		cosSDVsz = cosine of semi-diurnal variation multiply with szfact Vector
		sinSDVsz = sine of semi-diurnal variation multiply with szfact Vector
		cosTDVsz = cosine of ter-diurnal variation multiply with szfact Vector
		sinTDVsz = sine of ter-diurnal variation multiply with szfact Vector
	"""
	# lat_rad = np.deg2rad(lat_deg)
	LT = myfunc.UT2LT(UT_hrs, lon_deg)
	latm_rad = myfunc.geoLat2magLat(np.deg2rad(lat_deg), lon_deg)
	# latm_deg = latm_rad * 180./np.pi

	cos_solzenith, szfact = myfunc.sunZenith(doy, np.deg2rad(lat_deg))

	cosDVmsz = np.cos(2. * np.pi * (LT - 14.) / 24.) * cos_solzenith
	cosDVsz = np.cos(2. * np.pi * LT / 24.) * cos_solzenith
	sinDVsz = np.sin(2. * np.pi * LT / 24.) * cos_solzenith
	cosSDVsz = np.cos(2. * np.pi * LT / 12.) * cos_solzenith
	sinSDVsz = np.sin(2. * np.pi * LT / 12.) * cos_solzenith
	cosTDVsz = np.cos(2. * np.pi * LT / 8.) * cos_solzenith
	sinTDVsz = np.sin(2. * np.pi * LT / 8.) * cos_solzenith
	cosAV = np.cos(2. * np.pi * doy / 365.25)
	sinAV = np.sin(2. * np.pi * doy / 365.25)
	cosSAV = np.cos(4. * np.pi * doy / 365.25)
	sinSAV = np.sin(4. * np.pi * doy / 365.25)

	return (
	LT, latm_rad, cos_solzenith, szfact, cosDVmsz, cosDVsz, sinDVsz, cosSDVsz, sinSDVsz, cosTDVsz, sinTDVsz, cosAV, sinAV,
	cosSAV, sinSAV)


def NTCM(doy, F10p7, latm_rad, szfact, cosDVmsz, cosSDVsz, sinSDVsz, cosTDVsz, sinTDVsz ):
	"""
	Syntax:
		vtec = NTCM( doy, F10p7, latm_rad, szfact, cosDVmsz, cosSDVsz, sinSDVsz, cosTDVsz, sinTDVsz )
		vtec in TECU
	Description:
		TEC: Total Electron Content in TECU (Vertical direction up to GPS height)
		for more see description of model(ionpar)

		NeustrelitZ Total Electron Content Model (NTCM) approach
		Local Time variation:
		   Diurnal Variation: DVm = 2*pi*(LT-14)/24
		   Semi-Diurnal Variation: SDV = 2*pi*LT/12
		   Tar-Diurnal Variation: TDV = 2*pi*LT/8
		   F1 = cos(chi)***+((c1cos(DVm)+c2sin(DV)+c3cos(SDV)+c4sin(SDV)+c5cos(TDV)+c6sin(TDV))cos(chi)**
		   cos(chi)*** 	= cos(phi - delta) + 0.4 # square root is omitted, it was a printing mistake in Jakowski et al .[2011]
		   cos(chi)** = cos(phi - delta) - 2phi/pi*sin(delta); phi = geographic latitude radian, delta = sun declination radian
		Annual Semiannual variation
		   Annual Variation: AV = 2*pi(doy-doy_DAV)/365.25; doy_DAV = 18
		   Semi-Annual Variation: SAV = 4*pi(doy-doy_DSAV)/365.25; doy_DSAV = 6
		   F2 =1+c7cos(AV)+c8cos(SAV)
		Dependence from geomagnetic field
		   F3 =1+c9cos(phi_m); phi_m = geomagnetic latitude radian
		Dependence from Crest region
		   Equatorial Crest: EC1 = (phi_m-phi_c1)^2/2sigma_1^2; phi_c1 = 16N
		   Equatorial Crest: EC2 = (phi_m-phi_c2)^2/2sigma_2^2; phi_c2 = -10N
		   F4 = 1+c10exp(EC1)+c11exp(EC2)
		Dependence from solar activity
		   F5 =c12+c13*F10.7; F10.7 = solar radio flux in flux units
		   TECvt = F1*F2*F3*F4*F5 in TECU
		REFERENCE: Jakowski, N. and Hoque, M. M. and Mayer, C. (2011)
				   A new global TEC model for estimating transionospheric radio wave propagation errors.
				   Journal of Geodesy, 85 (12), pp. 965-974. Springer. DOI: 10.1007/s00190-011-0455-1. ISSN 0949-7714.
	"""

	K = (0.8966, 0.1698, -0.0217, 0.0593, 0.0074, 0.1391, -0.1759, -0.3455, 1.1168, 1.1573, -4.3356, 0.1778)

	vtec = ((szfact + K[0] * cosDVmsz + K[1] * cosSDVsz + K[2] * sinSDVsz + K[3] * cosTDVsz +
			 K[4] * sinTDVsz) * (1 + K[5] * np.cos(2 * np.pi * (doy - 18.) / 365.25) + K[6] * np.cos(
				4 * np.pi * (doy - 6.) / 365.25)) * (1 + K[7] * np.cos(latm_rad)) *
			(1 + K[8] * np.exp(-(np.rad2deg(latm_rad) - 16.) ** 2 / 288.) + K[9] * np.exp(
					-(np.rad2deg(latm_rad) + 10.) ** 2 / 338.)) * (K[10] + K[11] * F10p7))

	return vtec

def NPDM(doy, F10p7, LT, latm_rad, lat_rad, szfact, cosDVmsz, cosSDVsz, sinSDVsz, cosTDVsz, sinTDVsz ):

		"""
		Syntax:
			NmF2 = NPDM( doy, F10p7, LT, latm_rad, lat_rad, szfact, cosDVmsz, cosSDVsz, sinSDVsz, cosTDVsz, sinTDVsz )
			NmF2 in 10^12 el/m^3
		Description:
			NmF2: Maximum ionization of F2 layer in 1.e+12 el/m^3
			for more see description of model(ionpar)

		Neustrelitz Peak Density Model (NPDM) approach
		Local Time variation:
			Diurnal Variation: DVm = 2*pi*(LT-14)/24
			Semi-Diurnal Variation: SDV = 2*pi*LT/12
			Tar-Diurnal Variation: TDV = 2*pi*LT/8
			F1 = cos(chi***)+((c1cos(DVm)+c2cos(SDV)+c3sin(SDV)+c4cos(TDV)+c5sin(TDV))cos(chi**)+c13BO
			cos(chi)*** 	= cos(phi - delta) + 0.4
			cos(chi)** = cos(phi - delta) - 2phi/pi*sin(delta); phi = geographic latitude radian, delta = sun declination radian
			Midlatitude Summer daytime Bite Out effect: BO
				sigma_BO = 3;
				doyBO = 181;
				LTBO = 13. + 1.5*cos(2*pi*(doy - doyBO)/365.25).*SIGN;
				EBO = exp(-(LT-LTBO).^2/2/sigma_BO^2);
				sigma_BO2 = 14;
				EBO2 = exp(-(abs(lat_deg) - 45).^2/2/sigma_BO2^2).*SIGN;
				BO = EBO2.*cos(2*pi*(doy-doyBO)/365.25).*EBO;
		Annual Semiannual variation
			Annual Variation: AV = 2*pi(doy - doy_DAV)/365.25; doy_DAV = 18
			Semi-Annual Variation: SAV = 4*pi(doy - doy_DSAV)/365.25; doy_DSAV = 6
			F2 =1+c7cos(AV)+c8cos(SAV)
		Dependence from geomagnetic field
			F3 =1+c9cos(phi_m); phi_m = geomagnetic latitude
		Dependence from Crest region
			phi_c1 = 16; %degrees
			phi_c2 = -15; %degrees
			sigma_LT = 12;
			EC_LT = -(LT - 14).^2/2/sigma_LT^2;
			sigma_c1 = 20 - 10*exp(EC_LT);
			sigma_c2 =  sigma_c1;
			Equatorial Crest: EC1 = (phi_m-phi_c1)^2/2sigma_1^2
			Equatorial Crest: EC2 = (phi_m-phi_c2)^2/2sigma_2^2
			F4 = 1+c10exp(EC1)+c11exp(EC2)
		Dependence from solar activity
			F5 =c12+c13*F10.7
		NmF2 = F1*F2*F3*F4*F5 in 1.e+12 el/m^3
		Reference:
			Hoque, M. M. and Jakowski, N.: A new global empirical NmF2
				model for operational use in radio systems, Radio Sci., 46,
				RS6015, doi:10.1029/2011RS004807, 2011b.
		"""
		K = (
		1.00889, 0.12569, -0.00882, 0.10268, 0.04894, 0.13443, -0.16045, 0.19216, 0.62074, 0.58005, 0.91756, -1.18833,
		-0.83712)

		if np.size(lat_rad) == 1:
			lat_rad = lat_rad * np.ones(1)

		# SIGN = self.lat_rad / np.fabs(self.lat_rad)
		SIGN = np.ones(np.size(lat_rad))
		indices = np.nonzero(np.abs(lat_rad) > 0)
		#print("indices", indices, lat_rad)
		SIGN[indices] = lat_rad[indices] / np.fabs(lat_rad[indices])

		# print("SIGN", self.lat_rad)

		SIGN = np.select([np.isnan(SIGN), ~np.isnan(SIGN)], [0, SIGN])

		BO = ((np.exp(-(np.fabs(np.rad2deg(lat_rad)) - 45.) ** 2 / 392.) * SIGN) *
			  np.cos(2 * np.pi * (doy - 181.) / 365.25) * np.exp(
					-(LT - (13. + 1.5 * np.cos(2 * np.pi * (doy - 181.) / 365.25) * SIGN)) ** 2 / 18.))

		sigma_c1 = 20. - 10. * np.exp(-(LT - 14.) ** 2 / 288.)

		NmF2 = ((szfact + K[0] * cosDVmsz + K[1] * cosSDVsz + K[2] * sinSDVsz + K[
			3] * cosTDVsz + K[4] * sinTDVsz + K[12] * BO) *
				(1 + K[5] * np.cos(2 * np.pi * (doy - 18.) / 365.25) + K[6] * np.cos(
					4 * np.pi * (doy - 6.) / 365.25)) * (1 + K[7] * np.cos(latm_rad)) *
				(1 + K[8] * np.exp(-(np.rad2deg(latm_rad) - 16.) ** 2 / 2. / sigma_c1 ** 2) + K[9] * np.exp(
					-(np.rad2deg(latm_rad) + 15.) ** 2 / 2. / sigma_c1 ** 2)) *
				(K[10] + K[11] * np.exp(-F10p7 / 144.)))

		return NmF2


def NPHM(doy, F10p7, LT, latm_rad, szfact, cosDVsz, sinDVsz, cosSDVsz, sinSDVsz, cosTDVsz, sinTDVsz):
	"""
	Syntax:
		hmF2 = NPDM( doy, F10p7, LT, latm_rad, szfact, cosDVsz, sinDVsz, cosSDVsz, sinSDVsz, cosTDVsz, sinTDVsz )
		hmF2 = in km
	Description:
		hmF2: Maximum ionization height of F2 layer in km
		for more see description of model(ionpar)

	Neustrelitz Peak Height Model (NPHM) approach
	Local Time variation:
		Diurnal Variation: DV = 2*pi*LT/24
		Semi-Diurnal Variation: SDV = 2*pi*LT/12
		Tar-Diurnal Variation: TDV = 2*pi*LT/8
		F1 = 1 + c1*cos(chi***)+(c2*cos(DV)+c3*sin(DV)+c4*cos(SDV)+c5*sin(SDV)+c6*cos(TDV)+c7*sin(TDV))cos(chi**)
		cos(chi)*** 	= cos(phi - delta) + 0.4
		cos(chi)** = cos(phi - delta) - 2phi/pi*sin(delta); phi = geographic latitude radian, delta = sun declination radian
	Annual Semiannual variation
		Annual Variation: AV = 2*pi(doy - doy_DAV)/365.25; doy_DAV = 181
		Semi-Annual Variation: SAV = 4*pi(doy - doy_DSAV)/365.25; doy_DSAV = 49
		F2 = 1+c8*cos_AV+c9*cos_SAV
	Dependence from geomagnetic field
		sigma_c2 = 40; %degrees
		exp_EC_phi = exp(-latm_deg.^2/2/sigma_c2^2);
		sigma_c1 = 20; %degrees
		EC_phi = -latm_deg.^2/2/sigma_c1^2;
		sigma_LT = 4;
		EC_LT = -(LT - 14).^2/2/sigma_LT^2;
		exp_phi_LT = exp(EC_phi).*exp(EC_LT);
		F3 = 1+c10*exp_EC_phi+c11*exp_phi_LT
   Dependence from solar activity
		delta_F10p7 = 10.8;
		exp_F10p7 = exp(-F10p7/delta_F10p7^2);
		F4 = c12+c13*exp_F10p7
   hmF2 = F1 * F2 *F3 *F4
	Reference:
		Hoque, M. M. and Jakowski, N.: A new global model for the ionospheric F2 peak height for radio
			wave propagation, Ann. Geophys., 30, 797809, 2012, www.ann-geophys.net/30/797/2012/
			doi 10.5194/angeo-30-797-2012
	"""

	K = (
	0.09246, 0.19113, 0.02297, 0.05666, -0.01687, -0.01590, 0.01194, -0.01781, -0.00618, -0.14070, 0.46728, 348.66432,
	-184.15337)

	hmF2 = ((1 + K[0] * szfact + K[1] * cosDVsz + K[2] * sinDVsz + K[3] * cosSDVsz + K[
		4] * sinSDVsz + K[5] * cosTDVsz + K[6] * sinTDVsz) *
			(1 + K[7] * np.cos(2 * np.pi * (doy - 181.) / 365.25) + K[8] * np.cos(
				4 * np.pi * (doy - 49.) / 365.25)) *
			(1 + K[9] * np.exp(-np.rad2deg(latm_rad) ** 2 / 3200.) + K[10] * np.exp(
				-np.rad2deg(latm_rad) ** 2 / 800.) * np.exp(-(LT - 14.) ** 2 / 32.)) *
			(K[11] + K[12] * np.exp(-F10p7 / 116.64)))

	return hmF2


def Np0_tp(doy, F10p7, LT, cos_solzenith, szfact):
	"""
	   Syntax:
		Np0_L = Np0_tp( doy, F10p7, LT, cos_solzenith, szfact )
		Np0_L = basic ionization for plasmaspheric top layer (L shell part) in 10^12 el/m^3
	Description:
	%----------------------------------------------------------------------
		%INPUT
		%   F10p7: Solar radio flux input
		%   doy: day of year
		%   LT: local time in hours
		%   lat_deg: geographic latitude in degrees
		%   ModCo: Model Coefficients
		%OUPUT
		%   Np0_tp: basic ionization of plasmaspheric layer in 1.e+12 el/m^3
		%Version:    v1
		%Author:    Mainul Hoque
		%Created:    20.07.2017
		%Copyright:    (c) Mainul Hoque 2017
		%Mail:        Mainul.Hoque@dlr.de
		%Licence:    DLR
		%-----------------------------------------------------------------------
		%===============Np0_tp Model basic approach=========================
		%Local Time variation:
		%   Diurnal Variation: DV = 2*pi*LT/24
		%   Semi-diurnal Variation: SDV = 2*pi*LT/12
		%   F1 = cos(chi***)+( (c1*cos(DV) + c2*sin(DV) + c3*cos(SDV) + c4*sin(SDV) )*cos(chi**)
		%   Annual-semiannual variation
		%   F2 = 1 + c5*cos(AV) + c6*sin(AV) + c7*cos(SAV) + c8*sin(SAV)
		%Dependence from solar activity
		%   F3 =c9 + c10*F10.7
		%   Np0_tp = F1*F2*F3 in 1.e+12 el/m^3
		%------------------------------------------------------------------------

	"""
	K = (-0.065993, -0.172225, 0.176225, -0.178877, 0.062047, 0.009406, -0.035450, -0.010803, 0.012275, 0.000049)
	# Np0_L =  ((szfact + K[0] * cosDVsz + K[1] * sinDVsz + K[2] * cosSDVsz + K[3] * sinSDVsz) *
	#         (1 + K[4] * cosAV + K[5] * sinAV + K[6] * cosSAV + K[7] * sinSAV) *
	#         (K[8] + K[9] * F10p7))

	Np0_L =  ((szfact + K[0] * np.cos(2. * np.pi * LT / 24.) * cos_solzenith + K[1] * np.sin(2. * np.pi * LT / 24.) * cos_solzenith +
			   K[2] * np.cos(2. * np.pi * LT / 12.) * cos_solzenith + K[3] * np.sin(2. * np.pi * LT / 12.) * cos_solzenith) *
			(1 + K[4] * np.cos(2. * np.pi * doy / 365.25) + K[5] * np.sin(2. * np.pi * doy / 365.25) + K[6] *
			 np.cos(4. * np.pi * doy / 365.25) + K[7] * np.sin(4. * np.pi * doy / 365.25)) *
			(K[8] + K[9] * F10p7))



	return Np0_L



def Hp_tp(doy, F10p7, LT, cos_solzenith ):
		"""
		   Syntax:
		   Hp_L = Hp_tp( doy, F10p7, LT, cos_solzenith )
		   Hp_L = plasmaspheric scale height topside in km
	   Description:
		   %----------------------------------------------------------------------
		   %INPUT
		   %   F10p7: solar radio flux input
		   %   doy: day of year
		   %   LT: local time in hours
		   %   lat_deg: geographi latitude in degrees
		   %   ModCo: Model Coefficients
		   %OUPUT
		   %   Hp_tp: topside plasmaspheric scale height in km
		   %Version:    v1
		   %Author:    Mainul Hoque
		   %Created:    20.07.2017
		   %Copyright:    (c) Mainul Hoque 2017
		   %Mail:        Mainul.Hoque@dlr.de
		   %Licence:    DLR
		   %-----------------------------------------------------------------------
		   %===============Hp_tp model basic approach=========================
		   %Local Time variation:
		   %   Diurnal Variation: DV = 2*pi*LT/24
		   %   Semi-diurnal Variation: DV = 2*pi*LT/24
		   %   F1 = 1+( (c1*cos(DV) + c2*sin(DV) + c3*cos(SDV) + c4*sin(SDV) )cos(chi**)
		   %Annual-semiannual variation
		   %   F2 = 1 + c5*cos(AV) + c6*sin(AV) + c7*cos(SAV) + c8*sin(SAV)
		   %Dependence from solar activity
		   %   F3  = c9 + c10*F10.7
		   %   Hp_tp = F1*F2*F3 in km
		   %------------------------------------------------------------------------
	   """

		K = (0.012120, 0.025590, -0.027455, 0.033566, -0.015126, -0.001065, 0.013310, -0.002841, 4564.920529, -3.154672)

		# Hp_L =  (1 + K[0] * cosDVsz + K[1] * sinDVsz + K[2] * cosSDVsz + K[3] * sinSDVsz) * (
		#             1 + K[4] * cosAV + K[5] * sinAV + K[6] * cosSAV + K[7] * sinSAV) * (
		#                    K[8] + K[9] * F10p7)

		Hp_L =  (1 + K[0] * np.cos(2. * np.pi * LT / 24.) * cos_solzenith + K[1] * np.sin(2. * np.pi * LT / 24.) * cos_solzenith +
				 K[2] * np.cos(2. * np.pi * LT / 12.) * cos_solzenith + K[3] * np.sin(2. * np.pi * LT / 12.) * cos_solzenith) * (
					1 + K[4] * np.cos(2. * np.pi * doy / 365.25) + K[5] * np.sin(2. * np.pi * doy / 365.25) +
					K[6] * np.cos(4. * np.pi * doy / 365.25) + K[7] * np.sin(4. * np.pi * doy / 365.25)) * (
						   K[8] + K[9] * F10p7)
		return Hp_L



def Np0_lp(doy, F10p7, LT, latm_rad, cos_solzenith, szfact ):
	"""
	   Syntax:
		Np0_h = Np0_lp( doy, F10p7, LT, latm_rad, cos_solzenith, szfact )
		Np0_h = basic ionization for plasmaspheric lower layer (h dependendent part) in 10^12 el/m^3
	   %----------------------------------------------------------------------
	   %INPUT
	   %   F10p7: Solar radio flux input
	   %   doy: day of year
	   %   LT: local time in hours
	   %   lat_deg: geographic latitude in degrees
	   %   latm_deg: geomagnetic latitude in degrees
	   %   ModCo: Model Coefficients
	   %OUPUT
	   %   Np0_lp: basic ionization of plasmaspheric lower layer in 1.e+12 el/m^3
	   %Version:    v1
	   %Author:    Mainul Hoque
	   %Created:    20.07.2017
	   %Copyright:    (c) Mainul Hoque 2017
	   %Mail:        Mainul.Hoque@dlr.de
	   %Licence:    DLR
	   %-----------------------------------------------------------------------
	   %===============Np0_lp Model basic approach=========================
	   %Local Time variation:
	   %   Diurnal Variation Modified: DVM = 2*pi*(LT - LT_DV)/24
	   %   Semi-diurnal Variation Modified: SDVM = 2*pi*(LT - LT_SDV)/12
	   %   Ter-diurnal Variation Modified: TDVM = 2*pi*(LT - LT_TDV)/8
	   %   F1 = cos(chi***)+( (c1*cos(DVM) + c2*cos(SDVM) + c3*cos(TDVM) )*cos(chi**)
	   %   Annual variation Modified: AVM = 2*pi*(doy -doy_AN)/365.25
	   %   Semiannual variation Modified: SAVM = 4*pi*(doy -doy_SAN)/365.25
	   %   F2 = 1 + c4*cos(AVM) + c5*cos(SAVM)
	   %Dependence from geomagnetic latitude
	   %   F3 = 1 + c6*cos(phim) + c7*(cos(4*phim))^2
	   %Dependence from crest region
	   %   phim = latm_deg
	   %   F4 = 1 + c8*exp(-(phim - phim_pcm)^2/2/sigma_pcn^2) + c9*exp(-(phim - phim_pcs)^2/2/sigma_pcs^2)
	   %Dependence from solar activity
	   %   F5 = c10 + c11*F10.7
	   %   Np0_tp = F1*F2*F3*F4*F5 in 1.e+12 el/m^3
	   %------------------------------------------------------------------------
	"""

	K = (
	-0.606376, 0.133197, 0.139693, 0.105906, -0.039258, 28.609481, -0.625364, 0.070696, 0.026846, 0.000558, 0.000005)

	LT_DV = 0.47
	LT_SDV = 9.16
	LT_TDV = 0.66
	doy_AV = -1.4
	doy_SAV = -11.1
	latm_deg = np.rad2deg(latm_rad)

	phi_pcn = 15 + 2.5 * (1 + np.cos(2 * np.pi * (doy - 1) / 365.25))
	sigma_pcn = 8 + 4.0 * (1 - np.cos(2 * np.pi * (doy - 1) / 365.25))
	phi_pcs = -15 - 2.5 * (1 - np.cos(2 * np.pi * (doy - 1) / 365.25))
	sigma_pcs = 8 + 4.0 * (1 + np.cos(2 * np.pi * (doy - 1) / 365.25))
	exp_EC1 = np.exp(-(latm_deg - phi_pcn) ** 2 / 2 / sigma_pcn ** 2)
	exp_EC2 = np.exp(-(latm_deg - phi_pcs) ** 2 / 2 / sigma_pcs ** 2)

	# Np0_h =  (szfact + (
	#             K[0] * np.cos(2 * np.pi * (LT - LT_DV) / 24) + K[1] * np.cos(2 * np.pi * (LT - LT_SDV) / 12) +
	#             K[2] * np.cos(2 * np.pi * (LT - LT_TDV) / 8)) * cos_solzenith) * (
	#                    1 + K[3] * np.cos(2 * np.pi * (doy - doy_AV) / 365.25) + K[4] * np.cos(
	#                4 * np.pi * (doy - doy_SAV) / 365.25)) * (
	#                    1 + K[5] * np.cos(latm_rad) + K[6] * np.cos(4 * latm_rad) ** 2) * (
	#                    1 + K[7] * exp_EC1 + K[8] * exp_EC2) * (K[9] + K[10] * F10p7)

	Np0_h = (szfact + (
			K[0] * np.cos(2 * np.pi * (LT - LT_DV) / 24) + K[1] * np.cos(2 * np.pi * (LT - LT_SDV) / 12) +
			K[2] * np.cos(2 * np.pi * (LT - LT_TDV) / 8)) * cos_solzenith) * (
					1 + K[3] * np.cos(2 * np.pi * (doy - doy_AV) / 365.25) + K[4] * np.cos(
				4 * np.pi * (doy - doy_SAV) / 365.25)) * (
					1 + K[5] * np.cos(latm_rad) + K[6] * np.cos(4 * latm_rad) ** 2) * (
					1 + K[7] * exp_EC1 + K[8] * exp_EC2) * (K[9] + K[10] * F10p7)

	return Np0_h




def Hp_lp(doy, F10p7, LT, latm_rad, cos_solzenith ):
		"""
		  Syntax:
			Hp_h = Hp_lp( doy, F10p7, LT, latm_rad, cos_solzenith )
			Hp_h = plasmaspheric scale height lower layer in km
		  Description:
		  %----------------------------------------------------------------------
		  %INPUT
		  %   F10p7: solar radio flux input
		  %   doy: day of year
		  %   LT: local time in hours
		  %   lat_deg: geographi latitude in degrees
		  %   latm_deg: geomagnetic latitude in degrees
		  %   ModCo: Model Coefficients
		  %OUPUT
		  %   Hp_lp: topside plasmaspheric scale height in km
		  %Version:    v1
		  %Author:    Mainul Hoque
		  %Created:    20.07.2017
		  %Copyright:    (c) Mainul Hoque 2017
		  %Mail:        Mainul.Hoque@dlr.de
		  %Licence:    DLR
		  %-----------------------------------------------------------------------
		  %===============Hp_lp model basic approach=========================
		  %Local Time variation:
		  %   Diurnal Variation Modified: DVM = 2*pi*(LT - LT_DV)/24
		  %   Semi-diurnal Variation Modified: SDVM = 2*pi*(LT - LT_SDV)/12
		  %   Ter-diurnal Variation Modified: TDVM = 2*pi*(LT - LT_TDV)/8
		  %   F1 = 1 + ( (c1*cos(DVM) + c2*cos(SDVM) + c3*cos(TDVM) )*cos(chi**)
		  %   Annual variation Modified: AVM = 2*pi*(doy -doy_AN)/365.25
		  %   Semiannual variation Modified: SAVM = 4*pi*(doy -doy_SAN)/365.25
		  %   F2 = 1 + c4*cos(AVM) + c5*cos(SAVM)
		  %Dependence from geomagnetic latitude
		  %   phim_mod = 0.7*latm_deg*pi/180
		  %   F3 = 1 + c6*cos(phim_mod) + c7*(cos(4*phim_mod))^2
		  %Dependence from solar activity
		  %   F4  = c8 + c9*F10.7
		  %   Hp_lp = F1*F2*F3*F4 in km
		  %------------------------------------------------------------------------
		"""

		K = (
		0.072240, 0.110115, 0.031275, 0.044048, 0.047681, 1.080420, 0.183067, 486.968530, -0.359689, 0.374722, 0.131115,
		0.435041)
		LT_DV = 13.7
		LT_SDV = 14.5
		LT_TDV = 1.7
		doy_AV = 182
		doy_SAV = 180

		return (1 + (K[0] * np.cos(2 * np.pi * (LT - LT_DV) / 24) + K[1] * np.cos(
			2 * np.pi * (LT - LT_SDV) / 12) + K[2] * np.cos(
			2 * np.pi * (LT - LT_TDV) / 8)) * cos_solzenith) * (
						   1 + K[3] * np.cos(2 * np.pi * (doy - doy_AV) / 365.25) + K[4] * np.cos(
					   4 * np.pi * (doy - doy_SAV) / 365.25)) * (
						   1 + K[5] * np.cos(latm_rad * 0.7) + K[6] * np.cos(4 * latm_rad * 0.7) ** 2) * (
						   K[7] + K[8] * F10p7)



def getNe_tp(Np0_tp, Hp_tp, latm_rad, altm, hmRefm):
	"""
	 Syntax:
		 Ne_tp, altkm = getNe_tp( Np0_tp, Hp_tp, latm_rad, altm, hmRefm)
		 [Ne_tp, altkm] = electron density for L shell part versus altitude in km
	 Description:
		 [Ne_tp, altkm] = npsmP2PObj.getNe_tp()
		 Ne = electron density Vector in 10**12 el/m**3
		 altkm = corresponding altitude Vector in km

		%----------------------------------------------------------------------
		%INPUT
		%   Np0_tp: plasmaspheric basic density for top layer in 1.e+12 el/m^3
		%   Hp_tp: plasmaspheric scale height for top layer in km
		%   h: height from the Earth's surface in km
		%   latm_rad: geomagnetic latitude in radians
		%OUPUT
		%   Ne_tp: electron density for plasmaspheric top layer in 1.e+12 el/m^3
		%   h: height in km
		%Version:    v1
		%Author:    Mainul Hoque
		%Created:    20.07.2017
		%Copyright:    (c) Mainul Hoque 2017
		%Mail:        Mainul.Hoque@dlr.de
		%Licence:    DLR
		%-----------------------------------------------------------------------
		%===============Ne_tp profile basic approach=========================
		%------------------------------------------------------------------------

	"""

	h = altm / 1000

	if np.size(latm_rad) == 1:
		latm_rad = latm_rad * np.ones(np.shape(h))

	# if   Np0_tp.shape[1] != h.shape[1] :
	if Np0_tp.size != h.size:
		Np0_tp = Np0_tp * np.ones(np.shape(h))
		Hp_tp = Hp_tp * np.ones(np.shape(h))

	REkm = mycons.REm / 1000
	Lpp = mycons.Lpp
	N_ms = mycons.N_ms  # in 10^1^2 el/m^3;
	# hmF2 = mycons.hI/1000 #km
	hmF2 = hmRefm / 1000  # km
	# hmF2 = self.NPHM() #km

	Lval = (h + REkm) / (REkm * np.cos(latm_rad) ** 2)

	indices = np.nonzero(h >= hmF2)
	Rpp = Lpp * REkm * np.cos(latm_rad[indices]) ** 2
	F_pp = np.arctan((Rpp - REkm - h[indices]) / 500) / np.pi + 0.5
	Ne_tp = np.zeros(np.shape(h))
	Ne_tp[indices] = Np0_tp[indices] * F_pp * (np.exp(-REkm * (Lval[indices] - 1.) / Hp_tp[indices])) + N_ms

	return Ne_tp, h


def getNe_lp(Np0_lp, Hp_lp, altm, hmRefm):
	"""
		 Syntax:
			 npsmP2PObj = getNe_lp( Np0_lp, Hp_lp, altm, hmRefm)
			 [Ne_lp, altkm] = electron density for lower part versus altitude in km
		 Description:
			 [Ne_lp, altkm] = npsmP2P.getNe_lp()
			 Ne_lp = electron density Vector in 10**12 el/m**3
			 altkm = corresponding altitude Vector in km
			%----------------------------------------------------------------------
			%INPUT
			%   Np0_lp: plasmaspheric basic density for lower layer in 1.e+12 el/m^3
			%   Hp_lp: plasmaspheric scale height for lower layer in km
			%   h: height from the Earth's surface in km
			%OUPUT
			%   Ne_tl: electron density for plasmaspheric top layer in 1.e+12 el/m^3
			%   h: height in km
			%Version:    v1
			%Author:    Mainul Hoque
			%Created:    20.07.2017
			%Copyright:    (c) Mainul Hoque 2017
			%Mail:        Mainul.Hoque@dlr.de
			%Licence:    DLR
			%-----------------------------------------------------------------------
			%===============Ne_lp profile basic approach=========================
			%------------------------------------------------------------------------


	"""

	h = altm / 1000

	# print "h [km]:", 100
	# g
	# if   Np0_lp.shape[1] != h.shape[1] :
	if Np0_lp.size != h.size:
		Np0_lp = Np0_lp * np.ones(np.shape(h))
		Hp_lp = Hp_lp * np.ones(np.shape(h))

	# hmF2 = mycons.hI/1000 #km
	hmF2 = hmRefm / 1000  # km
	# hmF2 = self.NPHM() #km

	#print("hmF2", hmF2)
	indices = np.nonzero(h >= hmF2)
	Ne_lp = np.zeros(np.shape(h))
	# Ne_lp[indices] = Np0_lp[indices] * ( np.exp( -h[indices]/Hp_lp[indices] ) )
	# chnage 23.12.2019 see matlab NPSM_matlab_v2
	# z = (h[indices] - 350)/350
	#z = (h[indices] - hmF2) / 350
	z = (h[indices] - hmF2[indices]) / 350  #30.11.2020

	Ne_lp[indices] = Np0_lp[indices] * (np.exp(-h[indices] / Hp_lp[indices])) * (1 - np.exp(-z))

	return Ne_lp, h



def getNe_lp_vpec(Np0_lp, Hp_lp, altm, hmRefm):
	"""
		 Syntax:
			 [Ne_lp, altkm] = getNe_lp_vpec( Np0_lp, Hp_lp, altm, hmRefm)
			 [Ne_lp, altkm] = electron density for lower part versus altitude in km
		 Description:
			 [Ne_lp, altkm] = npsmP2P.getNe_lp()
			 Ne_lp = electron density Vector in 10**12 el/m**3
			 altkm = corresponding altitude Vector in km
			%----------------------------------------------------------------------
			%INPUT
			%   Np0_lp: plasmaspheric basic density for lower layer in 1.e+12 el/m^3
			%   Hp_lp: plasmaspheric scale height for lower layer in km
			%   h: height from the Earth's surface in km
			%OUPUT
			%   Ne_tl: electron density for plasmaspheric top layer in 1.e+12 el/m^3
			%   h: height in km
			%Version:    v1
			%Author:    Mainul Hoque
			%Created:    20.07.2017
			%Copyright:    (c) Mainul Hoque 2017
			%Mail:        Mainul.Hoque@dlr.de
			%Licence:    DLR
			%-----------------------------------------------------------------------
			%===============Ne_lp profile basic approach=========================
			%------------------------------------------------------------------------


	"""

	h = altm / 1000

	# print "h [km]:", 100
	# g
	# if   Np0_lp.shape[1] != h.shape[1] :
	if Np0_lp.size != h.size:
		Np0_lp = Np0_lp * np.ones(np.shape(h))
		Hp_lp = Hp_lp * np.ones(np.shape(h))

	# hmF2 = mycons.hI/1000 #km
	hmF2 = hmRefm / 1000  # km
	# hmF2 = self.NPHM() #km

	#print("hmF2", hmF2)
	indices = np.nonzero(h >= hmF2)
	Ne_lp = np.zeros(np.shape(h))
	# Ne_lp[indices] = Np0_lp[indices] * ( np.exp( -h[indices]/Hp_lp[indices] ) )
	# chnage 23.12.2019 see matlab NPSM_matlab_v2
	# z = (h[indices] - 350)/350
	z = (h[indices] - hmF2) / 350
	#z = (h[indices] - hmF2[indices]) / 350  #30.11.2020

	Ne_lp[indices] = Np0_lp[indices] * (np.exp(-h[indices] / Hp_lp[indices])) * (1 - np.exp(-z))

	return Ne_lp, h


def getNe_Elayer(doy, F10p7, LT, lat_deg, lon_deg, altm):
	"""
	Syntax:
	N_E, h = getNe_Elayer(doy, F10p7, LT, lat_deg, lon_deg, altm):
	N_E, h = E-layer electron density (10^12 el/m^3) versus altitude in km
	Description:
		N_E: E-layer electron density
	Reference:
		Ching, B. K. and Y. T. Chiu (1973) A phenomenological model of global ionospheric electron density in the E-,F1 and F2 regions, JATP, 35, 1615-1630
	"""

	delta = myfunc.sunDecl(doy)  # declination of the sun in radians
	cos_solzenith = np.sin(np.deg2rad(lat_deg)) * np.sin(delta) + np.cos(np.deg2rad(lat_deg)) * np.cos(delta) * np.cos(
			(LT - 12) * np.pi / 12)  # cosine of solar zenith angle
	h = altm / 1000
	hmE = 110  # km 	E-layer peak height
	HE = 10  # km		E-Layer scale height

	FD = F10p7 - 67.0
	R = 1.61 * FD - (0.0733 * FD) ** 2 + (0.0240 * FD) ** 3  # monthly smoothed Zurich sunspot number
	R = R / 100

	D_E = np.exp(2 * (np.sin(cos_solzenith) * np.sqrt(np.abs(cos_solzenith)) - 1))

	# print("self.lon_deg", self.lon_rad)
	sei = lon_deg * np.pi / 180 + delta * np.cos(np.deg2rad(lat_deg))  # in radians

	W_E = np.exp(-0.4 * (np.cos(sei) - np.cos(lon_deg * np.pi / 180)))

	Z_E = np.exp(0.5 * (1 - (h - hmE) / HE - np.exp(-(h - hmE) / HE)))

	N_E = 1.36 * Z_E * np.sqrt(1 + 1.15 * R) * D_E * W_E  # in 1.e+5 el/cm^3

	N_E = N_E / 10  # * 1.e+5*1.e+6/1.e+12
	#print("getNe_Elayer", np.size(self.UT_hrs), np.size(self.lon_deg))

	return N_E, h


def getNe_Flayer(TECvt, Nm_corr, hmkm, PECv, altm):
	"""
		Syntax:
			NeF, h = getNe_Flayer( TECvt, Nm_corr, hmkm, PECv, altm)
			NeF, h = F-layer electron density (10^12 el/m^3) versus altitude in km
		Description:
			single layer Chapman function
			Ne = electron density Vector in 10**12 el/m**3
			altkm = corresponding altitude Vector in km
	"""
	# get 2D model parameters

	h = altm / 1000

	TEC_Flayer = TECvt - PECv
	# print("TEC_Flayer", TEC_Flayer)

	#Nm_corr = Nm - Nphm * redfact

	HF = (TEC_Flayer / Nm_corr / 4.13) * 10  # in km
	# print("HF", HF)
	z = (h - hmkm) / HF

	#Chapman layer function
	#NeF = Nm * np.exp(0.5 * (1 - z - np.exp(-z)))  # in e+12 el/m^3
	NeF = Nm_corr * np.exp(0.5 * (1 - z - np.exp(-z)))  # in e+12 el/m^3 30.11.2020

	return NeF, h


def PECv(doy, F10p7, LT, cos_solzenith, szfact, latm_rad, lat_deg, lon_deg, hm ):
	"""
		Syntax:

		Description:
			PEC: vertical Plasmaspheric Content by NPSM


		Reference:
			NPSM, Jakowski and Hoque 2018
	"""


	if len(lat_deg) == 1 and  len(lon_deg) == 1: #added 21.11.2020
		maxlatdegdiff = 0
		maxlondegdiff = 0
	else:
		maxlatdegdiff = np.sum(np.abs(np.diff(lat_deg)))
		maxlondegdiff = np.sum(np.abs(np.diff(lon_deg)))


	if maxlatdegdiff < 1 and maxlondegdiff < 1:
		# altm = myfunc.getGeomHeight(hm[0]) *1000
		altm = np.arange(hm[0]/1000, 20200, 40) * 1000
		vpec, Nphm = npsm_vpec(doy[0]*np.ones(1), F10p7[0]*np.ones(1), LT[0]*np.ones(1), cos_solzenith[0]*np.ones(1), szfact[0]*np.ones(1),
							  latm_rad[0]*np.ones(1), lat_deg[0]*np.ones(1), lon_deg[0]*np.ones(1), altm, hm[0])
		#print("vpec", vpec)
		PEC = vpec * np.ones(np.size(hm))
		Nphm = Nphm * np.ones(np.size(hm))

	else:
		#PEC = np.array([])
		#Nphm = np.array([])
		PEC = np.zeros(np.size(hm))
		Nphm = np.zeros(np.size(hm))

		for i in range(0, len(lat_deg)):
			altm = myfunc.getGeomHeight(hm[i]/1000) * 1000
			#print("altm", np.diff(altm))
			#print("value: ", doy[i], F10p7[i], LT[i], cos_solzenith[i], szfact[i], latm_rad[i], lat_deg[i], lon_deg[i], hm[i])
			PEC[i], Nphm[i] = npsm_vpec(doy[i], F10p7[i], LT[i], cos_solzenith[i], szfact[i], latm_rad[i], lat_deg[i], lon_deg[i], altm, hm[i])
			#print("PEC[i], Nphm[i]", PEC[i], Nphm[i])
			#PEC = np.append(PEC, vpec)
			#Nphm = np.append(Nphm, Np)

	#print("PEC", PEC)

	return PEC, Nphm


def nedm2020(doy, F10p7, UT_hrs, lat_deg, lon_deg, altm,tec=0,nmf2=0,Np0_L=0,Np0_h=0):
	"""
		Syntax:
			npsmObj = nedm2020( lat_deg, lon_deg, altm, UT_hrs, doy, F10p7_sfu, parset['hmRefm'])
			STEC = npsmObj.stec()
			[Ne, altkm] = npsmObj.elden()
		Description:
			lat_deg = numphy variable/array of geodetic Latitude in degrees
			lon_deg = numphy variable/array of geodetic Longitude in degrees
			altm = numphy variable/array of geodetic Altitude in meters
			UT_hrs = universal time in hours
			doy = day of year
			F10p7_sfu = solar radio flux F10.7 in flux units
			optional parameters:
			IonLimitm = altitude limit of ionosphere in meter (above Earth's surfface)
			IonStepm = step size of each layer in meter
			PlasmaStepm = step size of the plasmasphere which extends from IonLimitm until Tx height
			default values:
			parset     = {    "IonLimitm" : 1000000.,    "IonStepm" : 10000,    "PlasmaStepm" : 50000}
			STEC = slant TEC connecting point P1 & P2 in TECU
			Ne = electron density Vector in 10**12 el/m**3
			altkm = corresponding altitude Vector in km
	"""

	(LT, latm_rad, cos_solzenith, szfact, cosDVmsz, cosDVsz, sinDVsz, cosSDVsz, sinSDVsz, cosTDVsz, sinTDVsz, cosAV,
	 sinAV, cosSAV, sinSAV) = ionpar(lat_deg, lon_deg, UT_hrs, doy)
	TECvt = NTCM(doy, F10p7, latm_rad, szfact, cosDVmsz, cosSDVsz, sinSDVsz, cosTDVsz, sinTDVsz)
    
	if(tec==0):
		TECvt = NTCM(doy, F10p7, latm_rad, szfact, cosDVmsz, cosSDVsz, sinSDVsz, cosTDVsz, sinTDVsz)
	else:
		TECvt = tec*1

	#print("NTCM = ", TECvt)
	if(nmf2==0):
		NmF2 = NPDM(doy, F10p7, LT, latm_rad, np.deg2rad(lat_deg), szfact, cosDVmsz, cosSDVsz, sinSDVsz, cosTDVsz,
    					 sinTDVsz)
	else:
		NmF2=nmf2*1
    
    #print("NPDM = ", NmF2)

	hmF2 = NPHM(doy, F10p7, LT, latm_rad, szfact, cosDVsz, sinDVsz, cosSDVsz, sinSDVsz, cosTDVsz, sinTDVsz)
	#print("NPHM = ", hmF2)

	#Np0_L = Np0_tp(doy, F10p7, LT, cos_solzenith, szfact)
	#print("Np0_L = ", Np0_L)

	#Hp_L = Hp_tp(doy, F10p7, LT, cos_solzenith)
	#print("Hp_L = ", Hp_L)

	#Np0_h = Np0_lp(doy, F10p7, LT, latm_rad, cos_solzenith, szfact)
	#print("Np0_h = ", Np0_h)

	# Hp_h = nedm.Hp_lp(doy[0], F10p7_sfu[0], LT, latm_rad, cos_solzenith )
	#Hp_h = Hp_lp(doy, F10p7, LT, latm_rad, cos_solzenith)
	#print("Hp_h = ", Hp_h)


	NeE, altkm = getNe_Elayer(doy, F10p7, LT, lat_deg, lon_deg, altm)
	#print("N_E, h = ", NeE, altkm)

	Nep, altkm, spec, Np0_L, Np0_h = npsm(doy, F10p7, LT, cos_solzenith, szfact, latm_rad, lat_deg, lon_deg, altm, hmF2*1000, Np0_L,Np0_h)
	#print("Nep, altkm, stec = ", Nep, altkm, stec)
	#print("tec_npsm", spec)
	#print("F10p7", F10p7)
	PECvt, Nphm = PECv(doy, F10p7, LT, cos_solzenith, szfact, latm_rad, lat_deg, lon_deg, hmF2 * 1000)
	#print("PEC = ", PECvt)

	redfact = 0.5 + 0.5 * (F10p7 - 60) / 140
	PECvt = PECvt * redfact
	Nm_corr = NmF2 - Nphm * redfact
	NeF, altkm = getNe_Flayer(TECvt, Nm_corr, hmF2, PECvt, altm)
	#print("NeF, altkm", NeF, altkm)

	Nep = Nep * redfact

	Ne = NeE + NeF + Nep
	#print("Nemerge", Nemerge)


	#print("len(lat_deg)", len(lat_deg))
	if len(lat_deg) == 1 and len(altm) > len(lat_deg):
		lat_deg = lat_deg * np.ones(np.shape(altm))
	if len(lon_deg) == 1 and len(altm) > len(lon_deg):
		lon_deg = lon_deg * np.ones(np.shape(altm))

	[x1, y1, z1] = myfunc.geodetic2ecef(np.deg2rad(lat_deg), np.deg2rad(lon_deg), altm)
	x2 = x1[1: len(x1)]
	y2 = y1[1: len(y1)]
	z2 = z1[1: len(z1)]
	x1 = x1[0: len(x1) - 1]
	y1 = y1[0: len(y1) - 1]
	z1 = z1[0: len(z1) - 1]
	ds = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
	dlm = np.hstack((ds, [0]))
	stec = np.sum(Ne * dlm) / 1.e+4  # TECU

	return Ne, altm/1000, stec, Nm_corr.max(), hmF2.max()#, Np0_L, Np0_h





def npsm(doy, F10p7, LT, cos_solzenith, szfact, latm_rad, lat_deg, lon_deg, altm, hmRefm, Np0_L, Np0_h ):

	"""
		  Syntax:
			  Ne, altkm, stec = npsm( doy, F10p7, LT, cos_solzenith, szfact, latm_rad, lat_deg, lon_deg, altm, hmRefm)
			  Ne = electron density in 10^12 el/m^3
			  altkm = altitude in km
			  stec = slant TEC in TECU
		  Description:
			  lat_deg = numphy variable/array of geodetic Latitude in degrees
			  lon_deg = numphy variable/array of geodetic Longitude in degrees
			  altm = numphy variable/array of geodetic Altitude in meters
			  UT_hrs = universal time in hours
			  doy = day of year
			  F10p7_sfu = solar radio flux F10.7 in flux units
			  optional parameters:
			  IonLimitm = altitude limit of ionosphere in meter (above Earth's surfface)
			  IonStepm = step size of each layer in meter
			  PlasmaStepm = step size of the plasmasphere which extends from IonLimitm until Tx height
			  default values:
			  parset     = {    "IonLimitm" : 1000000.,    "IonStepm" : 10000,    "PlasmaStepm" : 50000}
			  STEC = slant TEC connecting point P1 & P2 in TECU
			  Ne = electron density Vector in 10**12 el/m**3
			  altkm = corresponding altitude Vector in km
	"""

	if(Np0_L==0): Np0_L = Np0_tp(doy, F10p7, LT, cos_solzenith, szfact)
	else: Np0_L=Np0_L*1
	#print("Np0_L = ", Np0_L)

	Hp_L = Hp_tp(doy, F10p7, LT, cos_solzenith)
	#print("Hp_L = ", Hp_L)

	if(Np0_h==0): Np0_h = Np0_lp(doy, F10p7, LT, latm_rad, cos_solzenith, szfact)
	else: Np0_h = Np0_h*1
	#print("Np0_h = ", Np0_h)

	Hp_h = Hp_lp(doy, F10p7, LT, latm_rad, cos_solzenith)
	#print("Hp_h = ", Hp_h)

	Ne_tp, h = getNe_tp(Np0_L, Hp_L, latm_rad, altm, hmRefm)
	#print("Ne_tp, h = ", Ne_tp, h)

	Ne_lp, h = getNe_lp(Np0_h, Hp_h, altm, hmRefm)
	#print("Ne_lp, h = ", Ne_lp, h)


	if np.size(lat_deg) == 1 and np.size(altm) > np.size(lat_deg):
		lat_deg = lat_deg*np.ones(np.shape(altm))
		lon_deg = lon_deg*np.ones(np.shape(altm))

	[x1, y1, z1] = myfunc.geodetic2ecef(np.deg2rad(lat_deg) , np.deg2rad(lon_deg) , altm)
	x2 = x1[1 : len(x1)]
	y2 = y1[1 : len(y1)]
	z2 = z1[1 : len(z1)]
	x1 = x1[0 : len(x1)-1]
	y1 = y1[0 : len(y1)-1]
	z1 = z1[0 : len(z1)-1]
	ds = np.sqrt( (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2 )
	dlm = np.hstack( (ds, [0] ) )

	Ne = Ne_tp + Ne_lp
	stec = np.sum(Ne * dlm) / 1.e+4


	return Ne, altm/1000, stec,Np0_L,Np0_h


def npsm_vpec(doy, F10p7, LT, cos_solzenith, szfact, latm_rad, lat_deg, lon_deg, altm, hmRefm):
	"""
		  Syntax:
			  vpec, Ne[0] = npsm_vpec( doy, F10p7, LT, cos_solzenith, szfact, latm_rad, lat_deg, lon_deg, altm, hmRefm )
			  vpec = vertical plasmaspheric content in TECU
			  Ne[0] = plasmaspheric density (10!2 el/m^3) at peak density height

		  Description:
			  lat_deg = numphy variable/array of geodetic Latitude in degrees
			  lon_deg = numphy variable/array of geodetic Longitude in degrees
			  altm = numphy variable/array of geodetic Altitude in meters
			  UT_hrs = universal time in hours
			  doy = day of year
			  F10p7_sfu = solar radio flux F10.7 in flux units
			  optional parameters:
			  IonLimitm = altitude limit of ionosphere in meter (above Earth's surfface)
			  IonStepm = step size of each layer in meter
			  PlasmaStepm = step size of the plasmasphere which extends from IonLimitm until Tx height
			  default values:
			  parset     = {    "IonLimitm" : 1000000.,    "IonStepm" : 10000,    "PlasmaStepm" : 50000}
			  STEC = slant TEC connecting point P1 & P2 in TECU
			  Ne = electron density Vector in 10**12 el/m**3
			  altkm = corresponding altitude Vector in km
	"""

	Np0_L = Np0_tp(doy, F10p7, LT, cos_solzenith, szfact)
	#print("Np0_L = ", Np0_L)

	Hp_L = Hp_tp(doy, F10p7, LT, cos_solzenith)
	#print("Hp_L = ", Hp_L)

	Np0_h = Np0_lp(doy, F10p7, LT, latm_rad, cos_solzenith, szfact)
	#print("Np0_h = ", Np0_h)

	Hp_h = Hp_lp(doy, F10p7, LT, latm_rad, cos_solzenith)
	#print("Hp_h = ", Hp_h)

	Ne_tp, h = getNe_tp(Np0_L, Hp_L, latm_rad, altm, hmRefm)
	#print("Ne_tp, h = ", Ne_tp, h)

	Ne_lp, h = getNe_lp_vpec(Np0_h, Hp_h, altm, hmRefm)
	#print("Ne_lp, h = ", Ne_lp, h)


	Ne = Ne_tp + Ne_lp
	#print("Ne", Ne)
	vpec = np.sum(Ne[0:- 1] * np.diff(altm)) / 1.e+4
	#print("vpec, Ne[0]", vpec, Ne[0])

	return vpec, Ne[0]


if __name__ == "__main__":

	"""
	Testing each class / method
	"""



