from ..compute    import dist2_point2points
from ..model      import box_orientation, CoordTransform
import numpy      as np


## 1. Local Crystallinity
def localCRYSTALLINITY(points, g_vectors=((1,0,0)), lattice_constant=1.0, zDirect='001', switch_function=None):
	"""Function to Calculate Order Parameter with multi_vectors K.
	By Cao Thang, Apr 2019

    Args:
        points (Nx3 np.array): array contains bonding vectors between neighboring  atoms j and ref atom i
		g_vectors (tuple): 2d-tuple contains "directions_vectors" for g_vectors  (ex: ((1,0,0), (0,1,0)). The actual g_vectors will be computed in function. Default to ((1,0,0)).
		lattice_constant (float): lattice constant of crystal. Default to 1.
        zDirect (str): direction of Z-direction, available '001'  '110'  '111'. Default to '001'.
        switch_function (list): list contain values of switching function s(Rj) (Rj is positions of atom j). Default to None.

    Returns:
		aveLC (float): is average Order Parameter , tage over on input g_factors, 0 <= LC <=1
		LC (list): list of real numbers, are Order Parameters corresponding to each g-vector 0 <= LC <=1
		# S (not computed) Kx1 vetor of complex numbers, are Static Structure Factors corresponding to each g-vector

	Examples:
    ```python
        S = thatool.colvar.localCRYSTALLINITY([1,0,0; 0,1,0], switch_function=sw, zDirect='001')
    ```
	Notes:
		If multi g-vectors is input, then OrderPara is take by averaging over all g-vectors.
	"""
	##==== compulsory Inputs
	P = np.asarray(points)

	##==== optional Inputs (compute switching function)
	if switch_function!=None:
		Rij = dist2_point2points([0,0,0], P)
		mySW,_ = switch_function.Evaluate(Rij['bond_len'])
	else:
		mySW = np.ones(P.shape[0])

	## Define reciprocal vectors
	g = (4*np.pi/lattice_constant)*np.asarray(g_vectors)

	## Rotate reciprocal vectors
	if zDirect!=None:
		newAxis,_ = box_orientation(zDirect=zDirect)
		oldAxis = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
	BT = CoordTransform(old_orient=oldAxis, new_orient=newAxis)  # forward rotate
	g = BT.rotate_3d(g)

	## Compute Order Parameter
	Ng = g.shape[0];
	LC = np.zeros(Ng, dtype=float);    # LC is a vector of Ng components
	# S = np.zeros(Ng, dtype=complex);   # S is a vector of Ng complex-components
	# --
	for i in range(Ng):
		d = np.einsum('ij,j->i', P, g[i,:])   # same d = P @ g[i,:]   , dot product of each row of matrix P w.r.t vetor g[i,:]

		SumNatoms = sum(mySW*np.exp(1j*d));     # Sum over all atoms
		tmp  = SumNatoms/ sum(mySW) ;
		LC[i] = (abs(tmp))**2;                # Order_Parameter square of module of complex number
		# S[i] = tmp;                           # Static Structure Factor
	
	aveLC = sum(LC)/Ng;                  # Static Structure Factor Averaging over all g_vectors
	return aveLC, LC

