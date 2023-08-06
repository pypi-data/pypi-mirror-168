
c = 299792458

def model_ionfree_func(f1,f2,p1,p2,l1,l2):

    mp1=(f1**2)/(f1**2-f2**2);
    mp2=-(f2**2)/(f1**2-f2**2);

    ml1=(f1**2)/(f1**2-f2**2);
    ml2=-(f1*f2)/(f1**2-f2**2);
    wIF=c/(ml1*f1+ml2*f2)
    
    # wIF=c*(f1-f2)/(f1**2-f2**2)

    pIF=mp1*p1+mp2*p2
    lIF=wIF*(ml1*l1+ml2*l2)

    return pIF, lIF

# w1=c/f1
# w2=c/f2

# ml1=(f1**2)/(f1**2-f2**2);
# ml2=-(f1*f2)/(f1**2-f2**2);
# lif1=(ml1*l1+ml2*l2)
# wif1=c/(ml1*f1+ml2*f2)

# C1= (f1**2)/((f1**2)-(f2**2));
# C2=-(f2**2)/((f1**2)-(f2**2));
# lif2=C1*l1+C2*l2;
# wif2=c/(C1*f1+C2*f2)