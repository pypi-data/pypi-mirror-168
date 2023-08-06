import numpy as np
import scipy.spatial



def cartesian2spherical(xyz):
	"""xyz : Mx3 matrix contain Cartesian coordinates"""
	xy2 = xyz[:,0]**2 + xyz[:,1]**2
	R = np.sqrt(xy2 + xyz[:,2]**2)
	theta = np.arctan2(np.sqrt(xy2), xyz[:,2])         # for theta angle defined from Z-axis down, in unit rad. This equivalent to np.arccos(xyz[:,2]/R), but void devide zero 
	# theta = np.arctan2(xyz[:,2], np.sqrt(xy2))           # for theta angle defined from XY-plane up
	phi = np.arctan2(xyz[:,1],xyz[:,0])
	newCoord = np.column_stack((R, theta, phi))
	return newCoord
##--------

def qlm_i(l, Rij_Position, SW):
	"""compute Ylm_bar complex vector (or qlm vector of (2l+1) components)
	* Input: 
		Rij_Position  : Nx3 array contain Rij_Positions of nearest neighbors compute from atom i
		l             : degree of Spherical Harmonic
		SW            : Nx1 values of switching function
	* Output: 
		Ylm_bar       : a vector of (2l+1) complex components, qlm(i) vector"""  
	import scipy.special
	## --
	Ps = cartesian2spherical(Rij_Position)
	m=np.arange(-l,l+0.1,1, dtype=int)
	# Ylm_bar complex vector (or qlm vector of (2l+1) components)
	qlm = np.zeros([m.shape[0]], dtype=complex)
	for i in range(m.shape[0]):
		harm = scipy.special.sph_harm(m[i], l, Ps[:,2], Ps[:,1])        # Ylm(Rij)  in eq.(8)
		qlm[i] = sum(SW*harm)/ sum(SW) 
	return qlm
##--------

def Ql_Steinhardt(qlm_i):
	"""compute origincal Stainhardt of l-th order 
	* Input: 
		qlm_i   : a vector of (2l+1) complex components, qlm(i) vector of atom i
	* Output: 
		Ql      : scalar value of l-th order Stainhardt parameter"""   
	# refine input 
	qlm_i = np.asarray(qlm_i); 
	l = qlm_i.shape[0]
	# --
	Sum_ql2 = sum(qlm_i * np.conjugate(qlm_i))
	# Sum_ql2 = sum((np.abs(qlm_i))**2)
	Ql = np.sqrt(4*np.pi/(2*l+1))*np.sqrt(Sum_ql2)
	return Ql.real
##--------

def Local_Ql_Steinhardt(qlm_i, qlm_j, SW):
	"""compute Local Stainhardt of l-th order (modified Steinhardt as: 10.1021/acs.jctc.6b01073) 
	* Input: 
		qlm_i   : 1x(2l+1) array, vector of (2l+1) complex components, qlm(i) vector of atom i
		qlm_j   : Nx(2l+1) array, rows are vectors of (2l+1) complex components, qlm(j) of all neighbors j of atom i
	* Output: 
		Local_Ql_i      : scalar value of l-th order Stainhardt parameter of atom i 
	* PreRequire: compute qlm_i complex vector for all atoms before this function can be used"""
	# refine input 
	qlm_i = np.asarray(qlm_i);      qlm_j = np.asarray(qlm_j)
	# way 1
	# dotProd = np.conjugate(qlm_j)@qlm_i    # dot product of each row of matrix qlm_j w.r.t vetor qlm_i
	dotProd = np.einsum('ij,j->i', np.conjugate(qlm_j), qlm_i)
	Local_Q6 = sum(SW*dotProd)/ sum(SW) 
	
	# #way 2
	# Sum_dotProd = 0
	# for j in range(qlm_j.shape[0]):
		# Sum_dotProd += SW[j]*sum(qlm_i*np.conjugate(qlm_j[j]))
	# Local_Q6 = Sum_dotProd/ sum(SW) 
	return Local_Q6.real
##--------

def neighbors_finder_gen(P, Box, bndCond=[1, 1, 1], **kwargs):
	""" find Nearest_Neighbors, return generator of Nearest_IDs, "Nearest relative-Position vetors from atom i" 
	Ver 2: scipy.spatial.cKDTree
	By Cao Thang, Sep 2019
	Update: Dec 2020 to use generator
	* Input: 
		P          : Nx3 array contain positions of atoms
		Box        : simulation box
		bndCond=[1, 1, 1]:  boundary condition
			Cutoff_Neighbors=6.5: find neighbors within a Cutoff, or 
  			Number_Neighbors=12: find k nearest neighbors
		keepRef=Flase    : include referal-atom in result
	* Ouyput: this output a GEN contains (Near_IDs, Rij_vectors), so access with
		for Near_ID, Rij_vector in GEN:
			print (Near_ID, Rij_vector)

		Near_IDs    : Nx1 list of Mx1-vectors, contain Image_IDs(id of the original atoms before make periodicity) of Nearest atoms 
		Rij_vectors : Nx1 list of Mx3-Matrices, contain Nearest Rij relative-Position vetors from Ref.atom i (Nearest Positions)
		
	Ex:   GEN = thaTool.neighbors_finder_gen(P, Box, bndCond = [1, 1, 1], Cutoff_Neighbors=9, keepRef=False)
	"""
	##==== optional Inputs 
	if 'Cutoff_Neighbors' in kwargs: Rcut = kwargs['Cutoff_Neighbors']  
	elif 'Number_Neighbors' in kwargs:
		near_number = kwargs['Number_Neighbors']  
		if 'Rcut' in kwargs: Rcut = kwargs['Rcut']  
		else: 			     Rcut = 9
	else: raise Exception("The 4th input must be: 'Cutoff_Neighbors' or 'Number_Neighbors'")
	
	if 'keepRef' in kwargs: keepRef = kwargs['keepRef']  
	else: 					keepRef = False
 
	## refine input 
	P = np.asarray(P);    Box = np.asarray(Box);   bndCond = np.asarray(bndCond);
	  
	## Add Periodic_Image at Periodic Boundaries
	_,_,PJ,ImageID = add_periodic_image(P, Box, bndCond, Rcut)
	
	## Detect Neighbors  
	# Near_IDs=[None]*P.shape[0]; Rij_Vectors=[None]*P.shape[0];     # Rij_Bond=[None]*P.shape[0]       # cannot use np array, since it fix the length of rows and cannot assign array to elm    
	if 'Cutoff_Neighbors' in kwargs:  
		treePJ = scipy.spatial.cKDTree(PJ)
		treeP = scipy.spatial.cKDTree(P)
		ID_listPJ = treeP.query_ball_tree(treePJ, Rcut)   # return list of lists of indice
		
		for i in range(P.shape[0]):
			m = np.asarray(ID_listPJ[i])
			if keepRef == False: m = np.delete(m, np.nonzero(m==i)) ;             # remove atom i from result
			Near_IDs = ImageID[m].astype(int) 
			# Nearest Distances & Nearest Vectors from atom i
			Rij = dist2_node2nodes(P[i,:], PJ[m,:])
			##--
			yield Near_IDs, Rij[['bx','by','bz']].values     # return 1 element of list
		##--
	 
	if 'Number_Neighbors' in kwargs:   
		treePJ = scipy.spatial.cKDTree(PJ)
		for i in range(P.shape[0]):
			_, m = treePJ.query(P[i,:], near_number+1)
			# --
			if keepRef == False: m = np.delete(m, np.nonzero(m==i)) ;             # remove atom i from result
			Near_IDs = ImageID[m].astype(int) 
			# Nearest Distances & Nearest Vectors from atom i
			Rij = dist2_node2nodes(P[i,:], PJ[m,:])  
			##--    
			yield Near_IDs, Rij[['bx','by','bz']].values      # return 1 element of list
		## --    
	# return Near_IDs, Rij_Vectors          # return all list: Near_IDs, Rij_Vectors, Rij_Bond
##--------

def neighbors_finder_list(P, Box, bndCond=[1, 1, 1], **kwargs):
	""" find Nearest_Neighbors, return list of Nearest_IDs, "Nearest relative-Position vetors from atom i" 
	Ver 2: scipy.spatial.cKDTree
	By Cao Thang, Sep 2019
	* Input: 
		P          : Nx3 array contain positions of atoms
		Box        : simulation box
		bndCond=[1, 1, 1]:  boundary condition
			Cutoff_Neighbors=6.5: find neighbors within a Cutoff, or 
  			Number_Neighbors=12: find k nearest neighbors
		keepRef=Flase    : include referal-atom in result
	* Ouyput: 
		Near_IDs    : Nx1 list of Mx1-vectors, contain Image_IDs(id of the original atoms before make periodicity) of Nearest atoms 
		Rij_vectors : Nx1 list of Mx3-Matrices, contain Nearest Rij relative-Position vetors from Ref.atom i (Nearest Positions)
		# Rij_Bonds : Nx1 list of scalars, contain Rij_bonds from Ref.atom to Nearest_atoms (Nearest-bonds)
	# NOTEs: don't compute Rij_Bond to save memory
		
	Ex:   Near_IDs, Rij_vectors = thaTool.fNeighbors_finder(P, Box, bndCond = [1, 1, 1], Cutoff_Neighbors=9, keepRef=False)
	"""
	##==== optional Inputs 
	if 'Cutoff_Neighbors' in kwargs: Rcut = kwargs['Cutoff_Neighbors']  
	elif 'Number_Neighbors' in kwargs:
		near_number = kwargs['Number_Neighbors']  
		if 'Rcut' in kwargs: Rcut = kwargs['Rcut']  
		else: 			     Rcut = 9
	else: raise Exception("The 4th input must be: 'Cutoff_Neighbors' or 'Number_Neighbors'")
	
	if 'keepRef' in kwargs: keepRef = kwargs['keepRef']  
	else: 					keepRef = False
 
	## refine input 
	P = np.asarray(P);    Box = np.asarray(Box);   bndCond = np.asarray(bndCond);
	  
	## Add Periodic_Image at Periodic Boundaries
	_,_,PJ,ImageID = add_periodic_image(P, Box, bndCond, Rcut)
	
	## Detect Neighbors  
	Near_IDs=[None]*P.shape[0]; Rij_Vectors=[None]*P.shape[0];     # Rij_Bond=[None]*P.shape[0]       # cannot use np array, since it fix the length of rows and cannot assign array to elm    
	if 'Cutoff_Neighbors' in kwargs:  
		treePJ = scipy.spatial.cKDTree(PJ)
		treeP = scipy.spatial.cKDTree(P)
		ID_listPJ = treeP.query_ball_tree(treePJ, Rcut)   # return list of lists of indice
		
		for i in range(P.shape[0]):
			m = np.asarray(ID_listPJ[i])
			if keepRef == False: m = np.delete(m, np.nonzero(m==i)) ;             # remove atom i from result
			Near_IDs[i] = ImageID[m].astype(int) 
			# Nearest Distances & Nearest Vectors from atom i
			# Rij_Bond[i], Rij_Vectors[i] = dist2_node2nodes(P[i,:], PJ[m,:])        # compute distance from atom P[i,:] to its neighbors PJ[m,:]
			df = dist2_node2nodes(P[i,:], PJ[m,:])
			Rij_Vectors[i] = df[['bx','by','bz']] 
		##--
	 
	if 'Number_Neighbors' in kwargs:   
		treePJ = scipy.spatial.cKDTree(PJ)
		for i in range(P.shape[0]):
			_, m = treePJ.query(P[i,:], near_number+1)
			# --
			if keepRef == False: m = np.delete(m, np.nonzero(m==i)) ;             # remove atom i from result
			Near_IDs[i] = ImageID[m].astype(int) 
			# Nearest Distances & Nearest Vectors from atom i
			# Rij_Bond[i], Rij_Vectors[i] = dist2_node2nodes(P[i,:], PJ[m,:])          
			df = dist2_node2nodes(P[i,:], PJ[m,:])
			Rij_Vectors[i] = df[['bx','by','bz']] 			
		## --    
	return Near_IDs, Rij_Vectors          # return all list: Near_IDs, Rij_Vectors, Rij_Bond
##--------




