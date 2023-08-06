import numpy as np
from scipy import interpolate

def model_tropo_niel_func(doy,latr,elrad,altr):
    # simple function would be
    # mh=1/np.sin(elrad);
    if np.isscalar(latr):
        if(latr>75): latr=75
        if(latr>=0): d0=28
        if(latr<0): d0=211
    else: 
        latr[latr>75]=75
        d0=latr*np.nan
        d0[latr>=0]=28
        d0[latr<0]=211
    
    # coef dry NMF 
    latNmf=np.array((15,30,45,60,75))
    am=np.array((1.2769934E-3, 1.2683230E-3, 1.2465397E-3, 1.2196049E-3, 1.2045996E-3))
    bm=np.array((2.9153695E-3, 2.9152299E-3, 2.9288445E-3, 2.9022565E-3, 2.9024912E-3))
    cm=np.array((62.610505E-3, 62.837393E-3, 63.721774E-3, 63.824265E-3, 64.258455E-3))
    
    aa=np.array((0.0000000E-0, 1.2709626E-5, 2.6523662E-5, 3.4000452E-5, 4.1202191E-5))
    ba=np.array((0.0000000E-0, 2.1414979E-5, 3.0160779E-5, 7.2562722E-5, 11.723375E-5))
    ca=np.array((0.0000000E-0, 9.0128400E-5, 4.3497037E-5, 84.795348E-5, 170.37206E-5))
    
    aht=2.53E-5 
    bht=5.49E-3
    cht=1.14E-3

    # coef wet NMF 
    aw=np.array((5.8021897e-4,5.6794847e-4,5.8118019e-4,5.9727542e-4,6.1641693e-4))
    bw=np.array((1.4275268e-3,1.5138625e-3,1.4572752e-3,1.5007428e-3,1.7599082e-3))
    cw=np.array((4.3472961e-2,4.6729510e-2,4.3908931e-2,4.4626982e-2,5.4736038e-2))
    
    latNmf=np.append(-np.flipud(latNmf),latNmf)
    am=np.append(np.flipud(am),am)
    bm=np.append(np.flipud(bm),bm)
    cm=np.append(np.flipud(cm),cm)
    aa=np.append(np.flipud(aa),aa)
    ba=np.append(np.flipud(ba),ba)
    ca=np.append(np.flipud(ca),ca)
    aw=np.append(np.flipud(aw),aw)
    bw=np.append(np.flipud(bw),bw)
    cw=np.append(np.flipud(cw),cw)
    
    fam=interpolate.interp1d(latNmf, am,'linear')
    fbm=interpolate.interp1d(latNmf, bm,'linear')
    fcm=interpolate.interp1d(latNmf, cm,'linear')
    faa=interpolate.interp1d(latNmf, aa,'linear')
    fba=interpolate.interp1d(latNmf, ba,'linear')
    fca=interpolate.interp1d(latNmf, ca,'linear')
    faw=interpolate.interp1d(latNmf, aw,'linear')
    fbw=interpolate.interp1d(latNmf, bw,'linear')
    fcw=interpolate.interp1d(latNmf, cw,'linear')
    
    ah=fam(latr)-faa(latr)*np.cos(2*np.pi*(doy-1-d0)/365.25) # doys are from 0 to 364 in NMF
    bh=fbm(latr)-fba(latr)*np.cos(2*np.pi*(doy-1-d0)/365.25) # doys are from 0 to 364 in NMF
    ch=fcm(latr)-fca(latr)*np.cos(2*np.pi*(doy-1-d0)/365.25) # doys are from 0 to 364 in NMF
    Num=1+(ah/(1+bh/(1+ch)))
    Den=np.sin(elrad)+(ah/(np.sin(elrad)+bh/(np.sin(elrad)+ch)))
    Numh=1+(aht/(1+bht/(1+cht)))
    Denh=np.sin(elrad)+(aht/(np.sin(elrad)+bht/(np.sin(elrad)+cht)))
    mh_dry=Num/Den+(1/np.sin(elrad)-Numh/Denh)*altr/1e3
    
    ah=faw(latr)*1
    bh=fbw(latr)*1
    ch=fcw(latr)*1
    Num=1+(ah/(1+bh/(1+ch)))
    Den=np.sin(elrad)+(ah/(np.sin(elrad)+bh/(np.sin(elrad)+ch)))
    mh_wet=Num/Den

    return mh_dry, mh_wet
