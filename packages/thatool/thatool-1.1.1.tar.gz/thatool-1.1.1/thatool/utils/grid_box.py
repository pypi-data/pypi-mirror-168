import numpy as np


def grid_box_2d(points, box, plane='XY', mode='bin_number', grid_size=[20,20]):
	""" devide box into 2d grid, return list of atom-IDs in each slab and list of slab-centers
	* Input: 
		P          : Nx3 array contain positions of atoms
		box        : simulation box
		mode       : "bin_number" or "bin_size"
		mode_value : corresponding 'Number-of-bins' or 'size-of-bin'
		plane      : on which plane the box will be gridded
	* Output: 
		atomIDinCell : 1xBinNumber array of 1xM-vector, contain indices of atoms of each Cell
		cellCenter   : 1xBinNumber array of scalar, is center of each slab"""   
	
	## refine input 
	P = np.asarray(points);    box = np.asarray(box);  grid_size=np.asarray(grid_size)
	if   (plane=='XY'): col1=0; col2=1
	elif (plane=='XZ'): col1=0; col2=2
	elif (plane=='YZ'): col1=1; col2=2 
	else: raise Exception("not availabe plane, please choose 'XY', 'XZ', 'YZ' ")
	##
	rowNum = grid_size[0];   colNum = grid_size[1]; 
	if mode=='bin_number': 
		Xgrid = np.linspace(box[col1,0], box[col1,1], colNum+1)   # number of columns
		Ygrid = np.linspace(box[col2,0], box[col2,1], rowNum+1)   # number of rows
	if mode=='bin_size':     
		Xgrid = np.hstack((np.arange(box[col1,0], box[col1,1], colNum),  box[col1,1])) 
		Ygrid = np.hstack((np.arange(box[col2,0], box[col2,1], rowNum),  box[col2,1])) 
		
	##
	totalCell = (len(Xgrid)-1)*(len(Ygrid)-1)   
	atomIDinCell = [None]*(totalCell);  # list of None (NxN) rows, arbitrary number of columns   
	cellCenter = [None]*(totalCell)     
	oldAtomID = np.arange(P.shape[0])           # original atom's ID of P
	runIndex=-1
	for i in range(len(Ygrid)-1):
		for j in range(len(Xgrid)-1):
			runIndex = runIndex +1
			myCond = (P[:,col1]>Xgrid[j]) & (P[:,col1]<=Xgrid[j+1]) & (P[:,col2]>Ygrid[i]) & (P[:,col2]<=Ygrid[i+1])
			atomIDinCell[runIndex] = oldAtomID[myCond]        
			cellCenter[runIndex] = [(Xgrid[j] + Xgrid[j+1])/2,  (Ygrid[i] + Ygrid[i+1])/2]
	##
	return np.asarray(atomIDinCell), np.asarray(cellCenter)
##--------


def grid_box_1d(points, box, axis='Z', mode='bin_number', grid_size=20):
	""" devide box into 1d slabs, return list of atom-IDs in each slab and list of slab-centers
	* Input: 
		P          : Nx3 array contain positions of atoms
		box        : simulation box
		mode       : "bin_number" or "bin_size"
		mode_value : corresponding 'Number-of-bins' or 'size-of-bin'
		axis       : on which axis the box will be slabbed
	* Output: 
		atomIDinCell : 1xBinNumber array of 1xM arrays, contain indices of atoms of each Slab, array of arrays
		geoCenter    : 1xBinNumber array of scalar, is geometry center of each slab
		massCenter   : 1xBinNumber array of scalar, is mass center of each slab"""   
	
	## refine input 
	P = np.asarray(points);    box = np.asarray(box);  
	if (axis=='Z')or(axis=='z')or(axis==2): colu=2
	if (axis=='Y')or(axis=='y')or(axis==1): colu=1
	if (axis=='X')or(axis=='x')or(axis==0): colu=0  
	##
	if mode=='bin_number': 
		binNum = grid_size
		Xgrid = np.linspace(box[colu,0], box[colu,1], binNum+1)
	if mode=='bin_size': 
		bin_size = grid_size
		Xgrid = np.hstack((np.arange(box[colu,0], box[colu,1], bin_size), box[colu,1]))
	##
	atomIDinCell = [None]*(len(Xgrid)-1);   geoCenter = [None]*(len(Xgrid)-1);   massCenter = [None]*(len(Xgrid)-1)     # list of None 														 
	oldAtomID = np.arange(P.shape[0])           # original ID of P
	for i in range(len(Xgrid)-1):
		tmpID = oldAtomID[(P[:,colu] > Xgrid[i]) & (P[:,colu] <= Xgrid[i+1])]
		atomIDinCell[i]  = tmpID
		geoCenter[i] = (Xgrid[i] + Xgrid[i+1])/2
		if tmpID.size != 0:  massCenter[i] = np.sum(P[tmpID, colu]) /tmpID.size
		else: massCenter[i] = 0
	##
	return np.asarray(atomIDinCell), np.asarray(geoCenter), np.asarray(massCenter)
##--------

