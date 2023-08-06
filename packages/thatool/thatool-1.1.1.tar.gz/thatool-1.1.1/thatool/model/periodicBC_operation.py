import numpy as np
import pandas as pd
from ..utils.row_operation    import unique_row, match_row

#### ===========================================================================
#### Functions definition
#### ===========================================================================
def add_periodic_image(points, box, bound_cond=[1, 1, 1], cutoff=6.5):
	"""Function to add "Periodic Images" of atoms at Periodic Boundaries (with a specific cutoff distance)
	By Thang, June 2019 (update 2022)

	Args:
		points (2d-list/np.array/pd.DataFrame)    : Mx3 Matrix contain positions of atoms before Wrapping
		box (3d-list/array) 3x2 Matrix contain simulation box bounds
		bound_cond (list): 1x3 list contains convention of Peridic bounds(ex: bound_cond = [1 1 1])
		cutoff (float): Cutoff distance

	Returns:
	    df (pd.DataFrame): contains original atoms and image atoms with remark colum df['image'].

	Examples:
	    df = add_periodic_image(P, box, bound_cond=[1 1 0], cutoff=5)
	 """
	## convert input to DataFrame
	if isinstance(points, pd.DataFrame): df = points
	if isinstance(points, list):         df = pd.DataFrame(points, columns=['x','y','z'] )
	if isinstance(points, np.ndarray):   df = pd.DataFrame(points.tolist(), columns=['x','y','z'] )
	if 'idx' not in df.columns.tolist():
		df['idx'] = np.arange(df.shape[0])
	df['image'] = 0               # 'image' to remark an image atom vs original atoms

	## Add atoms at Periodic Boundaries
	box = np.asarray(box)
	lenX = box[0,1]-box[0,0]
	lenY = box[1,1]-box[1,0]
	lenZ = box[2,1]-box[2,0]
	## on X_bound
	if bound_cond[0]==1:
		## left X
		wall = box[0,0]
		df_img1 = df[df['x'] <= wall+cutoff]
		df_img1.loc[df_img1.index,'x'] = df_img1.loc[df_img1.index,'x'] + lenX     # periodicity: moving atoms a distance = length box
		df_img1.loc[df_img1.index,'image'] = 1                                     # remark image atoms
		## right X
		wall = box[0,1]
		df_img2 = df[df['x'] >= wall-cutoff]
		df_img2.loc[df_img2.index,'x'] = df_img2.loc[df_img2.index,'x'] - lenX     # periodicity: moving atoms a distance = length box
		df_img2.loc[df_img2.index,'image'] = 1                                     # remark image atoms
		df = pd.concat([df, df_img1, df_img2], axis=0, ignore_index=True)  # update df
	## on Y_bound
	if bound_cond[1]==1:
		## left Y
		wall = box[1,0]
		df_img1 = df[df['y'] <= wall+cutoff]
		df_img1.loc[df_img1.index,'y'] = df_img1.loc[df_img1.index,'y'] + lenY     # periodicity: moving atoms a distance = length box
		df_img1.loc[df_img1.index,'image'] = 1                                     # remark image atoms
		## right Y
		wall = box[1,1]
		df_img2 = df[df['y'] >= wall-cutoff]
		df_img2.loc[df_img2.index,'y'] = df_img2.loc[df_img2.index,'y'] - lenY     # periodicity: moving atoms a distance = length box
		df_img2.loc[df_img2.index,'image'] = 1                                     # remark image atoms
		df = pd.concat([df, df_img1, df_img2], axis=0, ignore_index=True)  # update df
	## on Z_bound
	if bound_cond[2]==1:
		## left Y
		wall = box[2,0]
		df_img1 = df[df['z'] <= wall+cutoff]
		df_img1.loc[df_img1.index,'z'] = df_img1.loc[df_img1.index,'z'] + lenZ     # periodicity: moving atoms a distance = length box
		df_img1.loc[df_img1.index,'image'] = 1                                     # remark image atoms
		## right Y
		wall = box[2,1]
		df_img2 = df[df['z'] >= wall-cutoff]
		df_img2.loc[df_img2.index,'z'] = df_img2.loc[df_img2.index,'z'] - lenZ     # periodicity: moving atoms a distance = length box
		df_img2.loc[df_img2.index,'image'] = 1                                     # remark image atoms
		df = pd.concat([df, df_img1, df_img2], axis=0, ignore_index=True)  # update df
	## remove duplicated atoms
	df.drop_duplicates(subset=['x','y','z'], inplace=True)

	return df
##--------


def wrap_coord_PBC(points, box, bound_cond=[1, 1, 1]):
	"""Function to wrap atom positions at Periodic Boundaries
	By Thang, June 2019 (update 2022)

	Args:
		points (2d-list/np.array/pd.DataFrame)    : Mx3 Matrix contain positions of atoms before Wrapping
		box (3d-list/array) 3x2 Matrix contain simulation box bounds
		bound_cond (list): 1x3 list contains convention of Peridic bounds(ex: bound_cond = [1 1 1])

	Returns:
	    df (pd.DataFrame): contains atom positions.
	Examples:
	    df = wrap_coord_PBC(P, box, bound_cond=[1 1 0], cutoff=5)
	 """
	## convert input to DataFrame
	if isinstance(points, pd.DataFrame): df = points
	if isinstance(points, list):         df = pd.DataFrame(points, columns=['x','y','z'] )
	if isinstance(points, np.ndarray):   df = pd.DataFrame(points.tolist(), columns=['x','y','z'] )

	## Add atoms at Periodic Boundaries
	box = np.asarray(box)
	lenX=box[0,1]-box[0,0]
	lenY=box[1,1]-box[1,0]
	lenZ=box[2,1]-box[2,0]
	## on X_bound
	if bound_cond[0]==1:
		## left X
		wall = box[0,0];
		df_tmp = df[df['x'] < wall]
		while df_tmp.shape[0]!=0:                             # periodicity: moving atoms a distance = length box
			df.loc[df_tmp.index, 'x'] = df.loc[df_tmp.index, 'x'] + lenX
			df_tmp = df[df['x'] < wall]
		## right X
		wall = box[0,1]
		df_tmp = df[df['x'] > wall]
		while df_tmp.shape[0]!=0:                             # periodicity: moving atoms a distance = length box
			df.loc[df_tmp.index, 'x'] = df.loc[df_tmp.index, 'x'] - lenX
			df_tmp = df[df['x'] > wall]

	## on Y_bound
	if bound_cond[1]==1:
		## left Y
		wall = box[1,0]
		df_tmp = df[df['y'] < wall]
		while df_tmp.shape[0]!=0:                             # periodicity: moving atoms a distance = length box
			df.loc[df_tmp.index, 'y'] = df.loc[df_tmp.index, 'y'] + lenY
			df_tmp = df[df['y'] < wall]
		## right Y
		wall = box[1,1]
		df_tmp = df[df['y'] > wall]
		while df_tmp.shape[0]!=0:                             # periodicity: moving atoms a distance = length box
			df.loc[df_tmp.index, 'y'] = df.loc[df_tmp.index, 'y'] - lenY
			df_tmp = df[df['y'] > wall]

	## on Z_bound
	if bound_cond[2]==1:
		## left Z
		wall = box[2,0]
		df_tmp = df[df['z'] < wall]
		while df_tmp.shape[0]!=0:                             # periodicity: moving atoms a distance = length box
			df.loc[df_tmp.index, 'z'] = df.loc[df_tmp.index, 'z'] + lenZ
			df_tmp = df[df['z'] < wall]
		## right Z
		wall = box[2,1]
		df_tmp = df[df['z'] > wall]
		while df_tmp.shape[0]!=0:                             # periodicity: moving atoms a distance = length box
			df.loc[df_tmp.index, 'z'] = df.loc[df_tmp.index, 'z'] - lenZ
			df_tmp = df[df['z'] > wall]
	return df
##--------






#### ===========================================================================
#### Old functions
#### ===========================================================================
def add_periodic_image_old(P, box, bound_cond=[1, 1, 1], cutoff=6.5):
	""" Function to add "Periodic Images" of atoms at Periodic Boundaries
	 (with a specific cutoff distance)

	 (input) = (P, box, cutoff, bound_cond)
	        P    : Mx3 Matrix contain positions of atoms before Wrapping
	        box  : 3x2 Matrix contain simulation box bounds
	        cutoff : scalar value of Cutoff distance
	        bound_cond : 1x3 Matrix contain convention of Peridic bounds(ex: bound_cond = [1 1 1])

	 [output] = [addAtom, addIndex, allAtom, allIndex]
	        addAtom : 2d array contain positions of only added atoms
	        addIndex :1d array contain conserved Index (added-atoms have the same indices to origin atoms).
	        allAtom : 2d array combine added atoms + oldAtom
	        allIndex :1d array combine added Index + oldIndex

	   Example: addAtom, addIndex, allAtom, allIndex = fBCs_Add_Periodic_Image(P, box, 2.5, [1 1 0])
	 By Cao Thang, June 2019"""

	# refine input
	P = np.asarray(P);    box = np.asarray(box);   bound_cond = np.asarray(bound_cond);

	## Add atoms at Periodic Boundaries
	lenX=box[0,1]-box[0,0]; lenY=box[1,1]-box[1,0]; lenZ=box[2,1]-box[2,0];
	I = np.arange(P.shape[0]);
	oldIndex = np.copy(I)       # original index of input atoms
	oldAtom = np.copy(P)                    # original input atoms
	# --
	addAtom = np.empty((1,3))       # save all added atoms only, contain 1 dummy-atom as created
	addIndex = np.empty(1)

	## on X_bound
	if bound_cond[0] == 1:
		col = 0; Dist = lenX;
		# left X
		bnd = box[0,0];
		nowIndex = np.arange(P.shape[0]) ;
		tmpIndex = nowIndex[P[:,col] <= bnd+cutoff]
		Padd = P[tmpIndex, :]  ;             # Nx3 matrix
		Iadd = I[tmpIndex];                  # Nx1 matrix
		# take periodicity
		Padd[:,col] = Padd[:,col] + Dist;
		## upadate total P
		P = np.vstack((P, Padd))        # 2d array
		I = np.hstack((I, Iadd))        # 1d array, add new Indices
		# add new atoms into oringinal model
		addAtom = np.vstack((addAtom, Padd))  # save only added-atoms
		addIndex = np.hstack((addIndex, Iadd))

		# right X
		bnd = box[0,1];
		nowIndex = np.arange(P.shape[0]) ;
		tmpIndex = nowIndex[P[:,col] >= bnd-cutoff]
		Padd = P[tmpIndex, :]  ;             # Nx3 matrix
		Iadd = I[tmpIndex];                  # Nx1 matrix
		# take periodicity
		Padd[:,col] = Padd[:,col] - Dist;
		## upadate total P
		P = np.vstack((P, Padd))        # 2d array
		I = np.hstack((I, Iadd))        # 1d array, add new Indices
		# add new atoms into oringinal model
		addAtom = np.vstack((addAtom, Padd))  # save only added-atoms
		addIndex = np.hstack((addIndex, Iadd))

	## on Y_bound
	if bound_cond[1] == 1:
		col = 1; Dist = lenY;
		# left Y
		bnd = box[1,0];
		nowIndex = np.arange(P.shape[0]) ;
		tmpIndex = nowIndex[P[:,col] <= bnd+cutoff]
		Padd = P[tmpIndex, :]  ;             # Nx3 matrix
		Iadd = I[tmpIndex];                  # Nx1 matrix
		# take periodicity
		Padd[:,col] = Padd[:,col] + Dist;
		## upadate total P
		P = np.vstack((P, Padd))        # 2d array
		I = np.hstack((I, Iadd))        # 1d array, add new Indices
		# add new atoms into oringinal model
		addAtom = np.vstack((addAtom, Padd))  # save only added-atoms
		addIndex = np.hstack((addIndex, Iadd))

		# right Y
		bnd = box[1,1];
		nowIndex = np.arange(P.shape[0]) ;
		tmpIndex = nowIndex[P[:,col] >= bnd-cutoff]
		Padd = P[tmpIndex, :]  ;             # Nx3 matrix
		Iadd = I[tmpIndex];                  # Nx1 matrix
		# take periodicity
		Padd[:,col] = Padd[:,col] - Dist;
		## upadate total P
		P = np.vstack((P, Padd))        # 2d array
		I = np.hstack((I, Iadd))        # 1d array, add new Indices
		# add new atoms into oringinal model
		addAtom = np.vstack((addAtom, Padd))  # save only added-atoms
		addIndex = np.hstack((addIndex, Iadd))

	## on Z_bound
	if bound_cond[2] == 1:
		col = 2; Dist = lenZ;
		# left Z
		bnd = box[2,0];
		nowIndex = np.arange(P.shape[0]) ;
		tmpIndex = nowIndex[P[:,col] <= bnd+cutoff]
		Padd = P[tmpIndex, :]  ;             # Nx3 matrix
		Iadd = I[tmpIndex];                  # Nx1 matrix
		# take periodicity
		Padd[:,col] = Padd[:,col] + Dist;
		## upadate total P
		P = np.vstack((P, Padd))        # 2d array
		I = np.hstack((I, Iadd))        # 1d array, add new Indices
		# add new atoms into oringinal model
		addAtom = np.vstack((addAtom, Padd))  # save only added-atoms
		addIndex = np.hstack((addIndex, Iadd))

		# right Z
		bnd = box[2,1];
		nowIndex = np.arange(P.shape[0]) ;
		tmpIndex = nowIndex[P[:,col] >= bnd-cutoff]
		Padd = P[tmpIndex, :]  ;             # Nx3 matrix
		Iadd = I[tmpIndex];                  # Nx1 matrix
		# take periodicity
		Padd[:,col] = Padd[:,col] - Dist;
		## upadate total P
		P = np.vstack((P, Padd))        # 2d array
		I = np.hstack((I, Iadd))        # 1d array, add new Indices
		# add new atoms into oringinal model
		addAtom = np.vstack((addAtom, Padd))  # save only added-atoms
		addIndex = np.hstack((addIndex, Iadd))

	## Remove first added atom (the dummy-atom when initiate array)
	addAtom = addAtom[1:,:]
	addIndex = addIndex[1:]
	## remove duplicated atoms
	_,uniqueIndex = unique_row(addAtom, tol_decimal=2)
	addAtom = addAtom[uniqueIndex]
	addIndex = addIndex[uniqueIndex]
	##--
	_,mismatch_index = match_row(addAtom, oldAtom)
	addAtom = addAtom[mismatch_index]
	addIndex = addIndex[mismatch_index]

	# Out put
	allAtom = np.vstack((oldAtom, addAtom))
	allIndex = np.hstack((oldIndex, addIndex))

	return addAtom, addIndex, allAtom, allIndex
##--------

def wrap_coord_PBC_old(P, box, bound_cond=[1, 1, 1]):

	  # refine input
	P = np.asarray(P);    box = np.asarray(box);   bound_cond = np.asarray(bound_cond);

	## Add atoms at Periodic Boundaries
	lenX=box[0,1]-box[0,0]; lenY=box[1,1]-box[1,0]; lenZ=box[2,1]-box[2,0];
	oldIndex = np.arange(P.shape[0]);

	## on X_bound
	if bound_cond[0] == 1:
		col = 0; Dist = lenX;
		# left X
		bnd = box[0,0];
		tmpIndex = oldIndex[P[:,col] < bnd]
		# take periodicity
		while len(tmpIndex)!=0:
			P[tmpIndex,col] = P[tmpIndex,col]%Dist + Dist;
			tmpIndex = oldIndex[P[:,col] < bnd]

		# right X
		bnd = box[0,1];
		tmpIndex = oldIndex[P[:,col] > bnd]
		# take periodicity
		while len(tmpIndex)!=0:
			P[tmpIndex,col] = P[tmpIndex,col] - Dist;
			tmpIndex = oldIndex[P[:,col] > bnd]

	## on Y_bound
	if bound_cond[1] == 1:
		col = 1; Dist = lenY;
		# left Y
		bnd = box[1,0];
		tmpIndex = oldIndex[P[:,col] < bnd]
		# take periodicity
		while len(tmpIndex)!=0:
			P[tmpIndex,col] = P[tmpIndex,col]%Dist + Dist;
			tmpIndex = oldIndex[P[:,col] < bnd]

		# right Y
		bnd = box[1,1];
		tmpIndex = oldIndex[P[:,col] > bnd]
		# take periodicity
		while len(tmpIndex)!=0:
			P[tmpIndex,col] = P[tmpIndex,col] - Dist;
			tmpIndex = oldIndex[P[:,col] > bnd]

	## on Z_bound
	if bound_cond[2] == 1:
		col = 2; Dist = lenZ;
		# left Z
		bnd = box[2,0];
		tmpIndex = oldIndex[P[:,col] < bnd]
		# take periodicity
		while len(tmpIndex)!=0:
			P[tmpIndex,col] = P[tmpIndex,col]%Dist + Dist;
			tmpIndex = oldIndex[P[:,col] < bnd]

		# right Z
		bnd = box[2,1];
		tmpIndex = oldIndex[P[:,col] > bnd]
		# take periodicity
		while len(tmpIndex)!=0:
			P[tmpIndex,col] = P[tmpIndex,col] - Dist;
			tmpIndex = oldIndex[P[:,col] > bnd]

	return P
##--------




