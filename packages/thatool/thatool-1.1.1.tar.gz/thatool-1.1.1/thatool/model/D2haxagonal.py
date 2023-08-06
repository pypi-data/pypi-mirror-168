from numpy      import array, zeros, copy, column_stack, linalg, sin, cos, pi, gcd, sqrt, arctan
import pandas 	as pd
from matplotlib 			import path
from .coord_rotation 		import rot1axis
from ..utils.row_operation 	import unique_row


"""
* haxagonal Boron Nitride (h-BN) have the same configuration as Graphene
	C-C bond: 1.4 - 1.42 Amstrom
	B-N bond: 1.4 - 1.43 Amstrom
Ref: 10.1039/c7ra00260b
"""

### ============================================================================
### Graphene-based Models:
### ============================================================================
def _UnitCell_2Dhoneycomb(m, n, bond_CC=1.421, basis_atom='AB'):
	"""Calculates the 3D Cartesian coordinates of atoms of 1 units cell of (n,m)graphene sheet, which which n >= m >= 0
	By Cao Thang Nguyen, Nov 2019 (update 2022)

	Args:
		n,m  (int): Chiral indices n>=m>=0
		bond_CC (float): Length of C-C bonds
		basis_atom (str): 'AB'/'A'/'B': to create semi-Graphene lattice for adoptting Hydrogen atoms
			 - 'AB': full Garaphene-like crystal
			 - 'A': semi Graphene-like with atom at A-position
			 - 'B': semi Graphene-like with atom at B-position

	Returns:
		df (DataFrame)  : Nx3 array, contain positions of atoms of 1 units cell of (n,m)graphene sheet.
		unitbox (array) : size of unit box
		param (dict)	: dict contains characteristic parameters of graphene lattice.
			'Chiral_len' (float)    : length of Translational unit vector, corresponding to length on Y direction
			'Translate_len' (float) : length of Chiral vector, corresponding to length on X direction
			'Chiral_ang' (float)    : Chiral angle of Graphene sheet in Degree.
			'Chiral_vector' (array_1x2) : Chiral vector
			'Translate_vector' (array_1x2): translations vector

	Notes:
		n=1, m=0 : is the unit cell for Zigzag
		n=1, m=1 : is the unit cell for Armchair
		n>m      : unit cell is automatically computed

	Refs:
		Dresselhaus et al. “Physics of Carbon Nanotubes.”, 1995, doi:10.1016/0008-6223(95)00017-8.
		Antonsen, and Thomas Garm Pedersen. “Characterisation and Modelling of Carbon Nanotubes,” 2013.
	"""
	## check if n >= m >= 0
	if n < m or m < 0:
		raise Exception('Bad choice of (n,m). Be sure n >= m >= 0')
	if basis_atom not in ['AB', 'A', 'B']:
		raise Exception("Choose basis_atom in list: 'AB', 'A', 'B' ")

	## Compute ONE unit cell
	if m==0:
		m=0;	n = n/n
	elif m==n:
		m = n/n;	n = n/n
	else:
		m=m;	n=n
	m=int(m);   n=int(n)
	###=========================================================================
	### Calculate the characteristic parameters of 2D graphene
	###=========================================================================
	## Lattice vector and two atomic basis b1, b2 for the graphene sheet
	latt = bond_CC*sqrt(3)               # length of lattice vector a = |a1| = |a2|
	a1 = latt*array([1, 0])
	a2 = latt*array([cos(pi/3), sin(pi/3)])
	b1 = latt*array([0, 0])
	b2 = latt*array([1/2, 1/(sqrt(3)*2)])

	## Translations vector
	G = gcd(2*n+m, 2*m+n)           # Greatest common divisor
	t1 = (2*m+n)/G
	t2 = -(2*n+m)/G
	## Chiral and translations vector
	C = n*a1 + m*a2
	T = t1*a1 + t2*a2
	ChiralAng = arctan(m*sqrt(3)/(2*n+m))   # Chiral angle in rad
	ChiralAng = ChiralAng*180/pi            # convert to deg
	## Calculate periodic unit cell
	lC = linalg.norm(C)        # length of Chiral vector, periodic on X
	lT = linalg.norm(T)        # length of Translation vector, periodic on Y
	unitbox = array([[0, lC], [-lT, 0], [0, 0]], dtype=float)

	## the number of haxagons in the 1D unit cell
	N = int(2*(n**2 + m**2 + n*m)/G)
	###=========================================================================
	### Calculations of points for the graphene sheet
	###=========================================================================
	R = zeros((4*N**2,2))    # just estimate sheet_size
	index = -1;
	for i in range(0,N,1):
		for j in range(-N,i,1):
			## For full-Graphene sheet
			if basis_atom=='AB':
				index = index + 1
				R[index, :] = i*a1 + j*a2 + b1        # atom A
				index = index + 1
				R[index, :] = i*a1+j*a2 + b2          # atom B
			elif basis_atom=='A':
				index = index + 1
				R[index, :] = i*a1 + j*a2 + b1        # atom A
			elif basis_atom=='B':
				index = index + 1
				R[index, :] = i*a1+j*a2 + b2          # atom B

	R = R[0:index+1, :]     # remove extra zero-rows
	###=========================================================================

	## Calculation of 2D cartesian coordinates for the (n,m)SWCNT. To avoid identical points the polygon ABCD restraining the CNT points is moved southwest.
	epsilon = (C[0]+T[0]) * ((bond_CC/1000)/linalg.norm(T)) 
	myPoly = array([[0,0], [C[0],C[1]], [C[0]+T[0],C[1]+T[1]], [T[0],T[1]]]) - epsilon
	## check points inside polygon
	poly = path.Path(myPoly)
	insideIndex = poly.contains_points(R)
	Rin = R[insideIndex]           # take the inside points

	## Rotate matrix to align Chiral direction with X direction
	P,_ = unique_row(Rin, tol_decimal=2)    # remove duplicate points
	param = {'Chiral_len': lC, 
		     'Translate_len': lT, 
		     'Chiral_ang': ChiralAng,
		     'Chiral_vector': C,
		     'Translate_vector': T}
	return P, unitbox, param


def _UnitCell_Graphene(m, n, bond_CC=1.421, basis_atom='AB'):
	## Rotate matrix to align Chiral direction with X direction
	xy,unitbox,param = _UnitCell_2Dhoneycomb(m, n, bond_CC=bond_CC, basis_atom=basis_atom)    # remove duplicate points
	z = zeros((xy.shape[0], 1))              # assign z coordinates = 0
	P = column_stack((xy, z))  
	ang = param['Chiral_ang']   
	P = rot1axis(P, ang, axis='Z')
	## save df
	df = pd.DataFrame(data=P, columns=['x','y','z'], dtype=float)
	return df, unitbox, param


def lattice_Graphene(m, n, bond_CC=1.421, sheet_size=[1,1], sheet_number=1, layer_bond=3.35, basis_atom='AB'):
	"""Calculates the 3D Cartesian coordinates of atoms of (n,m)graphene sheet/ Graphite
	By Cao Thang Nguyen, Nov 2019 (update 2022)

	Args:
		n,m (int): Chiral indices n>=m>=0
		bond_CC (float): Length of C-C bonds
		sheet_size (list): [Xsize, Ysize], size of graphene sheet
		sheet_number (int): number of sheets
		layer_bond : Length of plane-plane bonds
		basis_atom (str): 'AB'/'A'/'B': to create semi-Graphene lattice for adoptting Hydrogen atoms
			 - 'AB': full Garaphene-like crystal
			 - 'A': semi Graphene-like with atom at A-position
			 - 'B': semi Graphene-like with atom at B-position

	Returns:
		df (DataFrame) : Nx3 array, contain positions of atoms of 1 units cell of (n,m)graphene sheet.
		box (array)    : Simulation box
		param (dict)   : dict contains characteristic parameters of graphene lattice.
			'Chiral_len' (float)    : length of Translational unit vector, corresponding to length on Y direction
			'Translate_len' (float) : length of Chiral vector, corresponding to length on X direction
			'Chiral_ang' (float)    : Chiral angle of Graphene sheet in Degree.
			'Chiral_vector' (array) : Chiral vector
			'Translate_vector' (array) : translations vector
		
	Notes:
		n=1, m=0 : is the unit cell for Zigzag
		n=1, m=1 : is the unit cell for Armchair
		n>m      : unit cell is automatically computed
	"""
	## Compute coordinates of 1 unit cell
	df,unitbox,param = _UnitCell_Graphene(m, n, bond_CC, basis_atom)
	lC,lT = param['Chiral_len'], param['Translate_len']
	## Duplicate unit cell
	lx, ly = sheet_size[0], sheet_size[1]
	repX = int(round(lx/lC))           # number of unit cell in X direction
	repY = int(round(ly/lT))           # number of unit cell in Y direction
	if repX>=2:
		dfold = df.copy()
		for i in range(1,repX,1):
			dftmp = dfold.copy()
			dftmp['x'] = dftmp['x'] + i*lC
			df = df.append(dftmp, ignore_index=True)
	if repY>=2:
		dfold = df.copy()
		for i in range(1,repY,1):
			dftmp = dfold.copy()
			dftmp['y'] = dftmp['y'] + i*lT
			df = df.append(dftmp, ignore_index=True)
	if sheet_number>=2:
		dfold = df.copy()
		for i in range(1,int(sheet_number),1):
			dftmp = dfold.copy()
			dftmp['z'] = dftmp['z'] + i*layer_bond
			df = df.append(dftmp, ignore_index=True)

	## remove duplicate points
	df.drop_duplicates(inplace=True, ignore_index=True)
	## compute box periodic
	box = copy(unitbox)
	if repX>0: 
		box[0,1] = box[0,1] + (repX -1)*lC
	if repY>0: 
		box[1,1] = box[1,1] + (repY -1)*lT
	## box_size in Z
	if sheet_number>0:
		box[2,1] = box[2,1] + layer_bond/2 + (sheet_number-1)*layer_bond
		box[2,0] = box[2,0] - layer_bond/2

	return df, box, param
