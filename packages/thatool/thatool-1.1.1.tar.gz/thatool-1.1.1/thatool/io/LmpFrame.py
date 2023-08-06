# import sys, re, glob, types
# from logging 
# from os import error
# from numpy      import format_float_scientific as formatE

from datetime 	import datetime
import numpy 	as np
import pandas 	as pd
import ele
import copy
from ..model    import wrap_coord_PBC


### Define somes support functions
def _readline_coeff(C, separator='#', firstCol='id'):
	"""Reading the coefficients section

	Args:
		C: list (string)
		separator (str): separator to indetify comment part.

	Returns:
		df (pd.DataFrame): pandas.DataFrame
	"""
	## check leading/trailing of C (reomve leading/trailing empty lines or comment lines)
	if C[0].partition(separator)[0] in ['',' ']:
		C = C[1:]                                 # remove first elem from list
	if C[-1].partition(separator)[0] in ['',' ']:
		C = C[:-1]                                # remove last elem from list
	##
	coeff = [line.partition(separator)[0].split() for line in C]   # list-of-lists (str)
	note  = [line.partition(separator)[-1].strip() for line in C]          # list (str)
	## Create DataFrame
	# cols = ['id'] + ['c'+str(i+1) for i in range(len(coeff[0])-1)]
	cols = [firstCol] + ['c'+str(i+1) for i in range(len(coeff[0])-1)]
	df = pd.DataFrame(data=coeff, columns=cols, dtype=float)       # create df and set type
	df['note'] = note
	return df
#####=======

def _writeline_coeff(df, FMTstr):
	"""Reading the coefficients section

	Args:
		df (pd.DataFrame): df contains data write into list
		FMTstr: string format
		
	Returns:
		L: list (string)
	"""
	note = df['note']  # series
	df.drop(['note'], axis=1, inplace=True)
	mylines = []
	for i,row in df.iterrows():
		line=[("%i" %item) if df.columns[j] in ['id','mol','type','xFlag','yFlag','zFlag']
						   else (FMTstr %item).rstrip('0').rstrip('.')
						   for j,item in enumerate(row.values) ]

		if note[i] not in ['',' ']:
			line.append('\t# '+note[i])

		mylines.append('\t'.join(line))		 # separater.join(list)
	return mylines
#####=======


# Class definition
# =============================================================================
# LAMMPS Frame (single Frame)
# =============================================================================
class LmpFrame():
	"""Create an Object of single-FRAME of LAMMPS (use for both DATA/DUMP files). The docstring is in Google-style.

	This class create a data-object (single configuration) for the analysis of computing data from LAMMPS. The file formats implemented in this class
		- [LAMMPS DATA Format](https://docs.lammps.org/2001/data_format.html)
		- [LAMMPS DUMP Format](https://docs.lammps.org/dump.html)
		- [PDB format](https://ftp.wwpdb.org/pub/pdb/doc/format_descriptions/Format_v33_Letter.pdf)
		- [XYZ format](https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/xyz.html)

		.. image:: https://icme.hpc.msstate.edu/mediawiki/images/e/e7/4kovito.gif

	This class implemented several ways to create `lmpFRAME` object
		- create an empty data object
		- create_DATA object with input data
		- read from DUMP file
		- read from DATA file
		- read frome PDB file

	Args:
		dump_file (str, optional): filename of DUMP file. Defaults to None.
		data_file (str, optional): filename of DATA file. Defaults to None.
		pdb_file (str, optional): filename of PBD file. Defaults to None.
		xyz_file (str, optional): filename of XYZ file. Defaults to None.
		from_df (pd.DataFrame, optional): create FRAME from data. Defaults to None.

	Attributes:
		file_name (str): name of input file
		timestep (int): the timestep of configuration
		box (3x2 np.array): the box size
		box_angle (1x3 np.array): the box angle
		atom (pd.DataFrame) DataFrame of per-atom values
		prop_key (list) column-names of properties
		mass (pd.DataFrame) DataFrame of per-type masses
		FMTstr (str) default format for float numbers, don't use %g because it will lost precision

	Examples:
		```python
		# empty object
		da = io.LmpFrame()
		# oject with input data
		da = io.LmpFrame(from_df=df)
		# from DUMP file
		da = io.LmpFrame(dump_file='test.cfg')
		# from DATA file
		da = io.LmpFrame(data_file='mydata.dat')
		# from PDB file
		da = io.LmpFrame(pdb_file='test.pdb')
		```

	.. _Use chain mutator calls
		https://stackoverflow.com/questions/36484000/use-an-object-method-with-the-initializer-same-line
	"""

	def __init__(self,  dump_file=None,
						data_file=None, atom_style='auto',
						pdb_file=None,
						xyz_file=None,
						from_df=None, 
						box=None, box_angle=None ):
		"""initilize the lmpFRAME object
		Note:
			Use mutator, so do not use self.* when define value
		"""
		# super(LmpFrame, self).__init__()    # does not work

		## Default initial attributes
		self.file_name   = None         # string
		self.timestep    = 0            # int
		self.box 		 = np.asarray([[0,1],[0,1],[0,1]], dtype=float)  # 2d array of float64
		self.box_angle   = np.asarray([0, 0, 0], dtype=float)  		     # 1d array of float64
		self._FMT 	 	 = "%.6f"       # dont use %g, because it will lost precision
		self.prop_key    = None         # list
		self._num		 = {'n_atoms':0, 'n_atom_types':0}    # dict of numbers of sth
		self._style		 = {'atom_style':'', 'pair_style':'', 'bond_style':'', 'angle_style':'', 'dihedral_style':'', 'improper_style':'',}    # dict of numbers of sth

		### Use pd.DataFrame to save data
		## Atoms section
		self.atom        	= None      # DataFrame of per-atom values
		self.mass	     	= None      # DataFrame of per-type values
		## Coeffs section
		self.pair_coeff     = None     # list-of-lists(of float)
		self.bond_coeff     = None     # list-of-lists(of float)
		self.angle_coeff    = None     # list-of-lists(of float)
		self.dihedral_coeff = None
		self.improper_coeff = None
		## cross_coeff Section (class 2)
		self.bondBond_coeff     		= None
		self.bondAngle_coeff    		= None
		self.middleBondTorsion_coeff    = None
		self.endBondTorsion_coeff 		= None
		self.angleTorsion_coeff 		= None
		self.angleAngleTorsion_coeff 	= None
		self.bondBond13_coeff 			= None
		self.angleAngle_coeff 			= None
		## Bonds definition section
		self.bond 		  = None
		self.angle        = None
		self.dihedral     = None
		self.improper     = None

		### generate data
		list_inputs = [dump_file,data_file,pdb_file,xyz_file,from_df]
		if sum([1 for item in list_inputs if item is not None])>1:
			raise ValueError('Only one of {} is choose at a time'.format(list_inputs))

		## read Dumpfile
		if dump_file is not None:
			self.read_DUMP(dump_file)
		## read DataFile
		elif data_file is not None:
			self.read_DATA(data_file, atom_style)
		## read PDB
		elif pdb_file is not None:
			self.read_PDB(pdb_file)
		## read XYZ
		elif xyz_file is not None:
			self.read_XYZ(xyz_file)
		## create FRAME
		elif from_df is not None:
			self.create_DATA(from_df, box, box_angle)
		return
	#####=======


	def create_DATA(self, DataFrame, box=None, box_angle=None):
		"""The method to create new FRAME object with input data.

		Args:
			DataFrame (pd.DataFrame):  of input data
			box (3x2 np.array, optional): option to input boxSize. Defaults to None.
			box_angle (1x3 np.array, optional): option to input box_angle. Defaults to None.

		Returns:
			Obj(LmpFrame): update FRAME

		Examples:
			```python
				da = io.LmpFrame()
				da.create_DATA(DataFrame=df)
				# or
				da = io.LmpFrame(from_df=df)
			```
		"""
		## Save out put to CLASS's attributes
		self.file_name   = 'lammps.dat'
		self.atom     	 = DataFrame   # DataFrame of per-atom values
		self.prop_key    = DataFrame.columns.tolist()
		## update n_dict
		self._num['n_atoms'] = max(pd.unique(self.atom['id']))
		self._num['n_atom_types'] = max(pd.unique(self.atom['type']))

		## Inputs Optional
		if box is not None:
			self.box = box
		if box_angle is not None:
			self.box_angle = box_angle
		###
		return
	#####=======


	def read_DUMP(self, file_name):
		"""The method to create FRAME object by reading DUMP file.

		Args:
			file_name(str): name of input file

		Returns:
			Obj(LmpFrame): update FRAME

		Examples:
			```python
				da = io.LmpFrame()
				da.read_DUMP(DataFrame=df)
				# or
				da = io.LmpFrame(dump_file='mydata.cfg')
			```
		Notes:
			use list comprehension in code to get better performance
		"""
		## Read whole text and break lines
		with open(file_name,'r') as f:
			C = f.read().splitlines()              # a list of strings

		## Extract positions of atoms, and its properties (pd DataFrame)
		## find some text in line --> return line index
		idx_atom = [i for i,line in enumerate(C) if 'ITEM: ATOMS' in line][0]
		## split each line & covert type of 2d_list								## old code: use numpy --> bad performance
		P = [line.split() for line in C[idx_atom+1 :] if line.split()]   	    ##  P = np.char.split( C[index+1 :] ).tolist()   # list-of-lists (2d list)
		df = pd.DataFrame(data=P, dtype=float)                                  ##  P = np.asarray(P1).astype(float)             # convert str to float
		## extract column's name                                                
		myColumn = C[idx_atom].replace('ITEM: ATOMS','').split() 				
		df.columns = myColumn

		## Extract Header lines string(any lines before & included line: "ITEM: ATOMS...")
		H = C[0:idx_atom+1]
		## Extract Box
		index = [i for i,line in enumerate(H) if 'ITEM: BOX' in line][0]    # find index of element
		B = [line.split() for line in H[index+1 : index+4] ]
		B = np.asarray(B, dtype=float)
		# Ortho box
		box = B[:,0:2]
		# Box angle
		if B.shape[1]>2:
			box_angle = np.array([B[0,-1], B[1,-1], B[2,-1]], dtype=float)
		else:
			box_angle = np.array([0, 0, 0], dtype=float)

		## Extract TIMESTEP
		index = [i for i,line in enumerate(H) if 'ITEM: TIMESTEP' in line][0]
		timeStep = float(H[index+1])

		## Save Outputs to CLASS's attributes
		self.file_name    = file_name
		self.timestep     = timeStep
		self.box          = box           # 2d array of float64
		self.box_angle    = box_angle     # 1d array of float64
		self.atom         = df         # DataFrame of per-atom values
		self.prop_key     = df.columns.tolist()
		self._num = {'n_atoms': len(set(df['id'])), 'n_atom_types': len(set(df['type']))}
		return



	def read_DATA(self, file_name, atom_style='auto'):
		"""The method to create FRAME object by reading DATA file.
		The style of atomistic system.The format of "data file" depend on the definition of ["atom_style"](https://lammps.sandia.gov/doc/atom_style.html).
		See [list of atom_style format](https://lammps.sandia.gov/doc/read_data.html#description). Can be detected automatically, or explicitly setting
				- atomic      : atom-ID atom-type x y z
				- charge      : atom-ID atom-type q x y z
				- molecular   : atom-ID molecule-ID atom-type x y z
				- full        : atom-ID molecule-ID atom-type q x y z
		Full [lammps_data format](https://docs.lammps.org/2001/data_format.html)

		Args:
			file_name(str): name of input file
			atom_style(str, optional): option to choose atom_style. Defaults to 'auto'.

		Returns:
			Obj(LmpFrame): update FRAME

		Examples:
			```python
				da = io.LmpFrame(data_file='mydata.dat')
			```

		Notes:
			imgFlag: is auto detected
			```
				np.char.split(C[index]).tolist()              return "object"
				np.char.split(C[index]).tolist()              return list
				np.char.split(C[index1:idx_vel]).tolist()      return list-of-lists (2d list)
			```
		"""
		## Read whole text and break lines
		with open(file_name,'r') as f:
			C = f.read().splitlines()              # a list of strings

		## Extract number of something & detect index of lines
		n_atoms = n_bonds = n_angles = n_dihedrals = n_impropers = 0
		n_atom_types = n_bond_types = n_angle_types = n_dihedral_types = n_improper_types = 0

		idx_Bonds = idx_Angles = idx_Dihedrals = idx_Impropers = None
		idx_Pair_coeff = idx_Bond_coeff = idx_Angle_coeff = idx_Dihedral_coeff = idx_Improper_coeff = None
		idx_BondBond_coeff = idx_BondAngle_coeff = idx_MiddleBondTorsion_coeff = idx_EndBondTorsion_coeff = None
		idx_AngleTorsion_coeff = idx_AngleAngleTorsion_coeff = idx_BondBond13_coeff = idx_AngleAngle_coeff = None

		idx_Velocities = None

		for i,line in enumerate(C):
			if ' atoms' in line: 		n_atoms = int(line.split()[0])
			if ' bonds' in line: 		n_bonds = int(line.split()[0])
			if ' angles' in line: 		n_angles = int(line.split()[0])
			if ' dihedrals' in line: 	n_dihedrals = int(line.split()[0])
			if ' impropers' in line: 	n_impropers = int(line.split()[0])

			if ' atom types' in line: 	n_atom_types = int(line.split()[0])
			if ' bond types' in line: 	n_bond_types = int(line.split()[0])
			if ' angle types' in line: 	n_angle_types = int(line.split()[0])
			if ' dihedral types' in line: n_dihedral_types = int(line.split()[0])
			if ' improper types' in line: n_improper_types = int(line.split()[0])
			## detect index
			if 'xlo xhi' in line:  		idx_box = i
			if 'Masses' in line:  		idx_Masses = i
			if 'Atoms' in line:        	idx_Atoms = i
			if 'Velocities' in line:   	idx_Velocities = i

			if 'Bonds' in line:   	    idx_Bonds = i
			if 'Angles' in line:   	    idx_Angles = i
			if 'Dihedrals' in line:   	idx_Dihedrals = i
			if 'Impropers' in line:   	idx_Impropers = i

			if 'Pair Coeffs' in line:			idx_Pair_coeff = i
			if 'Bond Coeffs' in line:   		idx_Bond_coeff = i
			if 'Angle Coeffs' in line:   		idx_Angle_coeff = i
			if 'Dihedral Coeffs' in line:   	idx_Dihedral_coeff = i
			if 'Improper Coeffs' in line:   	idx_Improper_coeff = i

			if 'BondBond Coeffs' in line:   		idx_BondBond_coeff = i
			if 'BondAngle Coeffs' in line:   		idx_BondAngle_coeff = i
			if 'MiddleBondTorsion Coeffs' in line:  idx_MiddleBondTorsion_coeff = i
			if 'EndBondTorsion Coeffs' in line:   	idx_EndBondTorsion_coeff = i
			if 'AngleTorsion Coeffs' in line:   	idx_AngleTorsion_coeff = i
			if 'AngleAngleTorsion Coeffs' in line:  idx_AngleAngleTorsion_coeff = i
			if 'BondBond13 Coeffs' in line:  		idx_BondBond13_coeff = i
			if 'AngleAngle Coeffs' in line:   		idx_AngleAngle_coeff = i

		## save all number-of-sth to a dict
		_num = {'n_atoms':n_atoms, 'n_bonds':n_bonds, 'n_angles':n_angles, 'n_dihedrals':n_dihedrals, 'n_impropers':n_impropers,
				'n_atom_types':n_atom_types, 'n_bond_types':n_bond_types, 'n_angle_types':n_angle_types, 'n_dihedral_types':n_dihedral_types, 'n_improper_types':n_improper_types}

		if not n_atoms:
			raise Exception('The inpute file {} may have wrong format of LAMMPS-DATA, please check it'.format(file_name))
		#### ===================================================================
		#### Extract atoms properties Section
		#### ===================================================================
		## Extract box & box_angle
		B = [line.split() for line in C[idx_box : idx_box+3] ]
		B = [item[0:2] for item in B]
		self.box   = np.asarray(B, dtype=float)

		Ba = [line.split() for line in C[idx_box+3:idx_box+4] ]
		box_angle = np.asarray( Ba[0][0:3], dtype=float)
		if box_angle.shape[0]>0:
			self.box_angle   = box_angle    # 1d array of float64

		## Extract masses section, atom_symbol
		if n_atoms>0 and idx_Masses:
			newlines = C[idx_Masses+1 : idx_Masses+n_atom_types+2]
			df_mass = _readline_coeff(newlines,'#')

		df_mass.rename(columns={'id':'type', 'c1':'mass', 'note':'atom_symbol'}, inplace=True)
		df_mass['type'] = df_mass['type'].astype(int)
		self.mass = df_mass

		### Atoms section
		## Extract positions of atoms
		if n_atoms>0 and idx_Atoms:
			newlines = C[idx_Atoms+1 : idx_Atoms+n_atoms+2]
			df_atom = _readline_coeff(newlines,'#')
		## Set column names
		if atom_style=='auto':
			atom_style = C[idx_Atoms].partition('#')[-1].split()[-1]
			if atom_style in ['',' ']:
				raise Exception('Cannot recognize atom_style. Please define it using key_word: atom_style="style"')
		if atom_style=='atomic':
			myColumn = ['id','type','x','y','z']
		elif atom_style=='charge':
			myColumn = ['id','type','q','x','y','z']
		elif atom_style=='molecular':
			myColumn = ['id','mol','type','x','y','z']
		elif atom_style=='full':
			myColumn = ['id','mol','type','q','x','y','z']
		else: 
			raise ValueError('atom_style is not support. Just support: atomic, charge, molecular, full')
		## auto dectect imgFlag
		if (df_atom.shape[1]-1)>len(myColumn):
			myColumn.extend(['xFlag','yFlag','zFlag'])

		myColumn.extend(['note'])
		df_atom.columns = myColumn

		### Extract Velocities of atoms
		if n_atoms>0 and idx_Velocities:         # if idx_vel not empty
			newlines = C[idx_Velocities+1 : idx_Velocities+n_atoms+2]
			df_vel = _readline_coeff(newlines,'#')
			df_vel.columns = ['id','vx','vy','vz','note']
			df_atom = pd.concat([df_atom, df_vel[['vx','vy','vz']] ], axis=1)

		## Save out put to CLASS's attributes
		self.file_name   = file_name         # string
		self.atom        = df_atom           # pd.DataFrame of per-atom values
		self.prop_key    = df_atom.columns.tolist()
		self._num		 = _num                         # dict of numbers of sth

		#### ===================================================================
		### Read Coeffs section (if have) and save as list-of-lists(of floats). This is setting parts, that is not easy to modify but must use specific tool depend on forcefield
		#### ===================================================================
		## Coeffs section
		if n_atom_types>0 and idx_Pair_coeff:
			newlines = C[idx_Pair_coeff+1 : idx_Pair_coeff+n_atom_types+2]
			self.pair_coeff = _readline_coeff(newlines,'#','type')                      # pd.DataFrame
			self._style['pair_style'] = C[idx_Pair_coeff].partition('#')[-1]
			self._style['pair_unit'] = C[idx_Pair_coeff+1].partition('#')[-1]

		if n_bond_types>0 and idx_Bond_coeff:
			newlines = C[idx_Bond_coeff+1 : idx_Bond_coeff+n_bond_types+2]
			self.bond_coeff = _readline_coeff(newlines,'#','type')                      # pd.DataFrame
			self._style['bond_style'] = C[idx_Bond_coeff].partition('#')[-1].split()[-1]
			self._style['bond_unit'] = C[idx_Bond_coeff+1].partition('#')[-1]

		if n_angle_types>0 and idx_Angle_coeff:
			newlines = C[idx_Angle_coeff+1 : idx_Angle_coeff+n_angle_types+2]
			self.angle_coeff = _readline_coeff(newlines,'#','type')                      # pd.DataFrame
			self._style['angle_style'] = C[idx_Angle_coeff].partition('#')[-1]
			self._style['angle_unit'] = C[idx_Angle_coeff+1].partition('#')[-1]

		if n_dihedral_types>0 and idx_Dihedral_coeff:
			newlines = C[idx_Dihedral_coeff+1 : idx_Dihedral_coeff+n_dihedral_types+2]
			self.dihedral_coeff = _readline_coeff(newlines,'#','type')                      # pd.DataFrame
			self._style['dihedral_style'] = C[idx_Dihedral_coeff].partition('#')[-1]
			self._style['dihedral_unit'] = C[idx_Dihedral_coeff+1].partition('#')[-1]

		if n_improper_types>0 and idx_Improper_coeff:
			newlines = C[idx_Improper_coeff+1 : idx_Improper_coeff+n_improper_types+2]
			self.improper_coeff = _readline_coeff(newlines,'#','type')                      # pd.DataFrame
			self._style['improper_style'] = C[idx_Improper_coeff].partition('#')[-1]
			self._style['improper_unit'] = C[idx_Improper_coeff+1].partition('#')[-1]

		## cross_coeff Section
		if n_angle_types>0:
			if idx_BondBond_coeff:
				newlines = C[idx_BondBond_coeff+1 : idx_BondBond_coeff+n_angle_types+2]
				self.bondBond_coeff = _readline_coeff(newlines,'#','type')                      # pd.DataFrame
				self._style['bondBond_unit'] = C[idx_BondBond_coeff+1].partition('#')[-1]
			if idx_BondAngle_coeff:
				newlines = C[idx_BondAngle_coeff+1 : idx_BondAngle_coeff+n_angle_types+2]
				self.bondAngle_coeff = _readline_coeff(newlines,'#','type')                      # pd.DataFrame
				self._style['bondAngle_unit'] = C[idx_BondAngle_coeff+1].partition('#')[-1]

		if n_dihedral_types>0:
			if idx_MiddleBondTorsion_coeff:
				newlines = C[idx_MiddleBondTorsion_coeff+1 : idx_MiddleBondTorsion_coeff+n_dihedral_types+2]
				self.middleBondTorsion_coeff = _readline_coeff(newlines,'#','type')                      # pd.DataFrame
				self._style['middleBondTorsion_unit'] = C[idx_MiddleBondTorsion_coeff+1].partition('#')[-1]
			if idx_EndBondTorsion_coeff:
				newlines = C[idx_EndBondTorsion_coeff+1 : idx_EndBondTorsion_coeff+n_dihedral_types+2]
				self.endBondTorsion_coeff = _readline_coeff(newlines,'#','type')                      # pd.DataFrame
				self._style['endBondTorsion_unit'] = C[idx_EndBondTorsion_coeff+1].partition('#')[-1]
			if idx_AngleTorsion_coeff:
				newlines = C[idx_AngleTorsion_coeff+1 : idx_AngleTorsion_coeff+n_dihedral_types+2]
				self.angleTorsion_coeff = _readline_coeff(newlines,'#','type')                      # pd.DataFrame
				self._style['angleTorsion_unit'] = C[idx_AngleTorsion_coeff+1].partition('#')[-1]
			if idx_AngleAngleTorsion_coeff:
				newlines = C[idx_AngleAngleTorsion_coeff+1 : idx_AngleAngleTorsion_coeff+n_dihedral_types+2]
				self.angleAngleTorsion_coeff = _readline_coeff(newlines,'#','type')                      # pd.DataFrame
				self._style['angleAngleTorsion_unit'] = C[idx_AngleAngleTorsion_coeff+1].partition('#')[-1]
			if idx_BondBond13_coeff:
				newlines = C[idx_BondBond13_coeff+1 : idx_BondBond13_coeff+n_dihedral_types+2]
				self.bondBond13_coeff = _readline_coeff(newlines,'#','type')                      # pd.DataFrame
				self._style['bondBond13_unit'] = C[idx_BondBond13_coeff+1].partition('#')[-1]

		if n_improper_types>0:
			if idx_AngleAngle_coeff:
				newlines = C[idx_AngleAngle_coeff+1 : idx_AngleAngle_coeff+n_improper_types+2]
				self.angleAngle_coeff = _readline_coeff(newlines,'#','type')                      # pd.DataFrame
				self._style['angleAngle_unit'] = C[idx_AngleAngle_coeff+1].partition('#')[-1]

		#### ===================================================================
		#### Read Bonds definition section
		#### ===================================================================
		if n_bonds>0 and idx_Bonds:
			newlines = C[idx_Bonds+1 : idx_Bonds+n_bonds+2]
			self.bond = _readline_coeff(newlines,'#')                      # pd.DataFrame
			self.bond.rename(columns = {'c1':'type'}, inplace = True)
		if n_angles>0 and idx_Angles:
			newlines = C[idx_Angles+1 : idx_Angles+n_angles+2]
			self.angle = _readline_coeff(newlines,'#')                      # pd.DataFrame
			self.angle.rename(columns = {'c1':'type'}, inplace = True)
		if n_dihedrals>0 and idx_Dihedrals:
			newlines = C[idx_Dihedrals+1 : idx_Dihedrals+n_dihedrals+2]
			self.dihedral = _readline_coeff(newlines,'#')                      # pd.DataFrame
			self.dihedral.rename(columns = {'c1':'type'}, inplace = True)
		if n_impropers>0 and idx_Impropers:
			newlines = C[idx_Impropers+1 : idx_Impropers+n_impropers+2]
			self.improper = _readline_coeff(newlines,'#')                      # pd.DataFrame
			self.improper.rename(columns = {'c1':'type'}, inplace = True)

		return
	#####=======

	def read_PDB(self, file_name):
		"""The method to create FRAME object by reading PDB file.

		Args:
			file_name(str): name of input file

		Returns:
			Obj(LmpFrame): update FRAME
				record_name(str)
				atom_symbol(str): same as column 'type' in DUMP format
				residue_name(str)
				residue_id(int)
				chain(str)
				occupancy(float)
				beta(float)

		Examples:
			```python
			da = io.LmpFrame(pdb_file='mydata.pdb')
			```
		"""
		## Read whole text and break lines
		with open(file_name,'r') as fileID:
			C = fileID.read().splitlines()              # a list (str)

		## Extract positions of atom
		lines = [line.replace('ATOM','') for line in C if 'ATOM' in line]  # list (str)
		P     = [line.split() for line in lines]                           # list-of-lists (str)
		## extract columns
		myColumn = ['record_name', 'id','atom_symbol','residue_name','chain','residue_id','x','y','z']
		if len(P[0])>9: myColumn = myColumn + ['occupancy']
		if len(P[0])>10: myColumn = myColumn + ['beta']
		## Convert types on some columns of DataFrame
		df = pd.DataFrame(data=P, columns=myColumn, dtype=str)  # create DataFrame
		df[['id','residue_id','x','y','z']] = df[['id','residue_id','x','y','z']].astype(float)
		if 'occupancy' in df.columns: 
			df['occupancy'] = df['occupancy'].astype(float)
		if 'beta' in df.columns: 
			df['beta'] = df['beta'].astype(float)

		## extract box
		box = np.zeros((3, 2), dtype=float)
		box_angle = np.zeros((1, 3), dtype=float)
		B = [line.split() for line in C if "CRYST1" in line]
		if len(B)>0:
			B = [item for item in B[0] if item]
			box[0,1] = float(B[1])
			box[1,1] = float(B[2])
			box[2,1] = float(B[2])
			box_angle[:] = float(B[3]), float(B[4]), float(B[5])

		## Save out put to CLASS's attributes
		self.file_name  = file_name
		self.atom     	= df         # List of DataFrame
		self.box 	   	= box
		self.box_angle  = box_angle
		return
	#####=======


	def read_XYZ(self, file_name):
		"""The method to create FRAME object by reading XYZ file.

		Args:
			file_name(str): name of input file

		Returns:
			Obj(LmpFrame): update FRAME

		Examples:
			```python
			da = io.LmpFrame(pdb_file='mydata.pdb')
			```
		"""
		raise Exception('Not yet implemented')
		return


	def write_DUMP(self, file_name, column=None, FMTstr=None):
		""" The method to write DUMP file.

		Args:
			file_name(str): name of input file
			column(list-of-str, optional): contains columns to be written. Defaults to None, mean all columns will be written
			FMTstr(str, optional): string format for output values. Defaults to None, mean use self._FMT

		Returns:
			file: the DUMP file

		Examples:
			```python
			da.write_DUMP('test.cfg', column=['id','type','x','y','z'], FMTstr='%.4f')
			```
		"""
		## Inputs Compulsory
		df        = self.atom
		box       = self.box
		box_angle = self.box_angle
		## Inputs Optional
		if column==None:
			myColumn = df.columns.tolist()
		if FMTstr==None:
			FMTstr = self._FMT
		df = df[myColumn]

		## Construct header (any lines before & included line: "Atoms ")  (new code use list-of-strings)
		H = ['ITEM: TIMESTEP']                       # 1d list of strings , no need to set dtype='U256'
		H.append(str(int(self.timestep)))
		H.append('ITEM: NUMBER OF ATOMS')          # attach number of atoms
		H.append( str(df.shape[0]) )
		H.append('ITEM: BOX BOUNDS xy xz yz pp pp pp')
		# H.append(formatE(box[0,0],precision=14,unique=False,trim='-') + ' ' + formatE(box[0,1], precision=14,unique=False,trim='-') + ' ' + formatE(box_angle[0], precision=12,unique=False,trim='-'))
		# H.append(formatE(box[1,0],precision=14,unique=False,trim='-') + ' ' + formatE(box[1,1], precision=14,unique=False,trim='-') + ' ' + formatE(box_angle[1], precision=12,unique=False,trim='-'))
		# H.append(formatE(box[2,0],precision=14,unique=False,trim='-') + ' ' + formatE(box[2,1], precision=14,unique=False,trim='-') + ' ' + formatE(box_angle[2], precision=12,unique=False,trim='-'))
		H.append('%.12f %.12f %.12f' % (box[0,0], box[0,1], box_angle[0]) )
		H.append('%.12f %.12f %.12f' % (box[1,0], box[1,1], box_angle[1]) )
		H.append('%.12f %.12f %.12f' % (box[2,0], box[2,1], box_angle[2]) )		
		H.append('ITEM: ATOMS ' + ' '.join(myColumn))

		### Writing Output file
		## write headers
		with open(file_name,'w') as f:
			for line in H:
				f.write(line +'\n')

		## write Dump data
		with open(file_name,'a') as f:
			for i,row in df.iterrows():
				line=[("%s" %item) if isinstance(df[df.columns[j]][0],str)
								   else ("%i" %item) if df.columns[j] in ['id','mol','type']
								   else (FMTstr %item).rstrip('0').rstrip('.')
					               for j,item in enumerate(row.values) ]
				f.write(' '.join(line) +'\n')      # separater.join(list)
		###
		print('Write DUMP, done !')
		return

		# ## write headers
		# with open('test.txt','wb') as fileID:
		# 	np.savetxt(fileID, H, '%s', newline='\n')
		# ## write Dump data
		# fmt = ''
		# for elem in myColumn:
		# 	if elem == 'id' or elem == 'mol' or elem == 'type':   fmt = fmt + '%i  '
		# 	else:                                                 fmt = fmt +FMTstr +' '       # '%.10g '
		# #--
		# with open(file_name,'ab') as fileID:
		# 	np.savetxt(fileID, df[myColumn], fmt=fmt)
	#####=======

	def write_DATA(self, file_name, atom_style='atomic', 
						ignore_vel=False, ignore_imgFlag=False, ignore_pair_coeff=False, 
						comment_line='', FMTstr='%.6f'):
		""" The method to write DATA file. [DATA format](https://docs.lammps.org/2001/data_format.html)

		Args:
			file_name(str): name of input file
			atom_style(str, optional): the style of atomistic system, can be 'atomic', 'charge', 'molecular', 'full' . Defaults to 'atomic'.
			ignore_vel(bool, optional): to write Velocity values. Defaults to False.
			ignore_imgFlag(bool, optional): to write imgFlag tag. Defaults to False.
			comment(str, optional): comment on second line in DATA file. Defaults to ''.
			FMTstr(str, optional): string format for output values. Defaults to None, mean use self._FMT
			ignore_pair_coeff(bool, optional): ignore pair-coeff when write data. Defaults to False.

		Returns:
			file: the DUMP file

		Examples:
			```python
			da.write_DATA('test.dat', atom_style='atomic', ignore_imgFlag=False, ignore_vel=False, FMT='%.4f')
			```
		"""
		## Inputs Compulsory
		_num	         = self._num      # dict
		_style	         = self._style      # dict
		box      		 = self.box
		box_angle 		 = self.box_angle
		df_atom          = self.atom
		df_mass 		 = self.mass              # DataFrame of per-element values
		if df_mass is None:
			raise Exception('Atomic masses are not availabe, please set masses')
		else:
			c = set(pd.unique(df_atom['type'].astype('int'))) - set(df_mass['type'].astype('int'))  # check all items in list A not in list B
			if c: raise Exception('Atomic-masses of types {} are not availabe. Please set it.'.format(c))

		## Inputs Optional
		if FMTstr==None: FMTstr = self._FMT

		#### ===================================================================
		### Write header section
		#### ===================================================================
		## Construct header (any lines before & included line: "Atoms ")    (new code)
		L = ['# LAMMPS data, created by Thang, DATE:' +datetime.now().strftime('%Y-%b-%d %H:%M:%S')]   # 1d list of strings
		L.append(comment_line)
		## write number-of-something
		list1 = ['n_atoms','n_bonds','n_angles','n_dihedrals','n_impropers','n_atom_types','n_bond_types', 'n_angle_types', 'n_dihedral_types', 'n_improper_types']
		list2 = ['atoms','bonds','angles','dihedrals','impropers','atom types','bond types','angle types','dihedral types','improper types']
		for i,(item1,item2) in enumerate(zip(list1, list2)):
			if (item1 in _num.keys()) and _num[item1]>0:
				L.append(str(int(_num[item1])) +' ' +item2)

		## Box section
		L.append(' ')
		L.append('%.12f %.12f xlo xhi' %(box[0,0], box[0,1]) )
		L.append('%.12f %.12f ylo yhi' %(box[1,0], box[1,1]) )
		L.append('%.12f %.12f zlo zhi' %(box[2,0], box[2,1]) )
		if np.any(box_angle):
			L.append('%.12f %.12f %.12f xy xz yz' %(box_angle[0], box_angle[1], box_angle[2]) )

		## Masses section
		L.extend([' ','Masses',' '])    # append just add 1 elem to list, extend add list to list
		for i,row in df_mass.iterrows():
			L.append("\t".join([str(row['type']), str(row['mass']), '#', row['atom_symbol']]))

		#### ===================================================================
		### Write Coeffs section (if have)
		#### ===================================================================
		## Coeffs section
		if (self.pair_coeff is not None) and (ignore_pair_coeff==False):
			L.extend([' ', 'Pair Coeffs # ' +_style['pair_style'] ,'# '+_style['pair_unit'] ])
			lines = _writeline_coeff(self.pair_coeff, FMTstr)
			L.extend(lines)
		if self.bond_coeff is not None:
			L.extend([' ', 'Bond Coeffs # ' +_style['bond_style'] ,'# '+_style['bond_unit'] ])
			lines = _writeline_coeff(self.bond_coeff, FMTstr)
			L.extend(lines)
		if self.angle_coeff is not None:
			L.extend([' ', 'Angle Coeffs # ' +_style['angle_style'] ,'# '+_style['angle_unit'] ])
			lines = _writeline_coeff(self.angle_coeff, FMTstr)
			L.extend(lines)
		if self.dihedral_coeff is not None:
			L.extend([' ', 'Dihedral Coeffs # ' +_style['dihedral_style'] ,'# '+_style['dihedral_unit'] ])
			lines = _writeline_coeff(self.dihedral_coeff, FMTstr)
			L.extend(lines)
		if self.improper_coeff is not None:
			L.extend([' ', 'Improper Coeffs # ' +_style['improper_style'] ,'# '+_style['improper_unit'] ])
			lines = _writeline_coeff(self.improper_coeff, FMTstr)
			L.extend(lines)

		## cross_coeff Section
		if self.bondBond_coeff is not None:
			L.extend([' ', 'BondBond Coeffs', '# '+_style['bondBond_unit'] ])
			lines = _writeline_coeff(self.bondBond_coeff, FMTstr)
			L.extend(lines)
		if self.bondAngle_coeff is not None:
			L.extend([' ', 'BondAngle Coeffs Coeffs', '# '+_style['bondAngle_unit'] ])
			lines = _writeline_coeff(self.bondAngle_coeff, FMTstr)
			L.extend(lines)
		if self.middleBondTorsion_coeff is not None:
			L.extend([' ', 'MiddleBondTorsion Coeffs', '# '+_style['middleBondTorsion_unit'] ])
			lines = _writeline_coeff(self.middleBondTorsion_coeff, FMTstr)
			L.extend(lines)
		if self.endBondTorsion_coeff is not None:
			L.extend([' ', 'EndBondTorsion Coeffs', '# '+_style['endBondTorsion_unit'] ])
			lines = _writeline_coeff(self.endBondTorsion_coeff, FMTstr)
			L.extend(lines)
		if self.angleTorsion_coeff is not None:
			L.extend([' ', 'AngleTorsion Coeffs', '# '+_style['angleTorsion_unit'] ])
			lines = _writeline_coeff(self.angleTorsion_coeff, FMTstr)
			L.extend(lines)
		if self.angleAngleTorsion_coeff is not None:
			L.extend([' ', 'AngleAngleTorsion Coeffs', '# '+_style['angleAngleTorsion_unit'] ])
			lines = _writeline_coeff(self.angleAngleTorsion_coeff, FMTstr)
			L.extend(lines)
		if self.bondBond13_coeff is not None:
			L.extend([' ', 'BondBond13 Coeffs', '# '+_style['bondBond13_unit'] ])
			lines = _writeline_coeff(self.bondBond13_coeff, FMTstr)
			L.extend(lines)
		if self.angleAngle_coeff is not None:
			L.extend([' ', 'AngleAngle Coeffs', '# '+_style['angleAngle_unit'] ])
			lines = _writeline_coeff(self.angleAngle_coeff, FMTstr)
			L.extend(lines)
		## write to file
		with open(file_name,'w') as f:
			for line in L:
				f.write(line +'\n')

		#### ===================================================================
		### Write Atoms section
		#### ===================================================================
		## write Position
		if atom_style=='atomic':    myColumn = ['id','type']
		if atom_style=='charge':    myColumn = ['id','type','q']
		if atom_style=='molecular': myColumn = ['id','mol','type']
		if atom_style=='full':      myColumn = ['id','mol','type','q']
		##
		lis = self.atom.columns.tolist()
		if 'x' in lis: myColumn.extend(['x'])
		if 'y' in lis: myColumn.extend(['y'])
		if 'z' in lis: myColumn.extend(['z'])
		if 'xu' in lis: myColumn.extend(['xu'])
		if 'yu' in lis: myColumn.extend(['yu'])
		if 'zu' in lis: myColumn.extend(['zu'])
		if ignore_imgFlag==False: myColumn.extend(['xFlag','yFlag','zFlag'])
		##
		df = self.atom[myColumn]
		L = [' ', 'Atoms # '+atom_style ,' ']
		for i,row in df.iterrows():
			line=[("%i"%item) if df.columns[j] in ['id','mol','type','xFlag','yFlag','zFlag']
							else (FMTstr%item).rstrip('0').rstrip('.')
							for j,item in enumerate(row.values) ]
			# if self.atom['note'][i] not in ['',' ']:
			# 	line.append('\t# '+self.atom['note'][i] )

			L.append('\t'.join(line))		 # separater.join(list)
			# line=''
			# for j,item in enumerate(row.values):
			# 	if df.columns[j] in ['id','mol','type','xFlag','yFlag','zFlag']:
			# 		line = line + ("%i " %item)
			# 	else: line = line + ((FMTstr %item).rstrip('0').rstrip('.') +' ')

		with open(file_name,'a') as f:
			for line in L:
				f.write(line +'\n')

		## write Velocity
		if ignore_vel==False:
			df_vel = self.atom[['id','vx','vy','vz']]
			L = [' ', 'Velocities' ,' ']
			for i,row in df_vel.iterrows():
				line=[("%i"%item) if df_vel.columns[j] in ['id']
								else (FMTstr%item).rstrip('0').rstrip('.')
								for j,item in enumerate(row.values) ]
				L.append('\t'.join(line))		 # separater.join(list)
			##
			with open(file_name,'a') as f:
				for line in L:
					f.write(line +'\n')

		#### ===================================================================
		### Write Bonds definition section
		#### ===================================================================
		L = []
		if self.bond is not None:
			L.extend([' ', 'Bonds', ' '])
			lines = _writeline_coeff(self.bond, FMTstr)
			L.extend(lines)
		if self.angle is not None:
			L.extend([' ', 'Angles', ' '])
			lines = _writeline_coeff(self.angle, FMTstr)
			L.extend(lines)
		if self.dihedral is not None:
			L.extend([' ', 'Dihedrals', ' '])
			lines = _writeline_coeff(self.dihedral, FMTstr)
			L.extend(lines)
		if self.improper is not None:
			L.extend([' ', 'Impropers', ' '])
			lines = _writeline_coeff(self.improper, FMTstr)
			L.extend(lines)
		##
		with open(file_name,'a') as f:
			for line in L:
				f.write(line +'\n')
		###
		# print('Write DATA, {:d} atoms, done! Remmember to set atomic MASSes explicitly! https://tinyurl.com/yzv2namz'.format(df.shape[0]))
		print('Write DATA, {:d} atoms, done!'.format(df.shape[0]))
		return
	#####=======


	def write_XYZ(self, file_name, column=['X','xu','yu','zu'], FMTstr=None):
		""" The `method` to write XYZ file.

		Args:
			file_name(str): name of input file
			column(list-of-str, optional): contains columns to be written. Defaults to ['X','xu','yu','zu']
			FMTstr(str, optional): string format for output values. Defaults to None, mean use self._FMT

		Returns:
			file: the XYZ file

		Examples:
			```python
			da.write_XYZ('test.xyz')
			```
		"""
		## Inputs Compulsory
		df = self.atom
		## Inputs Optional
		if FMTstr==None:
			FMTstr = self._FMT

		## Writing to file
		## header
		H = ['Atoms. Timestep: 0']
		with open(file_name,'w') as f:
			for line in H:
				f.write(line +'\n')
		## position XYZ
		myColumn = ['type']
		lis = df.columns.tolist()
		if 'x' in lis: myColumn.extend(['x'])
		if 'y' in lis: myColumn.extend(['y'])
		if 'z' in lis: myColumn.extend(['z'])
		if 'xu' in lis: myColumn.extend(['xu'])
		if 'yu' in lis: myColumn.extend(['yu'])
		if 'zu' in lis: myColumn.extend(['zu'])
		#--
		df = df[myColumn]
		## write
		with open(file_name,'a') as f:
			for i,row in df.iterrows():
				line=[("%i"%item) if df.columns[j] in ['id','mol','type']
								else (FMTstr%item).rstrip('0').rstrip('.')
					            for j,item in enumerate(row.values) ]
				f.write(' '.join(line) +'\n')      # separater.join(list)
		##--
		print('Write XYZ, done !')
		return
	#####=======

	def write_PDB(self, file_name, writeBox=False):
		""" The method to write [PDB file](https://zhanggroup.org/SSIPe/pdb_atom_format.html)

		Args:
			file_name(str): name of input file
			writeBox(bool, optional): write box or not. Defaults to False.

		Returns:
			file: the PDB file

		Examples:
			```python
			da.write_PDB('test.pdb')
			```
		"""
		## specific which data to write
		df       = self.atom
		box      = self.box
		box_angle = self.box_angle

		## add column for PDB format
		if 'record_name' not in df.columns.tolist():
			df['record_name'] = ['ATOM']*df.shape[0]
		else: pass

		if 'atom_symbol' not in df.columns.tolist():
			if 'type' in df.columns.tolist():
				df['atom_symbol'] = df['type'].astype(int)
			else: df['atom_symbol'] = ['X']*df.shape[0]

		if 'residue_name' not in df.columns.tolist():
			df['residue_name'] = ['XX']*df.shape[0]
		else: pass

		if 'residue_id' not in df.columns.tolist():
			df['residue_id'] = [1]*df.shape[0]
		else: pass

		if 'chain' not in df.columns.tolist():
			df['chain'] = ['L']*df.shape[0]
		else: pass

		if 'occupancy' not in df.columns.tolist():
			df['occupancy'] = [0]*df.shape[0]
		else: pass

		if 'beta' not in df.columns.tolist():
			df['beta'] = [0]*df.shape[0]
		else: pass

		if 'segment_name' not in df.columns.tolist():
			df['segment_name'] = ['THA']*df.shape[0]
		else: pass

		if 'element_sym' not in df.columns.tolist():
			df['element_sym'] = ['X']*df.shape[0]
		else: pass

		## specific columns to be written
		if 'x' not in df.columns.tolist():
			myColumn = ['record_name','id','atom_symbol','residue_name','chain','residue_id', 'xu','yu','zu','occupancy','beta','segment_name','element_sym']
		else: myColumn = ['record_name','id','atom_symbol','residue_name','chain','residue_id', 'x','y','z','occupancy','beta','segment_name','element_sym']
		df = df[myColumn]

		## Construct header (any lines before & included line: "Atoms ")  (new code use list-of-strings)
		H = ['HEADER    PDB reference structure created by Thang ' +datetime.now().strftime('%Y-%b-%d %H:%M:%S')]    # 1d list of strings

		### Writing Output file
		## write headers
		with open(file_name,'w') as f:
			for line in H:
				f.write(line +'\n')

		## write Box: http://www.wwpdb.org/documentation/file-format-content/format33/sect8.html#CRYST1
		if writeBox:
			ang1,ang2,ang3 = 90,90,90
			sGroup = 'P 1'
			Zvalue = 1
			FMTstr = "%-6s %-9g %-9g %-9g %-7g %-7g %-7g %-11s %-4i \n"
			with open(file_name,'a') as f:
				f.write(FMTstr % ("CRYST1", box[0,1],box[1,1],box[2,1], ang1,ang2,ang3, sGroup,Zvalue))

		## write Atom coordinates
		fmt = ""
		for item in myColumn:
			if item=='record_name': 	fmt = fmt +"%-6s "
			if item=='id': 				fmt = fmt +"%-5i "
			if item=='atom_symbol': 		fmt = fmt +"%-5s "
			if item=='residue_name': 	fmt = fmt +"%-3s "
			if item=='chain': 			fmt = fmt +"%-1s "
			if item=='residue_id': 	fmt = fmt +"%-4i "
			if item in ['x','y','z','xu','yu','zu']: fmt = fmt +"%-8g "
			if item=='occupancy': 		fmt = fmt +"%-6g "
			if item=='beta': 			fmt = fmt +"%-6g "
			if item=='segment_name':    fmt = fmt +"%-4s "
			if item=='element_sym':     fmt = fmt +"%-2s "
		##
		with open(file_name,'a') as f:
			for i,row in df.iterrows():
				f.write( (fmt+"\n") % tuple(row.values) )
			f.write( 'END')
		###
		print('Write PDB, done !')
		return
	#####=======


	def add_column(self, data, newColumn=None, replace=False):
		""" The method to add new columns to da.atom.

		Args:
			data(pd.DataFrame, pd.Series, list): Nxm data of new columns
			newColumn(list): 1xN list contains names of columns. Default to None, mean it will take columnNames from DataFrame
			replace(bool, optional): replace column if existed. Defaults to False.

		Returns:
			Obj(LmpFrame): Update da.atom

		Examples:
			```python
			da.add_column(df, myColumn=['col1','col2'], replace=True)
			```
		"""
		## Inputs Compulsory
		if isinstance(data, pd.DataFrame): newdf = data
		if isinstance(data, pd.Series):    newdf = data.to_frame()
		if isinstance(data, list):         newdf = pd.DataFrame(data)
		if isinstance(data, np.ndarray):   newdf = pd.DataFrame(list(data))

		### ==========================================
		### Add columns/column
		### ==========================================
		olddf  = self.atom
		## If exist columns
		if newColumn==None:
			newColumn = newdf.columns.tolist()
		oldColumn = olddf.columns.tolist()
		existCols = [elem for elem in newColumn if elem in oldColumn]     # find intersect list
		if existCols:
			if replace==True:
				olddf.drop(columns=existCols, inplace=True)        # delete columns in olddf. If inplace=False, must return a copy olddr=olddf.drop()
				newdf.columns = newColumn
			else:
				newColChange = [elem+'1' if elem in existCols else elem for elem in newColumn] # change name in newColumn to avoid duplicate name
				newdf.columns = newColChange
		else:
			newdf.columns = newColumn

		self.atom = pd.concat([olddf, newdf], axis=1)
		return
	#####=======

	def delete_column(self, delColumns):
		""" The method to delete columns from da.atom.

		Args:
			data(pd.DataFrame, pd.Series, list): Nxm data of new columns
			delColumns (list): 1xN list contains names of columns to be deleted.

		Returns:
			Obj(LmpFrame): Update da.atom

		Examples:
			```python
			da.delete_column(delColumns=['col1','col2'])
			```
		"""
		for elem in delColumns:
			if elem in self.atom.columns.tolist():
				self.atom.drop(columns=elem, inplace=True)        # delete columns in olddf
		return
	#####=======

	def set_mass(self, element_dict):
		""" The method to set masses of atoms in system. Before use it, need to define element_dict with 2 keys: 'type', 'atom_symbol'
			element_dict={'type': list_values, 'atom_symbol':list_values}

		Args:
			element_dict(dict): a dict to define atom-types and atom-symbols.

		Returns:
			Obj(LmpFrame): Update da.atom

		Examples:
			```python
			da.set_mass(element_dict={'type':[1,2,3], 'atom_symbol':['C','H','N']})
			```
		"""
		## Inputs
		df_mass = self.mass
		c = set(element_dict['type']) - set(pd.unique(self.atom['type']))   # check all items in list A not in list B
		if c: raise Exception('Atom-types {} are not in system'.format(c))
		##
		new_mass = [ele.element_from_symbol(elem).mass for elem in element_dict['atom_symbol']]
		element_dict['mass'] = new_mass
		df = pd.DataFrame.from_dict(element_dict)

		if df_mass is None:
			df_mass = df
		else:
			df_mass.drop(df_mass[df_mass['type'].isin(df['type'])].index, inplace=True)
			df_mass = pd.concat([df_mass, df], axis=0)

		## Output
		self.mass = df_mass.sort_values(['type'])
		return
	#####=======

	def combine_frame(self, LmpFrame,
							merge_type=False,
							alignment='comXYZ',  #   'comXYZ'   'minXYZ'  'maxXYZ'
							shift_XYZ=None,   # [0,0,0]
							separate_XYZ=None,   # [0,0,0]
							merge_box=True,
							use_box='box1'  ):     # 'box1' or 'box2' only use when merge_box=False
		"""The method to combine 2 Lammps Frames.

		Args:
			LmpFrame (LmpFrame Obj): an Object of LmpFrame
			merge_type (bool, optional): merge the same type in 2 LmpFrame. Defaults to False.
			alignment (str, optional): choose how to align 2 frame. Defaults to 'comXYZ'.
				+ 'comXYZ': align based on COM
				+ 'minXYZ': align based on left corner
				+ 'maxXYZ': align based on right corner
			shift_XYZ (list, optional): shift a distance from COM aligment. Defaults to [0,0,0].
			separate_XYZ (list, optional): Separate 2 frame with a specific value. Defaults to [0,0,0].
			merge_box (bool, optional): choose to merge box or not. Defaults to True.
			use_box (str, optional): be used as the box size if merge_box=False. Defaults to 'box1'.

		Return:
		 	Update LmpFrame da1

		Usage:
			```python
			da1.combine_frame(da2)
			```

		TO DO:
			combine box_angle

		Refs:
			Deep copy: https://stackoverflow.com/questions/3975376/understanding-dict-copy-shallow-or-deep/3975388#3975388
		"""
		## Inputs
		da1 = self
		da2 = copy.deepcopy(LmpFrame)        # use copy to avoid un-expected changes in LmpFrame

		## detect atom_style of da2 (to ensure consistence with da1)
		#### ===================================================================
		#### autofill missing data
		#### ===================================================================
		## detect cols in da1 but not in da2
		for item in da1.atom.columns.to_list():
			if item not in da2.atom.columns.to_list():
				if item=='x':
					da2.atom[item] = da2.atom['xu'].values
				if item=='y':
					da2.atom[item] = da2.atom['yu']
				if item=='z':
					da2.atom[item] = da2.atom['zu']

				if item=='mol':
					da2.atom[item] = 1

				if item in ['vx','vy','vz','xFlag','yFlag','zFlag']:
					da2.atom[item] = 0

		## detect cols in da2 but not in da2
		for item in da2.atom.columns.to_list():
			if item not in da1.atom.columns.to_list():
				if item=='x':
					da1.atom[item] = da1.atom['xu']
				if item=='y':
					da1.atom[item] = da1.atom['yu']
				if item=='z':
					da1.atom[item] = da1.atom['zu']

				if item in ['vx','vy','vz','xFlag','yFlag','zFlag']:
					da1.atom[item] = 0


		#### ===================================================================
		#### Alignment (Shift position of da2)
		#### ===================================================================
		## Alignment
		if alignment=='comXYZ':
			com_da1 = da1.box.mean(axis=1)
			com_da2 = da2.box.mean(axis=1)
			bias = com_da1 - com_da2
		elif alignment=='minXYZ':
			min_da1 = da1.box[:,0]
			min_da2 = da2.box[:,0]
			bias = min_da1 - min_da2
		elif alignment=='maxXYZ':
			max_da1 = da1.box[:,1]
			max_da2 = da2.box[:,1]
			bias = max_da1 - max_da2
		else:
			raise ValueError("Support alignment types are: 'comXYZ', 'minXYZ', 'maxXYZ' ")
		##
		da2.atom['x'] = da2.atom['x'] + bias[0]
		da2.atom['y'] = da2.atom['y'] + bias[1]
		da2.atom['z'] = da2.atom['z'] + bias[2]
		da2.box[0,:] = da2.box[0,:] + bias[0]
		da2.box[1,:] = da2.box[1,:] + bias[1]
		da2.box[2,:] = da2.box[2,:] + bias[2]

		## Shift distance
		if shift_XYZ is not None:  # [0,0,0]
			da2.atom['x'] = da2.atom['x'] + shift_XYZ[0]
			da2.atom['y'] = da2.atom['y'] + shift_XYZ[1]
			da2.atom['z'] = da2.atom['z'] + shift_XYZ[2]
			da2.box[0,:] = da2.box[0,:] + shift_XYZ[0]
			da2.box[1,:] = da2.box[1,:] + shift_XYZ[1]
			da2.box[2,:] = da2.box[2,:] + shift_XYZ[2]

		## Separate distance
		if separate_XYZ is not None:  # [0,0,0]
			## on X-direction
			if separate_XYZ[0]<0:
				bias = da2.atom['x'].max()-da1.atom['x'].min()
				if bias>0: bias = -bias
			elif separate_XYZ[0]>0:
				bias = da2.atom['x'].min()-da1.atom['x'].max()
				if bias<0: bias = -bias
			else:
				bias = 0
			da2.atom['x'] = da2.atom['x'] + separate_XYZ[0] + bias
			da2.box[0,:] = da2.box[0,:] + separate_XYZ[0] + bias

			## on Y-direction
			if separate_XYZ[1]<0:
				bias = da2.atom['y'].max()-da1.atom['y'].min()
				if bias>0: bias = -bias
			elif separate_XYZ[1]>0:
				bias = da2.atom['y'].min()-da1.atom['y'].max()
				if bias<0: bias = -bias
			else:
				bias = 0
			da2.atom['y'] = da2.atom['y'] + separate_XYZ[1] + bias
			da2.box[1,:] = da2.box[1,:] + separate_XYZ[1] + bias

			## on Z-direction
			if separate_XYZ[2]<0:
				bias = da2.atom['z'].max()-da1.atom['z'].min()
				if bias>0: bias = -bias
			elif separate_XYZ[2]>0:
				bias = da2.atom['z'].min()-da1.atom['z'].max()
				if bias<0: bias = -bias
			else:
				bias = 0
			da2.atom['z'] = da2.atom['z'] + separate_XYZ[2] + bias
			da2.box[2,:] = da2.box[2,:] + separate_XYZ[2] + bias

		#### ===================================================================
		#### Combination Atom_section
		#### ===================================================================
		def _combine_id_df2(df1, df2):
			df2['id']   = df2['id'].astype('int') + max(df1['id'].astype('int'))
			if 'mol' in df1.columns.tolist():
				df2['mol'] = df2['mol'] + df1['mol'].max()
			return df2

		def _combine_type_df2(df1, df2, merge_type):
			if merge_type==False:
				df2['type'] = df2['type'].astype('int') + max(df1['type'].astype('int'))
			return df2

		def _combine_bond_df2(df2, OLD_N_ATOMS):
			"""used to combine bonds definitions"""
			df_keep = df2[['id','type','note']]
			df2.drop(['id','type','note'], axis=1, inplace=True)
			df2 += OLD_N_ATOMS
			df2_new = pd.concat([df_keep,df2], axis=1)
			return df2_new

		## combine Atoms
		df1 = da1.atom.copy()    # use copy to avoid change in original
		df2 = da2.atom.copy()
		OLD_N_ATOMS = df1.shape[0]
		df2 = _combine_id_df2(df1, df2)
		df2 = _combine_type_df2(df1, df2, merge_type)

		self.atom = pd.concat([df1,df2], axis=0, ignore_index=True)
		## update number_atom
		self._num['n_atoms'] = self.atom.shape[0]
		self._num['n_atom_types'] = pd.unique(self.atom['type']).shape[0]

		## combine Masses_section
		df1 = da1.mass.copy()
		df2 = da2.mass.copy()
		if df2 is None:
			raise Exception("da2.mass is empty, please set it")

		df2 = _combine_type_df2(df1, df2, merge_type)
		self.mass = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		## combine box (Note: cannot combine box_angle so far)
		box1 = da1.box.copy()
		box2 = da2.box.copy()
		if merge_box==True:
			box = np.asarray([[0,0],[0,0],[0,0]]).astype(float)   # must set type float
			box[0,0], box[1,0], box[2,0] = min(box1[0,0],box2[0,0]), min(box1[1,0],box2[1,0]), min(box1[2,0],box2[2,0])
			box[0,1], box[1,1], box[2,1] = max(box1[0,1],box2[0,1]), max(box1[1,1],box2[1,1]), max(box1[2,1],box2[2,1])
			self.box = box
		elif use_box=='box1':
			self.box = box1
		elif use_box=='box2':
			self.box = box2

		#### ===================================================================
		### Combine Bonds definition section
		#### ===================================================================
		## Combine bond
		if da2.bond is not None:
			df1 = da1.bond.copy()
			df2 = da2.bond.copy()
			df2 = _combine_id_df2(df1, df2)
			df2 = _combine_type_df2(df1, df2, merge_type)
			df2 = _combine_bond_df2(df2, OLD_N_ATOMS)
			self.bond = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

			self._num['n_bonds'] = self.bond.shape[0]
			self._num['n_bond_types'] = pd.unique(self.bond['type']).shape[0]
		## Combine angle
		if da2.angle is not None:
			df1 = da1.angle.copy()
			df2 = da2.angle.copy()
			df2 = _combine_id_df2(df1, df2)
			df2 = _combine_type_df2(df1, df2, merge_type)
			df2 = _combine_bond_df2(df2, OLD_N_ATOMS)
			self.angle = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

			self._num['n_angles'] = self.angle.shape[0]
			self._num['n_angle_types'] = pd.unique(self.angle['type']).shape[0]
		## Combine dihedral
		if da2.dihedral is not None:
			df1 = da1.dihedral.copy()
			df2 = da2.dihedral.copy()
			df2 = _combine_id_df2(df1, df2)
			df2 = _combine_type_df2(df1, df2, merge_type)
			df2 = _combine_bond_df2(df2, OLD_N_ATOMS)
			self.dihedral = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

			self._num['n_dihedrals'] = self.dihedral.shape[0]
			self._num['n_dihedral_types'] = pd.unique(self.dihedral['type']).shape[0]
		## Combine improper
		if da2.improper is not None:
			df1 = da1.improper.copy()
			df2 = da2.improper.copy()
			df2 = _combine_id_df2(df1, df2)
			df2 = _combine_type_df2(df1, df2, merge_type)
			df2 = _combine_bond_df2(df2, OLD_N_ATOMS)
			self.improper = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

			self._num['n_impropers'] = self.improper.shape[0]
			self._num['n_improper_types'] = pd.unique(self.improper['type']).shape[0]

		#### ===================================================================
		### Combine Coeffs section
		#### ===================================================================
		## Combine pair_coeff
		if da2.pair_coeff is not None:
			df1 = da1.pair_coeff.copy()
			df2 = da2.pair_coeff.copy()
			df2 = _combine_type_df2(df1, df2, merge_type)
			self.pair_coeff = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		## Combine bond_coeff
		if da2.bond_coeff is not None:
			df1 = da1.bond_coeff.copy()
			df2 = da2.bond_coeff.copy()
			df2 = _combine_type_df2(df1, df2, merge_type)
			self.bond_coeff = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		## Combine angle_coeff
		if da2.angle_coeff is not None:
			df1 = da1.angle_coeff.copy()
			df2 = da2.angle_coeff.copy()
			df2 = _combine_type_df2(df1, df2, merge_type)
			self.angle_coeff = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		if da2.dihedral_coeff is not None:
			df1 = da1.dihedral_coeff.copy()
			df2 = da2.dihedral_coeff.copy()
			df2 = _combine_type_df2(df1, df2, merge_type)
			self.dihedral_coeff = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		if da2.improper_coeff is not None:
			df1 = da1.improper_coeff.copy()
			df2 = da2.improper_coeff.copy()
			df2 = _combine_type_df2(df1, df2, merge_type)
			self.improper_coeff = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		if da2.bondBond_coeff is not None:
			df1 = da1.bondBond_coeff.copy()
			df2 = da2.bondBond_coeff.copy()
			df2 = _combine_type_df2(df1, df2, merge_type)
			self.bondBond_coeff = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		if da2.bondAngle_coeff is not None:
			df1 = da1.bondAngle_coeff.copy()
			df2 = da2.bondAngle_coeff.copy()
			df2 = _combine_type_df2(df1, df2, merge_type)
			self.bondAngle_coeff = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		if da2.middleBondTorsion_coeff is not None:
			df1 = da1.middleBondTorsion_coeff.copy()
			df2 = da2.middleBondTorsion_coeff.copy()
			df2 = _combine_type_df2(df1, df2, merge_type)
			self.middleBondTorsion_coeff = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		if da2.endBondTorsion_coeff is not None:
			df1 = da1.endBondTorsion_coeff.copy()
			df2 = da2.endBondTorsion_coeff.copy()
			df2 = _combine_type_df2(df1, df2, merge_type)
			self.endBondTorsion_coeff = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		if da2.angleTorsion_coeff is not None:
			df1 = da1.angleTorsion_coeff.copy()
			df2 = da2.angleTorsion_coeff.copy()
			df2 = _combine_type_df2(df1, df2, merge_type)
			self.angleTorsion_coeff = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		if da2.angleAngleTorsion_coeff is not None:
			df1 = da1.angleAngleTorsion_coeff.copy()
			df2 = da2.angleAngleTorsion_coeff.copy()
			df2 = _combine_type_df2(df1, df2, merge_type)
			self.angleAngleTorsion_coeff = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		if da2.bondBond13_coeff is not None:
			df1 = da1.bondBond13_coeff.copy()
			df2 = da2.bondBond13_coeff.copy()
			df2 = _combine_type_df2(df1, df2, merge_type)
			self.bondBond13_coeff = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		if da2.angleAngle_coeff is not None:
			df1 = da1.angleAngle_coeff.copy()
			df2 = da2.angleAngle_coeff.copy()
			df2 = _combine_type_df2(df1, df2, merge_type)
			self.angleAngle_coeff = pd.concat([df1,df2], axis=0, ignore_index=True).drop_duplicates()

		return
	#####=======


	def unwrap_coord_DATA(self, imgFlag=['x','y','z'], atom_types=[]):
		"""The method to upwrap coords in DATA file.

		Args:
			imgFlag (list, optional): image Flags in data file. Defaults to ['x','y','z'].
			atom_types (list, optional): just unwrap some atom-types. Defaults to [], mean unwrap all-types.

		Returns:
			Obj(LmpFrame): update FRAME

		Notes:
			cannot unwrap_coord_data if imgFlags are not available.
		"""

		## Inputs
		box = self.box
		df = self.atom
		if atom_types:
			df = df[df['type'].isin(atom_types)]

		if (set(imgFlag) - set(df.columns.tolist())):
			raise Exception('Periodic image Flags are not found in data file.')

		for i,item in enumerate(imgFlag):
			if item=='x':
				df['x'] = df['x'] + (box[0,1]-box[0,0]) *df['xFlag']
				df['xFlag'] = 0
			if item=='y':
				df['y'] = df['y'] + (box[1,1]-box[1,0]) *df['yFlag']
				df['yFlag'] = 0
			if item=='z':
				df['z'] = df['z'] + (box[2,1]-box[2,0]) *df['zFlag']
				df['zFlag'] = 0

		## Save output
		self.atom.loc[self.atom['id'].isin(df['id']), ['x','y','z','xFlag','yFlag','zFlag']] = df[['x','y','z','xFlag','yFlag','zFlag']]
		return


	def flip_coords(self, dim=[1,1,1]):
		"""The method to flip coords over the center.

		Args:
			dim (list, optional): choose the dimenstion to take flip. Defaults to [1,1,1].

		Returns:
			Obj(LmpFrame): update FRAME

		TODOs:
			Remove pandas Warning.
		"""
		## Inputs
		box = self.box
		df = self.atom[['x','y','z']]
		if dim[0]==1:
			old_min = df['x'].min()
			mean = df['x'].mean()
			tmp1 = df[df['x']>=mean]['x']
			tmp2 = df[df['x']<=mean]['x']
			df.loc[tmp1.index, 'x'] = tmp1 - 2*(tmp1 - mean)  # this line cause message
			df.loc[tmp2.index, 'x'] = tmp2 - 2*(tmp2 - mean)
			## update box
			new_min = df['x'].min()
			if (new_min-old_min)>0: bias = -(new_min-old_min)
			else: bias = (new_min-old_min)
			box[0,:] = box[0,:] + bias

		if dim[1]==1:
			old_min = df['y'].min()
			mean = df['y'].mean()
			tmp1 = df[df['y']>=mean]['y']
			tmp2 = df[df['y']<=mean]['y']
			df.loc[tmp1.index, 'y'] = tmp1 - 2*(tmp1 - mean)
			df.loc[tmp2.index, 'y'] = tmp2 - 2*(tmp2 - mean)
			## update box
			new_min = df['y'].min()
			if (new_min-old_min)>0: bias = -(new_min-old_min)
			else: bias = (new_min-old_min)
			box[1,:] = box[1,:] + bias

		if dim[2]==1:
			old_min = df['z'].min()
			mean = df['z'].mean()
			tmp1 = df[df['z']>=mean]['z']    # series
			tmp2 = df[df['z']<=mean]['z']
			df.loc[tmp1.index, 'z'] = tmp1 - 2*(tmp1 - mean)    # df.loc[row_index,col_indexer] = value  may void error
			df.loc[tmp2.index, 'z'] = tmp2 - 2*(tmp2 - mean)
			## update box
			new_min = df['z'].min()
			if (new_min-old_min)>0: bias = -(new_min-old_min)
			else: bias = (new_min-old_min)
			box[2,:] = box[2,:] + bias

		## Save output
		self.atom[['x','y','z']] = df[['x','y','z']]     # can use this way, because there is no slicing
		self.box = box
		return


	def wrap_coords_DUMP(self, dim=[1,1,1]):
		"""The method to flip coords over the center.

		Args:
			dim (list, optional): choose the dimenstion to take flip. Defaults to [1,1,1].

		Returns:
			Obj(LmpFrame): update FRAME
		"""
		## Inputs
		box = self.box
		df = self.atom[['x','y','z']]
		df = wrap_coord_PBC(df, box, bound_cond=dim)
		## Save output
		self.atom.loc[self.atom.index, ['x','y','z']] = df[['x','y','z']]
		return



	def change_atom_type(self, old_type, new_type, save_old_type=True):
		""" The method to change types of atoms in system.

		Args:
			old_type (list): a list of old-types.
			new_type (int):  one new-type.
			save_old_type (bool): to back up old types. Default to True.

		Returns:
			Obj(LmpFrame): update FRAME

		Examples:
			```python
			da.chage_atom_type([1,2,3], 2)
			```
		"""
		## Inputs
		if not isinstance(new_type,int):
			raise Exception('new_type must be an integer')

		df = self.atom
		mass = self.mass
		### back up Atom Types
		if save_old_type:
			self.add_column(df['type'], newColumn=['old_type'])
		### Change Atom Types
		df.loc[df['type'].isin(old_type),'type'] = new_type
		mass.loc[ mass['type']==min(old_type), 'type'] = new_type
		mass = mass[ mass['type'].isin(set(df['type'])) ]

		self.atom = df
		self.mass = mass
		self._num['n_atom_types'] = len(set(df['type']))

		return
	#####=======


	def merge_atom_type(self, old_type, save_old_type=True):
		""" The method to merge types of atoms in system.

		Args:
			old_type (list): a list of old-types.
			save_old_type (bool): to back up old types. Default to True.

		Returns:
			Obj(LmpFrame): update FRAME

		Examples:
			```python
			da.chage_atom_type([1,2,3], 2)
			```
		"""
		new_type = min(old_type)
		self.change_atom_type(old_type, new_type, save_old_type)
		return
	#####=======


	def copy(self):
		""" The method to make an indepedent copy of LmpFrame Obj. Then, the change values of the fields of the new object, the old object should not be affected by that.

		Args:
			None

		Returns:
			Obj(LmpFrame): new LmpFrame Obj.

		Examples:
			```python
			da1 = da.copy()
			```
		Refs:
			"shallow copying" vs "deep copying": https://stackoverflow.com/questions/3975376/understanding-dict-copy-shallow-or-deep/3975388#3975388
		"""
		da = copy.deepcopy(self)
		return da

	def replicate(self, dim=[1,1,1]):
		"""The method to flip coords over the center.

		Args:
			dim (list, optional): choose the dimenstion to take flip. Defaults to [1,1,1].

		Returns:
			Obj(LmpFrame): update FRAME
		"""
		if dim[0]>1:
			da = self.copy()
			sep = da.box[0,1] - da.box[0,0]
			for i in range(dim[0]-1):
				self.combine_frame(da, alignment='maxXYZ', shift_XYZ=[sep, 0, 0], merge_box=True, merge_type=True)

		if dim[1]>1:
			da = self.copy()
			sep = da.box[1,1] - da.box[1,0]
			for i in range(dim[1]-1):
				self.combine_frame(da, alignment='maxXYZ', shift_XYZ=[0, sep, 0], merge_box=True, merge_type=True)

		if dim[2]>1:
			da = self.copy()
			sep = da.box[2,1] - da.box[2,0]
			for i in range(dim[2]-1):
				self.combine_frame(da, alignment='maxXYZ', shift_XYZ=[0, 0, sep], merge_box=True, merge_type=True)
		return


	def scale_box(self, scale=None, final=None, delta=None, remap=True):
		""" The method to change size of simulation box.

		Args:
			scale (list, optional): to set scale ratio on each dimension of the box.
				scale = [0.7, 0.7, None] : if one dimension is set "None" its length is not changed.
			final (list, optional): to set final length on each dimension of the box.
			delta (list, optional): to set amount of change on each dimension of the box.
			remap (bool, optional): remap atom coordinate. Default to True.

		Returns:
			Obj(LmpFrame): update FRAME

		Examples:
			```python
			da.scale_box(scale=[0.7, 0.7, None])
			```
		"""
		box = self.box
		lenX = (box[0,1] - box[0,0])
		lenY = (box[1,1] - box[1,0])
		lenZ = (box[2,1] - box[2,0])
		if scale is not None:
			if scale[0] is not None: Xscale = scale[0]
			if scale[1] is not None: Yscale = scale[1]
			if scale[2] is not None: Zscale = scale[2]
		elif final is not None:
			if final[0] is not None: Xscale = final[0]/lenX
			if final[1] is not None: Yscale = final[1]/lenY
			if final[2] is not None: Zscale = final[2]/lenZ
		elif delta is not None:
			if delta[0] is not None: Xscale = (delta[0] + lenX)/lenX
			if delta[1] is not None: Yscale = (delta[1] + lenY)/lenY
			if delta[2] is not None: Zscale = (delta[2] + lenZ)/lenZ
		else:
			raise ValueError('set "scale" or "final" or "delta" values')
		## Scaling
		box[0,1] = Xscale*lenX
		box[1,1] = Yscale*lenY
		box[2,1] = Zscale*lenZ
		self.box = box
		## remap
		if remap:
			self.atom.loc[self.atom.index, 'x'] = self.atom['x']*Xscale
			self.atom.loc[self.atom.index, 'y'] = self.atom['y']*Yscale
			self.atom.loc[self.atom.index, 'z'] = self.atom['z']*Zscale
		return


	## Compute functions
	def check_exist(self, atom_types=None, mass_types=None):
		""" The method to check whether something is existed in system or not.

		Args:
			atom_types (list-of-int, optional): atom-types. Default to None.
			mass_types (list-of-int, optional): atom-types. Default to None.

		Returns:
			raise Message if error (mgs).

		Examples:
			```python
			da.isExist(atom_types=[2,3])
			```
		Notes:
			set() also return unique values.
		"""
		if atom_types is not None:
			c = set( np.intc(atom_types) ) - set( self.atom['type'].astype(int) )          # check all items in list A not in list B
			if c: raise Exception('Atom-types {} are not in system'.format(c))

		if mass_types is not None:   # use "is not" instead of "!=" to avoid datatype error
			if self.mass is not None:
				c = set( np.intc(mass_types) ) - set( self.mass['type'].astype(int) )   # check all items in list A not in list B
				if c: raise Exception('mass-types {} are not in system'.format(c))
			else:
				raise ValueError('Atom-mass are not existed, please set it')
		return

	def compute_mass(self, atom_types=[]):
		""" The method to compute mass of selected atom_types.

		Args:
			atom_types (list): atom-types to compute masses. Defaults to [], mean all-types.

		Returns:
			m (float): total mass of selected atoms.

		Examples:
			```python
			da.compute_mass(atom_types=[2,3])
			```
		"""
		## input
		if not atom_types:
			types = list(set( self.atom['type'].astype(int) ))
		else:
			types = list(set( np.intc(atom_types) ))
		## check existence
		self.check_exist(atom_types=types)
		self.check_exist(mass_types=types)

		total_mass = 0
		for item in types:
			natom = self.atom[self.atom['type']==item].size   # len of pandas series
			mass = self.mass[self.mass['type']==item]['mass'].values[0]   # note. pd.values return array
			total_mass += natom*mass
		return total_mass


	def compute_wt_percent(self, atom_types):
		""" The method to compute weight percentage of some atom_types.

		Args:
			atom_types (list): atom-types compute percentage of weight.

		Returns:
			wt% (float): weight percentage of chosen atoms.

		Examples:
			```python
			da.compute_wt_percent(atom_types=[2,3])
			```
		"""
		partial_mass = self.compute_mass(atom_types)
		total_mass = self.compute_mass()
		wt = partial_mass*100/total_mass
		return wt
	#####=======




