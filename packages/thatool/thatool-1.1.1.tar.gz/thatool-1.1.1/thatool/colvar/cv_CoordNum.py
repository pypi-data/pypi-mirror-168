from ..utils.compute_distance    import dist2_point2points
import numpy as np





## 3. Coordination
def CoordNum(Points, **kwargs):
    """The Coordination is the size of input "Points", this function just weight it with a switching function 
    * Compulsory Inputs:
    ** optional Inputs:
            switchFunc=[1,1...,1] : Nx1 array, contain values of switching function s(Rj) (Rj is positions of atom j)
    * Output:       
            coord  : scalar, Order Parameter
        Example: S = thaTool.OrderPara.Coordination([1,0,0; 0,1,0], SW=sw)
    By Cao Thang, Aug 2020
    """
    ##==== compulsory Inputs 
    P = np.asarray(Points)	
    
    ##==== optional Inputs 
    if 'switchFunc' in kwargs: 
        sw = kwargs['switchFunc']
        Rij = dist2_point2points([0,0,0], P)   
        mySW,_ = sw.Evaluate(Rij['bond_len'])
    else: mySW = np.ones(P.shape[0]) 

    ##==== Compute Coordination
    coordNum = sum(mySW)       # not compute final j, because no more k
    return  coordNum  
##--------



