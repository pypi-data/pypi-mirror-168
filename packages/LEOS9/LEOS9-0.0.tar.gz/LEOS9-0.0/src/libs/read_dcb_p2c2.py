import numpy as np

def read_dcb_p2c2_func(fname):
    
    file=open(fname, 'r')
    Lines = file.readlines()
    file.close()
    
    p2c2_dcb=np.zeros((32))
    for i in range(len(Lines)):
        if(Lines[i][0]=='G'):
            prn=int(Lines[i][1:3])
            p2c2_dcb[prn-1]=float(Lines[i][28:36])
    
    return p2c2_dcb