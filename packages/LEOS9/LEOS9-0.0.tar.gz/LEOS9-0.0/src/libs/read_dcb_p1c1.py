import numpy as np

def read_dcb_p1c1_func(fname):
    
    file=open(fname, 'r')
    Lines = file.readlines()
    file.close()
    
    p1c1_dcb=np.zeros((32))
    for i in range(len(Lines)):
        if(Lines[i][0]=='G'):
            prn=int(Lines[i][1:3])
            p1c1_dcb[prn-1]=float(Lines[i][28:36])
    
    return p1c1_dcb