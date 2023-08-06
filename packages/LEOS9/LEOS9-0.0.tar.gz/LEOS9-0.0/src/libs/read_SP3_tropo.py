import numpy as np

def read_SP3_tropo_func(fname,mname):
    
    file=open(fname, 'r')
    Lines = file.readlines()
    file.close()
    
    sec=[]
    trotot=[]
    
    for i in range(len(Lines)):
        if(Lines[i][:21]=='+TROP/STA_COORDINATES'):
            x=float(Lines[i+2][16:28])
            y=float(Lines[i+2][29:41])
            z=float(Lines[i+2][42:54])
        if(Lines[i][:14]=='+TROP/SOLUTION'):
            init_data=i*1
            break
        
    for i in range(init_data,len(Lines)):
        if(Lines[i][:5]==' '+mname):
            sec.append(float(Lines[i][13:18]))
            trotot.append(float(Lines[i][19:25])/1e3)
    
    sec=np.hstack(sec)
    trotot=np.hstack(trotot)
    
    return x, y, z, trotot, sec