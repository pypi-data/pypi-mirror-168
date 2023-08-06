import numpy as np
from scipy import interpolate

def model_tropo_nominal_func(latr,altr,doy,mfunc_tropo_dry,mfunc_tropo_wet):

    # tropDryNominal = 1.013*2.27*np.exp((-0.116e-03)*altr)
    # tropWetNominal = 0.10
    
    # tropo_dry=tropDryNominal*mfunc_tropo_dry
    # tropo_wet=tropWetNominal*mfunc_tropo_wet
    
    if np.isscalar(latr):
        if(latr>=0): Dmin=28
        if(latr<0): Dmin=211
    else: 
        Dmin=latr*np.nan
        Dmin[latr>=0]=28
        Dmin[latr<0]=211
        
    MOPSgm = 9.784
    MOPSg  = 9.80665
    MOPSk1 = 77.604
    MOPSk2 = 382000.0
    MOPSRd = 287.054
    MOPSzhydCT = ( 1E-6 * MOPSk1 * MOPSRd / MOPSgm )
    MOPSzwetCT = ( 1E-6 * MOPSk2 * MOPSRd )

    latMOPS=np.array((15,30,45,60,75,90))

    P0avg=np.array((1013.25,1017.25,1015.75,1011.75,1013.00,1013.00))
    T0avg=np.array((299.65, 294.15, 283.15, 272.15, 263.65, 263.65))
    E0avg=np.array((26.31,  21.79,  11.66,   6.78,   4.11,   4.11))
    B0avg=np.array((6.30E-3,6.05E-3,5.58E-3,5.39E-3,4.53E-3,4.53E-3))
    l0avg=np.array((2.77,   3.15,   2.57,   1.81,   1.55,   1.55))

    dP0avg=np.array((0.0,  -3.75,  -2.25,  -1.75,  -0.50,  -0.50))
    dT0avg=np.array((0.0,    7.0,   11.0,   15.0,   14.5,   14.5))
    dE0avg=np.array((0.0,   8.85,   7.24,   5.36,   3.39,   3.39))
    dB0avg=np.array((0.0E-3,0.25E-3,0.32E-3,0.81E-3,0.62E-3,0.62E-3))
    dl0avg=np.array((0.0,   0.33,   0.46,   0.74,   0.30,   0.30))

    latMOPS=np.append(-np.flipud(latMOPS),latMOPS)
    P0avg=np.append(np.flipud(P0avg),P0avg)
    T0avg=np.append(np.flipud(T0avg),T0avg)
    E0avg=np.append(np.flipud(E0avg),E0avg)
    B0avg=np.append(np.flipud(B0avg),B0avg)
    l0avg=np.append(np.flipud(l0avg),l0avg)
    dP0avg=np.append(np.flipud(dP0avg),dP0avg)
    dT0avg=np.append(np.flipud(dT0avg),dT0avg)
    dE0avg=np.append(np.flipud(dE0avg),dE0avg)
    dB0avg=np.append(np.flipud(dB0avg),dB0avg)
    dl0avg=np.append(np.flipud(dl0avg),dl0avg)

    fp0=interpolate.interp1d(latMOPS, P0avg,'linear')
    ft0=interpolate.interp1d(latMOPS, T0avg,'linear')
    fe0=interpolate.interp1d(latMOPS, E0avg,'linear')
    fb0=interpolate.interp1d(latMOPS, B0avg,'linear')
    fl0=interpolate.interp1d(latMOPS, l0avg,'linear')
    fdp0=interpolate.interp1d(latMOPS, dP0avg,'linear')
    fdt0=interpolate.interp1d(latMOPS, dT0avg,'linear')
    fde0=interpolate.interp1d(latMOPS, dE0avg,'linear')
    fdb0=interpolate.interp1d(latMOPS, dB0avg,'linear')
    fdl0=interpolate.interp1d(latMOPS, dl0avg,'linear')

    p0=fp0(latr)*1
    t0=ft0(latr)*1
    e0=fe0(latr)*1
    b0=fb0(latr)*1
    l0=fl0(latr)*1
    dp0=fdp0(latr)*1
    dt0=fdt0(latr)*1
    de0=fde0(latr)*1
    db0=fdb0(latr)*1
    dl0=fdl0(latr)*1

    MOPScosCT = ( 2.0 * np.pi / 365.25 )
    
    p = p0 - dp0 * np.cos ( (doy - Dmin)*MOPScosCT )
    t = t0 - dt0 * np.cos ( (doy - Dmin)*MOPScosCT )
    e = e0 - de0 * np.cos ( (doy - Dmin)*MOPScosCT )
    b = b0 - db0 * np.cos ( (doy - Dmin)*MOPScosCT )
    l = l0 - dl0 * np.cos ( (doy - Dmin)*MOPScosCT )
    
    Tzo_dry = MOPSzhydCT * p
    Tzo_wet = ( MOPSzwetCT /(MOPSgm*(l+1.0)-b*MOPSRd) ) * (e/t)
    
    factor=b*altr/t
    
    exp1=MOPSg/(MOPSRd*b)
    tropDryNominal=Tzo_dry*((1.0-factor)**exp1)
    
    exp2=((l+1.0)*MOPSg)/(MOPSRd*b)-1.0
    tropWetNominal=Tzo_wet*((1.0-factor)**exp2)
    
    tropo_dry=tropDryNominal*mfunc_tropo_dry
    tropo_wet=tropWetNominal*mfunc_tropo_wet
    
    return tropo_dry, tropo_wet
