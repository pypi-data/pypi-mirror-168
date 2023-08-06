from logging import raiseExceptions
from numpy      import array, zeros, copy, dot, column_stack, flip, linalg, sin, cos, pi
import pandas 	as pd
from .D2haxagonal 		    import _UnitCell_2Dhoneycomb

"""
To create nanotube
Consider to use this module: https://docs.scikit-nano.org/
code MATLAB: https://github.com/Armanimani/NanotubeGenerator/blob/master/src/Main.m
"""

### ============================================================================
### Graphene-based Models:
### ============================================================================
def _UnitCell_CNT(m, n, bond_CC=1.421, basis_atom='AB', diameter=None):
	"""Calculates the 3D Cartesian coordinates of atoms of 1 units cell of (n,m) CNT, which which n >= m >= 0
	By Cao Thang Nguyen, Aug 2022

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
	"""
	## Compute coordinates of 1 unit cell of graphene sheet
	R,_,param = _UnitCell_2Dhoneycomb(m, n, bond_CC, basis_atom)
	lC,lT,C,T = param['Chiral_len'], param['Translate_len'], param['Chiral_vector'], param['Translate_vector']
	## Convert the 2D cartesian coordinates to cylindric coordinates of the SWCNT.
	if (m==0) or (m==n):
		if diameter is None:
			raise Exception('For Zigzag or armchair direction, must specify tube-diameter')
	
	r = lC/(2*pi)                       # radius of tube
	theta = dot(R,C)/(lC**2) *(2*pi) 
	x = r*cos(theta)
	y = r*sin(theta)
	z = dot(R,T)/lT
	## save df
	df = pd.DataFrame(data=column_stack((x,y,z)), columns=['x','y','z'], dtype=float)
	param['Diameter'] = 2*r
	## unit box
	vacuum = 20     # vacuum space on XY sides
	unitbox = array([[df['x'].min()-vacuum, df['x'].max()+vacuum], 
					 [df['y'].min()-vacuum, df['y'].max()+vacuum], 
					 [0, lT]], dtype=float)
	return df, unitbox, param


def lattice_CNT(m, n, bond_CC=1.421, aspect=1, basis_atom='AB'):
	"""Calculates the 3D Cartesian coordinates of atoms of of (n,m) CNT.
	By Cao Thang Nguyen, Aug 2022

	Args:
		n,m (int): Chiral indices n>=m>=0
		bond_CC (float): Length of C-C bonds
		aspect (int): The nanotube aspect ratio L/D.
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
	df,unitbox,param = _UnitCell_CNT(m, n, bond_CC, basis_atom)
	lT,D = param['Translate_len'], param['Diameter']
	## Duplicate unit cell
	lenTube = D*aspect
	repZ = int(round(lenTube/lT))            # number of unit cell in Z direction
	if repZ>=2:
		dfold = df.copy()
		for i in range(1,repZ,1):
			dftmp = dfold.copy()
			dftmp['z'] = dftmp['z'] + i*lT
			df = df.append(dftmp, ignore_index=True)

	## remove duplicate points
	df.drop_duplicates(inplace=True, ignore_index=True)
	## compute box periodic
	box = copy(unitbox)
	if repZ>0:
		box[2,1] = box[2,1] + (repZ-1)*lT

	return df, box, param
