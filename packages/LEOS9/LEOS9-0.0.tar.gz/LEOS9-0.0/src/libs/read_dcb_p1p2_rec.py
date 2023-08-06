def read_dcb_p1p2_rec_func(fname,mname):
    
    file=open(fname, 'r')
    Lines = file.readlines()
    file.close()
    
    for i in range(len(Lines)):
        if(len(Lines[i])>10):
            if(Lines[i][:10]=='G     '+mname):
                p1p2_dcb=float(Lines[i][28:36])
    
    return p1p2_dcb