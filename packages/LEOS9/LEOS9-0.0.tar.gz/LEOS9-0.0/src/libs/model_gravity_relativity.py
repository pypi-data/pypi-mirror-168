import numpy as np

c = 299792458
MU = 3.986005e+14

def model_gravity_relativity_func(xr,yr,zr,xs,ys,zs):

    receiverModule = np.sqrt(xr**2 + yr**2 + zr**2) 
    satelliteModule = np.sqrt(xs**2 + ys**2 + zs**2)
    distance = np.sqrt( (xs-xr)**2 + (ys-yr)**2 + (zs-zr)**2 )
    
    Relativity_gravity=2.0*MU/(c*c) * np.log((satelliteModule+receiverModule+distance)/(satelliteModule+receiverModule-distance));

    return Relativity_gravity
