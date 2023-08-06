import numpy as np

## groupSURF index by consecutive-series
def string_index(idx_list):
    "groupSURF index by consecutive-series"
    idx_list = np.sort(idx_list)
    check = (np.diff(idx_list,1,prepend=idx_list[0]) == 1)     ## NOTE size(check) = size(index) - 1 if wihout prepend
    index =np.where(check==False)[0]
    jndex = np.append(index[1:],len(idx_list))
    myString=''
    for _,(i,j) in enumerate(zip(index,jndex)):
        if (j-i)>1: myString = myString +str(int(idx_list[i])) +'-' +str(int(idx_list[j-1])) +','
        else:  myString = myString +str(int(idx_list[j-1])) +',' 
    return myString[:-1] 
#####
