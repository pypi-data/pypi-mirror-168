from numpy      import array, zeros, asarray, einsum, arctan, dot, cross, sin, cos, pi, gcd, sqrt


### ============================================================================
## Vector tranformation/ Rotation
class CoordTransform:
	"""We can express a rotation using direction-cosines-matrix (DCM) or Euler-angles (phi,theta,psi)
	REFs: 
		1. Bower, Allan F. Applied Mechanics of Solids. CRC Press, 2009. page 711
		2. https://link.aps.org/doi/10.1103/PhysRevB.92.180102
		3. https://en.wikipedia.org/wiki/Euler_angles
	"""
	def __init__(self, old_orient=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
					   new_orient=[[1, 0, 0], [0, 1, 0], [0, 0, 1]]
				):
		"""* Optional Inputs:
			old_orient: 3x3 array/list, contains 3 mutully orthotropic unit vectors of the OLD basis 
			new_orient: 3x3 array/list, contains 3 mutully orthotropic unit vectors of the NEW basis
				(all input vector will be normalized to unit vectors)
				
		Example:    oldAxis = array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
					newAxis = array([[1, -1, 0], [1, 1, -2], [1, 1, 1]])
				BT = thaTool.CoordTransform(old_orient=oldAxis, new_orient=newAxis)"""

		## Initialization
		self.old_orient = asarray(old_orient)
		self.new_orient = asarray(new_orient)
		self.DCM  	= None
		self.ROT  	= None
		self.EA		= None
	
	def direction_cosine_matrix(self):
		"""Calculate direction-cosines-matrix (DCM) between 2 coordinates systems 
		* Input: 
		* Output:
			Q: 3x3 array, the rotation matrix or matrix of direction cosines
		Example:   
			BT = thaTool.CoordTransform(old_orient=oldAxis, new_orient=newAxis) 
			Q = BT.direction_cosine_matrix()
		By Cao Thang, Apr 2019,  Update: May2020"""

		old_orient = self.old_orient
		new_orient = self.new_orient
		## Calculate the matrix of direction cosines [new_orient.old_orient]
		Q = zeros((3,3))
		for i in range(Q.shape[0]):
			for j in range(Q.shape[1]):
				a = asarray(new_orient[i,:])
				b = asarray(old_orient[j,:])
				Q[i,j] = dot(a,b)/ ( sqrt(a.dot(a))*sqrt(b.dot(b)) )
		##
		self.DCM = Q
		return Q   
	#######

	def rotation_matrix(self):
		"""Calculate Rotation-matrix (R) as transpose of DCM
		By Cao Thang, Apr 2019,  Update: May2020"""
		## Calculate the matrix of direction cosines [new_orient.old_orient]
		R = self.direction_cosine_matrix().T
		##
		self.ROT= R
		return R   
	#######


	def EA2ROT(self, euler_angle, unit='rad'):
		"""Calculate Rotation_Matrix Euler Angles (EA) between 2 coordinates systems (ZXZ proper Euler angles)
		This is just for testing, since we dont know whether input angles yield orthogonal axis or not
		* Input Compulsory: 
			- EulerAngle: 1x3 array/list (phi,theta,psi) in Rad or Deg
		* Input (Optional): 
			- unit='rad': 'rad' or 'deg'      (default is rad)
		* Output:
			Q: 3x3 array, the rotation matrix or matrix of direction cosines
		Example:   
			BT = thaTool.CoordTransform() 
			DCM = BT.EulerAngle(euler_angle=[90,], unit='deg')
		NOTEs: don't use arctan2()
		By Cao Thang, May2020"""
		## Collect inputs
		if 'deg' in unit: 
			ufac = pi/180
		elif'rad' in unit: 
			ufac = 1
		else:
			raise ValueError("Supported units are: 'deg' or 'rad'")

		phi,theta,psi = asarray(euler_angle)*ufac

		## DCM, convension ZXZ
		R = zeros((3,3))
		R[0,0] = cos(psi)*cos(phi) - cos(theta)*sin(phi)*sin(psi)
		R[0,1] = cos(psi)*sin(phi) + cos(theta)*cos(phi)*sin(psi)
		R[0,2] = sin(psi)*sin(theta)

		R[1,0] = -sin(psi)*cos(phi) - cos(theta)*sin(phi)*cos(psi)
		R[1,1] = -sin(psi)*sin(phi) + cos(theta)*cos(phi)*cos(psi)
		R[1,2] = cos(psi)*sin(theta)

		R[2,0] = sin(theta)*sin(phi)
		R[2,1] = -sin(theta)*cos(phi)
		R[2,2] = cos(theta)
		##
		self.ROT = R
		return R
	##--------

	def euler_angle(self, unit='rad'):
		"""Calculate Euler Angles (EA) between 2 coordinates systems (intrinsic ZXZ proper Euler angles)
		https://en.wikipedia.org/wiki/Euler_angles#Definition_by_intrinsic_rotations
		https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.as_euler.html#r72d546869407-1
		* Input (Optional): 
			- unit='rad': 'rad' or 'deg'      (default is rad)
		* Output:
			- Angle: 1x3 array (phi,theta,psi) in Rad  (apply intrinsic ZXZ proper Euler)
		Example:   
			BT = thaTool.CoordTransform(old_orient=oldAxis, new_orient=newAxis) 
			phi,theta,psi = BT.EulerAngle(unit='deg')
		NOTEs: 
			- don't use arctan2()
			- Rotation Matrix is as to tranpose of DCM, use Rotation Matrix to compute EA
		By Cao Thang, May2020"""
		## Collect inputs
		if 'deg' in unit: 
			ufac = pi/180
		elif'rad' in unit: 
			ufac = 1
		else:
			raise ValueError("Supported units are: 'deg' or 'rad'")

		## Calculate Euler Angles [new_orient.old_orient], convension ZXZ
		R = self.direction_cosine_matrix()
		# R = self.rotation_matrix()
		phi = ufac*arctan(-R[2,0]/ R[2,1] )  
		theta = ufac*arctan( sqrt(1-R[2,2]**2)/ R[2,2] ) 
		psi = ufac*arctan( R[0,2]/ R[1,2] ) 
		##
		self.EA = (phi, theta, psi) 
		return (phi, theta, psi) 
	##--------

	def euler_angle_PSpincal(self, EulerOrder='zxz', unit='rad', tol=1e-7):
		"""Calculate Euler Angles (EA) between 2 coordinates systems (proper Eulerian angles)
		[1] navpy not use 'ZXZ': https://navpy.readthedocs.io/en/latest/code_docs/coordinate_transformations.html
		[2] use this https://pypi.org/project/PSpincalc/
					 https://github.com/tuxcell/PSpincalc/blob/master/PSpincalc/PSpincalc.py
					 Ex: https://github.com/tuxcell/PSpincalc/blob/master/examples/examplesPSpincalc.ipynb
		* Input (Optional): 
			unit: 'rad', 'deg'      (default is rad)
			EulerOrder='zxz': rotation order, lowercase ["zyx","zxy","yxz","xzy","xyz","yzx","zyz","zxz","yxy","yzy","xyx","xzx"]
		* Output:
			Angle: 1x3 array (phi,theta,psi) in Rad  (apply extrinsic ZXZ proper Euler)
		NOTEs: 
			- this module may define psi as phi, and vice versa. So becareful
			- should not use PSpincalc, since it produce unknown value?
		By Cao Thang, May2020"""

		import PSpincalc as sp
		## Collect inputs
		if 'deg' in unit: 
			ufac = pi/180
		elif'rad' in unit: 
			ufac = 1
		else:
			raise ValueError("Supported units are: 'deg' or 'rad'")

		## Calculate Euler Angles [new_orient.old_orient]
		R = self.direction_cosine_matrix()
		# R = self.rotation_matrix()		
		Angle = sp.DCM2EA(R, EulerOrder=EulerOrder, tol=tol)[0] *ufac
		return (Angle[0], Angle[1],Angle[2])

	
	def rotate_3d(self, points):
		"""Rotate a set of points (or set of vectors) from a OLD-coords to NEW-coords
		* Input:
			- points: Nx3 array, contain coords in OLD coordinates systems
		* Output:
			- points: Nx3 array, contain coords in NEW coordinates systems
		Example:   
			BT = thaTool.CoordTransform(old_orient=oldAxis, new_orient=newAxis) 
			newP = BT.rotate_3d(P)
		"""
		# refine input 
		P = asarray(points);     
		# Rotate point
		Q = self.direction_cosine_matrix()
		R = einsum('ik,jk', P, Q)       	# multiply matrix Q with each row of P, equivalent to:
											#        R = zeros((P.shape[0],3))
											#        for i in range(P.shape[0]):
											#            R[i,:] = matmul(Q, P[i,:])
		return R  
### =======================  End Class  ========================================



def rot1axis(P, theta, axis='X'):
	"""Rotate array of points about 1 axis
	* Input:    P      : Nx3 array, contain input poits
				theta  : the rotation angle in Degree
				axis   : Rotation axis
	* Output:   outP   : Nx3 array, contain points after rotation
	"""
	# refine inputs
	P = asarray(P)
	theta = theta*pi/180      # convert to radian
	ct = cos(theta)
	st = sin(theta)
	# calculate rotation matrix about an axis
	if axis=='X':    R = array([[1,  0,    0],
							    [0,  ct, -st],
							    [0,  st,  ct]])
		
	elif axis=='Y':  R = array([[ct,   0,   st],
							    [0,    1,    0],
							    [-st,  0,   ct]])
		
	elif axis=='Z':  R = array([[ct,  -st,  0],
							    [st,   ct,  0],
							    [ 0,    0,  1]])
	else: raise Exception("not decide rotation axis, choose: 'X' or 'Y' or 'Z'")    
	# compute rotation points
	outP = einsum('ij,jk', P, R)    #equivalent to matmul(P,R)
	return outP


def check_right_hand(list_3vec=[[1, 0, 0], [0, 1, 0], [0, 0, 1]] ): 
	"""check right_hand_rule orthogonal of 3 vectors"""
	b1 = list(list_3vec)
	b2 = b1[1:] + b1[:1]    # roll 1 item
	b3 = b2[1:] + b2[:1] 
	for i,(e1,e2,e3) in enumerate(zip(b1,b2,b3)):
		## check perpendicular e1,e2
		if dot(e1,e2)!=0: raise Exception ('2 vectors b%i and b%i are not perpendicular.'% (i+1, i+2) )
		## check right-hand-rule
		c = cross(e1,e2)
		check_cos = dot(c,e3)/(sqrt(dot(c,c)) *sqrt(dot(e3,e3)) )    # cos theta
		if check_cos==1: pass
		else: raise Exception ('3 vectors are not orthogonal. Try vector b%i with'% (3-i), c/gcd(c[0],c[1],c[2]) ) 
	##
	return True


def guess_right_hand(list_2vec=[[1, 0, 0], [0, 1, 0]] ): 
	"""give 2 vectors, then guess the third vector that satisfy right_hand_rule"""
	e1 = list_2vec[0]
	e2 = list_2vec[1]
	## check perpendicular e1,e2
	if dot(e1,e2)!=0: raise Exception ('2 vectors are not perpendicular.')
	c = cross(e1,e2)
	return c/gcd(c[0],c[1],c[2])
