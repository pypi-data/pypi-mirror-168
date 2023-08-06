from ..compute    import dist2_point2points
from ..model      import box_orientation, CoordTransform
import numpy      as np


## 2. FCC CUBIC harmonic
def fccCUBIC(points, alpha=27, zDirect='001', switch_function=None):
    """Function to Calculate FCC CUBIC parameters.
    By Cao Thang, Mar 2020

    Args:
        points (Nx3 np.array): array contains bonding vectors between neighboring  atoms j and ref atom i
        alpha (int): coefficient of harmonic function. Default to 27.
        zDirect (str): direction of Z-direction, available '001'  '110'  '111'. Default to '001'.
        switch_function (list): list contain values of switching function s(Rj) (Rj is positions of atom j). Default to None.

    Returns:
        param (float): Order Parameter.

    Examples:
    ```python
        S = thatool.colvar.fccCUBIC([1,0,0; 0,1,0], alpha=3, zDirect='001', switch_function=sw)
    ```

    Notes:
        Must choose suitable Rcut for Switching function.
    """
    ##==== compulsory Inputs
    P = np.asarray(points)

	##==== optional Inputs (compute switching function)
    if switch_function is not None:
        Rij = dist2_point2points([0,0,0], P)
        mySW,_ = switch_function.Evaluate(Rij['bond_len'])
    else:
        mySW = np.ones(P.shape[0])

    ## Rotate crystal, note Rotate P  --> rotate after find neighbor
    if zDirect is not None:
        newAxis,_ = box_orientation(zDirect=zDirect)
        oldAxis = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        BT = CoordTransform(old_orient=newAxis, new_orient=oldAxis)          # reverse rotate
        P = BT.rotate_3d(P)

    ##==== Compute FCC CUBIC Parameter
    x = P[:,0];     y = P[:,1];    z = P[:,2]
    Rij = dist2_point2points((0,0,0), P)
    r = Rij['bond_len']

    Ca = ( (x*y)**4 + (y*z)**4 + (z*x)**4 )/r**8 - alpha*((x*y*z)**4) /r**12
    a = 80080.0/(2717.0+16*alpha)
    b = 16.0*(alpha-143)/(2717.0+16*alpha)
    phi = (a*Ca + b)

    FCCcubic = sum(mySW*phi)/ sum(mySW)        # Sum over all atoms, Order_Parameter
    return  FCCcubic
