import numpy 	as np
import pandas 	as pd
from .coord_rotation import CoordTransform
from ..utils.row_operation 	import unique_row


""" This module contains classes to build models of atomic crystals
"""

### ============================================================================
### Othogonal Crystal: 'v2O5', FCC, BCC,...
### ============================================================================
def _UnitCell_orthoRHOMBIC(crystal_type, lattice_constant=[1,1,1]):
	""" a DICT, contain 1 conventional cell of a Simple crystal UnitCell(FCC, BCC,...), in pricipal axes [100] [010] [001]
	# V2O5 crystal based on: https://materialsproject.org/materials/mvc-11944/ but change order of lattice constants: c,a,b
	# This order is the same as: 10.1016/j.triboint.2020.106750

	Args:
		crystal_type     : 'V2O5', 'FCC', 'BCC'
		lattice_constant=[1,1,1] : lattice constant [a,b,c] corresponding to [x,y,z]

	Returns:
		R : Nx3 array, contain positions of atoms in conventional unit cell.
	"""
	### ========================================================================
	## lattice vector and basis for CUBIC: 1 constant
	### ========================================================================
	if crystal_type=='FCC':
		point = np.array([[0,0,0], [0,1,0], [1,0,0], [1,1,0], [0,0,1], [0,1,1], [1,0,1], [1,1,1],
			             [0,0.5,0.5], [1,0.5,0.5], [0.5,0,0.5], [0.5,1,0.5], [0.5,0.5,0], [0.5,0.5,1]]).astype(float)
		atomType = [1]*point.shape[0]

	elif crystal_type=='BCC':
		point = np.array([[0,0,0], [0,1,0], [1,0,0], [1,1,0], [0,0,1], [0,1,1], [1,0,1], [1,1,1], [0.5,0.5,0.5]]).astype(float)
		atomType = [1]*point.shape[0]

	elif crystal_type=='DIAMOND':
		point = np.array([[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5],
                         [0.25, 0.25, 0.75], [0.25, 0.75, 0.25], [0.75, 0.25, 0.25], [0.75, 0.75, 0.75]]).astype(float)
		atomType = [1]*point.shape[0]

	elif crystal_type=='DIAMOND_2type':
		point1 = np.array([[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5],
                         [0.25, 0.25, 0.75], [0.25, 0.75, 0.25], [0.75, 0.25, 0.25], [0.75, 0.75, 0.75]]).astype(float)
		point2 = np.array([[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5],
                         [0.25, 0.25, 0.75], [0.25, 0.75, 0.25], [0.75, 0.25, 0.25], [0.75, 0.75, 0.75]]).astype(float)
		atomType = [1]*point1.shape[0] + [2]*point2.shape[0]

	### ========================================================================
	## lattice vector and basis for orthoRHOMBIC: 3 constant
	### ========================================================================
	elif crystal_type=='V2O5':
		V = np.array([[0.6495,	0,	0.6117], [0.3505,	0,	0.6117], [0.8505,	0.5,	0.3883], [0.1495,	0.5,	0.3883] ]).astype(float)
		Oxy = np.array([[0.8182,	0,	0.4883], [0.1818,	0,	0.4883], [0.355,	0,	0.9471], [0.5,	0,	0.5013], [0.645,	0,	0.9471],
		              [0.6818,	0.5,	0.5117], [0.3182,	0.5	,0.5117], [0.145,	0.5,	0.0529], [0.855,	0.5,	0.0529], [0,	0.5,	0.4987] ]).astype(float)
		point = np.vstack((V,Oxy))
		## atom Types
		atomType = [1]*V.shape[0] + [2]*Oxy.shape[0]


	else: raise Exception("Crystal-Type is only avalable for: 'FCC', 'BCC', 'V2O5' ")

	## Output - Scale to lattice constant
	point[:,0] = point[:,0]*lattice_constant[0]
	point[:,1] = point[:,1]*lattice_constant[1]
	point[:,2] = point[:,2]*lattice_constant[2]
	##
	BB = np.column_stack((atomType,point))  # concatenate a list to an array
	df = pd.DataFrame(BB, columns=['type','x','y','z'])
	return df
##--------

def lattice_orthoRHOMBIC(crystal_type, lattice_constant, orient=[[1,0,0],[0,1,0],[0,0,1]], size=[1,1,1], bound_cond=[1,1,1], tol_on_bound=0.1):
	""" Function to create atomic coordinates for crystal model

	Args:
		crystal_type  : 'V2O5', 'FCC', 'BCC'
		lattice_constant      : lattice constant
		orient        : 3x3 array, contain direction vectors, ex: ([[1,0,0], [0,1,0], [0,0,1]])
		size          : [Nax Nay Naz] 1x3 array, size of model, Nax is X-size in lattice constant unit
		bound_cond       : 1x3 Matrix contain convention for boundary conditions: 1 is peridic; 0 is not

	Returns:
		points : Nx3 array contain positions of atoms.
		box   : 3x2 array contain size of box contain lattice ([[xlo, xhi], [ylo, yhi], [zlo, zhi]])
		unit_box : 3x2 array contain size of unit cell
	"""
	## refine input (have to set dtype for numpy array)
	orient=np.asarray(orient,dtype=float);    bound_cond=np.asarray(bound_cond,dtype=float); size=np.asarray(size,dtype=int);

	### ========================================================================
	### compute on unit Cell (just atoms in conventional cell, must use lattice_constant=[1,1,1])
	### ========================================================================
	df = _UnitCell_orthoRHOMBIC(crystal_type,lattice_constant=[1,1,1]);           # in basic orient [1 0 0; 0 1 0; 0 0 1]
	P = df[['x','y','z']].values
	## first rotate crystal to find unit box
	BT = CoordTransform(new_orient=orient)
	R1 = BT.rotate_3d(P)
	## length of directional vector
	a1 = np.linalg.norm(orient[0] /max(abs(orient[0])))
	a2 = np.linalg.norm(orient[1] /max(abs(orient[1])))
	a3 = np.linalg.norm(orient[2] /max(abs(orient[2])))
	## unit box
	Bxlo = min(R1[:,0]);    Bxhi = Bxlo + a1
	Bylo = min(R1[:,1]);    Byhi = Bylo + a2
	Bzlo = min(R1[:,2]);    Bzhi = Bzlo + a3
	###--
	unit_box = np.array([[Bxlo, Bxhi], [Bylo, Byhi], [Bzlo, Bzhi]])

	### ========================================================================
	### add more atom before rotate to create atoms in computational_unit_Cell(box size = 1)
	### ========================================================================
	### on X side
	tmp = df.copy()         # to make a fixed tmp during loop (have to use np.copy to avoid changing value of P when tmp change)
	for i in range(2):
		tmp1 = tmp.copy(); tmp2 = tmp.copy()           # use DataFrame to include atom-id
		tmp1['x'] = tmp1['x'] + (i+1.0)
		tmp2['x'] = tmp2['x'] - (i+1.0)
		df = pd.concat([df, tmp1, tmp2], axis=0, ignore_index=True)  ## update df
	### on Y side
	tmp = df.copy()
	for i in range(2):
		tmp1 = tmp.copy(); tmp2 = tmp.copy()   # use DataFrame to include atom-id
		tmp1['y'] = tmp1['y'] + (i+1.0)
		tmp2['y'] = tmp2['y'] - (i+1.0)
		df = pd.concat([df, tmp1, tmp2], axis=0, ignore_index=True)  ## update df
	### on Z side
	tmp = df.copy()
	for i in range(2):
		tmp1 = tmp.copy(); tmp2 = tmp.copy()   # use DataFrame to include atom-id
		tmp1['z'] = tmp1['z'] + (i+1.0)
		tmp2['z'] = tmp2['z'] - (i+1.0)
		df = pd.concat([df, tmp1, tmp2], axis=0, ignore_index=True)  ## update df
	## remove duplicate rows
	# df = df.drop_duplicates(subset=['x','y','z'])    # cannot control tolerance
	_,uniIndex = unique_row(df[['x','y','z']].values, tol_decimal=2)
	df = df.iloc[uniIndex].sort_index()

	### ========================================================================
	### rotate crystal & Trim atoms out side unit_box
	### ========================================================================
	P = df[['x','y','z']].values   # new P
	R = BT.rotate_3d(P)
	## Update DataFrame
	df[['x','y','z']] = R
	df = df[df['x']<=unit_box[0,1] ];   df = df[df['x']>= unit_box[0,0] ];
	df = df[df['y']<=unit_box[1,1] ];   df = df[df['y']>= unit_box[1,0] ];
	df = df[df['z']<=unit_box[2,1] ];   df = df[df['z']>= unit_box[2,0] ];

	### 1. duplicate unit Cell
	### X-direction
	tmp = df.copy()
	for i in range(size[0]-1):
		tmp1 = tmp.copy()        # must use copy() to avoid change in df
		tmp1['x'] = tmp1['x'] + (i+1)*(unit_box[0,1] - unit_box[0,0])
		df = pd.concat([df, tmp1], axis=0, ignore_index=True)  ## update df
	### Y-direction
	tmp = df.copy()
	for i in range(size[1]-1):
		tmp1 = tmp.copy()
		tmp1['y'] = tmp1['y'] + (i+1)*(unit_box[1,1] - unit_box[1,0]);
		df = pd.concat([df, tmp1], axis=0, ignore_index=True)  ## update df
	### Z-direction
	tmp = df.copy()
	for i in range(size[2]-1):
		tmp1 = tmp.copy()
		tmp1['z'] = tmp1['z'] + (i+1)*(unit_box[2,1] - unit_box[2,0]);
		df = pd.concat([df, tmp1], axis=0, ignore_index=True)  ## update df
	## remove duplicate rows
	# df = df.drop_duplicates(subset=['x','y','z'])    # cannot control tolerance
	_,uniIndex = unique_row(df[['x','y','z']].values, tol_decimal=2)
	df = df.iloc[uniIndex].sort_index()

	### box
	box = np.copy(unit_box)
	box[0,1] = box[0,1] + (size[0]-1)* (box[0,1] - box[0,0]);
	box[1,1] = box[1,1] + (size[1]-1)* (box[1,1] - box[1,0]);
	box[2,1] = box[2,1] + (size[2]-1)* (box[2,1] - box[2,0]);

	### 2. trim on PBC
	tolB = tol_on_bound
	if bound_cond[0]==1:
		df = df[df['x'] < box[0,1]-tolB]       # remove point very near Boundary
	if bound_cond[1]==1:
		df = df[df['y'] < box[1,1]-tolB]
	if bound_cond[2]==1:
		df = df[df['z'] < box[2,1]-tolB]

	### ========================================================================
	### Output - Scale to lattice constant
	### ========================================================================
	## Scale positions
	df['x'] = df['x']*lattice_constant[0]
	df['y'] = df['y']*lattice_constant[1]
	df['z'] = df['z']*lattice_constant[2]
	## Scale box
	box[0,:] = box[0,:]*lattice_constant[0]
	box[1,:] = box[1,:]*lattice_constant[1]
	box[2,:] = box[2,:]*lattice_constant[2]
	unit_box[0,:] = unit_box[0,:]*lattice_constant[0]
	unit_box[1,:] = unit_box[1,:]*lattice_constant[1]
	unit_box[2,:] = unit_box[2,:]*lattice_constant[2]
	## Shift box to Zero corner  ---> need to define box in PDB file
	if box[0,0]>=0: shiftX = -box[0,0]
	else:           shiftX = box[0,0]
	if box[1,0]>=0: shiftY = -box[1,0]
	else:           shiftY = box[1,0]
	if box[2,0]>=0: shiftZ = -box[2,0]
	else:           shiftZ = box[2,0]
	##--
	df['x'] = df['x'] + shiftX
	df['y'] = df['y'] + shiftY
	df['z'] = df['z'] + shiftZ
	box[0,:] = box[0,:] + shiftX
	box[1,:] = box[1,:] + shiftY
	box[2,:] = box[2,:] + shiftZ
	##
	return df, box, unit_box   # DataFrame of "atomic coordinates", array of box size, lattice vector
##--------

def lattice_CUBIC(crystal_type, lattice_constant, orient=[[1,0,0],[0,1,0],[0,0,1]], size=[1,1,1], bound_cond=[1,1,1], tol_on_bound=0.1):
	""" Shortcut to create CUBIC crystal, as subclass of ortthoRHOMBIC

	Args:
		crystal_type  : 'FCC', 'BCC'
		lattice_constant=a    : lattice constant a
		orient        : 3x3 array, contain direction vectors, ex: ([[1,0,0], [0,1,0], [0,0,1]])
		size          : [Nax Nay Naz] 1x3 array, size of model, Nax is X-size in lattice constant unit
		bound_cond       : 1x3 Matrix contain convention for boundary conditions: 1 is peridic; 0 is not

	Returns:
		points : Nx3 array contain positions of atoms.
		box   : 3x2 array contain size of box contain lattice ([[xlo, xhi], [ylo, yhi], [zlo, zhi]])
		unit_box : 3x2 array contain size of unit cell
	"""
	## refine input (have to set dtype for numpy array)
	orient=np.asarray(orient,dtype=float);    bound_cond=np.asarray(bound_cond,dtype=float); size=np.asarray(size,dtype=int);
	
	lattice_constant = [lattice_constant, lattice_constant, lattice_constant]
	df, box, unit_box = lattice_orthoRHOMBIC(crystal_type, lattice_constant, orient, size, bound_cond, tol_on_bound)
	return df,box,unit_box








################## OLD function - not used now #############################
### ============================================================================
### Cubic Crystall Models: FCC, BCC,...
### ============================================================================
def cubicCRYSTAL_UnitCell(crystal_type, lattice_constant=1):
	""" a DICT, contain 1 conventional cell of a Simple crystal UnitCell(FCC, BCC,...), in pricipal axes [100] [010] [001]
	* Input:
		crystal_type     : 'FCC', 'BCC'
		lattice_constant=1 : lattice constant "a" is equal for x,y,z
	* Output:
		R : Nx3 array, contain positions of atoms in conventional unit cell."""
	## lattice vector and basis
	if crystal_type=='FCC':
		B = np.array([[0,0,0], [0,1,0], [1,0,0], [1,1,0], [0,0,1], [0,1,1], [1,0,1], [1,1,1],
			[0,0.5,0.5], [1,0.5,0.5], [0.5,0,0.5], [0.5,1,0.5], [0.5,0.5,0], [0.5,0.5,1]], dtype=float)
	elif crystal_type=='BCC':
		B = np.array([[0,0,0], [0,1,0], [1,0,0], [1,1,0], [0,0,1], [0,1,1], [1,0,1], [1,1,1], [0.5,0.5,0.5]], dtype=float)
	else: raise Exception("Crystal-Type is only avalable for: 'FCC', 'BCC' ")
	##
	return B*lattice_constant
##--------

def cubicCRYSTAL_Lattice(crystal_type, lattice_constant, orient=[[1,0,0],[0,1,0],[0,0,1]], size=[1,1,1], bound_cond=[1,1,1], bias=[[0.0,0.0],[0.0,0.0],[0.0,0]], tol_on_bound=0.1):
	""" Function to create atomic coordinates for crystal model
	* Input:
		crystal_type  : 'FCC', 'BCC'
		lattice_constant      : lattice constant (optional)
		orient        : 3x3 array, contain direction vectors, ex: ([[1,0,0], [0,1,0], [0,0,1]])
		size          : [Nax Nay Naz] 1x3 array, size of model, Nax is X-size in lattice constant unit
		bound_cond       : 1x3 Matrix contain convention for boundary conditions: 1 is peridic; 0 is not
		bias          : [biasX biasX biasX] added to length of unit_box, useful for some unusual direction such as 111, 112,...
	* Output:
		points : Nx3 array contain positions of atoms.
		box   : 3x2 array contain size of box contain lattice ([[xlo, xhi], [ylo, yhi], [zlo, zhi]])
		unit_box : 3x2 array contain size of unit cell"""

	# refine input (have to set dtype for numpy array)
	orient = np.asarray(orient, dtype=float);    bound_cond = np.asarray(bound_cond, dtype=float);  bias = np.asarray(bias, dtype=float);
	size = np.asarray(size, dtype=int);

	### compute on unit Cell (just atoms in conventional cell)
	P = cubicCRYSTAL_UnitCell(crystal_type);           # in basic orient [1 0 0; 0 1 0; 0 0 1]

	### computational_unit_Cell
	## first rotate crystal to find unit box
	BT = CoordTransform(new_orient=orient)
	R1 = BT.rotate_3d(P)
	## length of directional vector
	a1 = np.linalg .norm(orient[0] /max(abs(orient[0])))
	a2 = np.linalg .norm(orient[1] /max(abs(orient[1])))
	a3 = np.linalg .norm(orient[2] /max(abs(orient[2])))
	## unit box
	Bxlo = min(R1[:,0]);    Bxhi = Bxlo + a1
	Bylo = min(R1[:,1]);    Byhi = Bylo + a2
	Bzlo = min(R1[:,2]);    Bzhi = Bzlo + a3
	###--
	unit_box = np.array([[Bxlo+bias[0,0], Bxhi+bias[0,1]], [Bylo+bias[1,0], Byhi+bias[1,1]], [Bzlo+bias[2,0], Bzhi+bias[2,1]]])

	############################################################################
	## add more atom before rotate to create atoms in computational_unit_Cell(box size = 1)
	# on X side
	tmp = np.copy(P)         # to make a fixed tmp during loop (have to use np.copy to avoid changing value of P when tmp change)
	for i in range(2):
		tmp1 = np.copy(tmp); tmp2 = np.copy(tmp)
		tmp1[:,0] = tmp1[:,0] + (i+1.0)
		tmp2[:,0] = tmp2[:,0] - (i+1.0)
		P = np.vstack((P, tmp1, tmp2))
	# on Y side
	tmp = np.copy(P)
	for i in range(2):
		tmp1 = np.copy(tmp); tmp2 = np.copy(tmp)
		tmp1[:,1] = tmp1[:,1] + (i+1)
		tmp2[:,1] = tmp2[:,1] - (i+1)
		P = np.vstack((P, tmp1, tmp2))
	# on Z side
	tmp = np.copy(P)
	for i in range(2):
		tmp1 = np.copy(tmp); tmp2 = np.copy(tmp)
		tmp1[:,2] = tmp1[:,2] + (i+1)
		tmp2[:,2] = tmp2[:,2] - (i+1)
		P = np.vstack((P, tmp1, tmp2))
	# remove duplicate points
	P,_ = unique_row(P, tol_decimal=2)

	## rotate crystal & Trim atoms out side unit_box
	R = BT.rotate_3d(P)
	R = R[R[:,0] <= unit_box[0,1], :];   R = R[R[:,0] >= unit_box[0,0], :];
	R = R[R[:,1] <= unit_box[1,1], :];   R = R[R[:,1] >= unit_box[1,0], :];
	R = R[R[:,2] <= unit_box[2,1], :];   R = R[R[:,2] >= unit_box[2,0], :];

	### duplicate unit Cell
	# X-direction
	tmp = np.copy(R)
	for i in range(size[0]-1):
		tmp1 = np.copy(tmp)
		tmp1[:,0] = tmp1[:,0] + (i+1)*(unit_box[0,1] - unit_box[0,0])
		R = np.vstack((R, tmp1))
	# Y-direction
	tmp = np.copy(R)
	for i in range(size[1]-1):
		tmp1 = np.copy(tmp)
		tmp1[:,1] = tmp1[:,1] + (i+1)*(unit_box[1,1] - unit_box[1,0]);
		R = np.vstack((R, tmp1))
	# Z-direction
	tmp = np.copy(R)
	for i in range(size[2]-1):
		tmp1 = np.copy(tmp)
		tmp1[:,2] = tmp1[:,2] + (i+1)*(unit_box[2,1] - unit_box[2,0]);
		R = np.vstack((R, tmp1))
	# eliminate duplicated atoms
	R,_ = unique_row(R, tol_decimal=2)

	# box
	box = np.copy(unit_box)
	box[0,1] = box[0,1] + (size[0]-1)* (box[0,1] - box[0,0]);
	box[1,1] = box[1,1] + (size[1]-1)* (box[1,1] - box[1,0]);
	box[2,1] = box[2,1] + (size[2]-1)* (box[2,1] - box[2,0]);

	# trim on PBC
	tolB = tol_on_bound
	if bound_cond[0]==1:
		R = R[R[:,0]<box[0,1]+tolB, :]       # remove point very near Boundary
		R = R[R[:,0]<box[0,1]-tolB, :]
	if bound_cond[1]==1:
		R = R[R[:,1]<box[1,1]+tolB, :]
		R = R[R[:,1]<box[1,1]-tolB, :]
	if bound_cond[2]==1:
		R = R[R[:,2]<box[2,1]+tolB, :]
		R = R[R[:,2]<box[2,1]-tolB, :]
	# --

	### Output
	out1 = lattice_constant*R               # matrix of atomic coordinates
	out2 = lattice_constant*box             # Matrix of box size
	out3 = lattice_constant*unit_box          # lattice vector
	return out1, out2, out3
##--------
