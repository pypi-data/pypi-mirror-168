from math import sqrt

### ============================================================================
### Functions definition
### ============================================================================
def box_orientation(box_size=[1,1,1], zDirect='001', xDirect=None): 
	""" covert Orirentation and length of simulation box.

	Args:
		box_size (list): dimension of box on each side as in [100] direction
		zDirect (str): specify the direction of z-side. Defaults to '001', mean nothing is happen.
		xDirect (str): specify the direction of z-side.  Defaults to None.

	Returns:
		newOrient (list): list-of-vectors of 3 directional vectors.
		box_size (tuple): dimension of box on each side.

	Examples:
		
	"""
	### input 
	Lx,Ly,Lz = box_size

	## Only use 1 input at a time
	only_input = [zDirect,xDirect] 
	if sum([1 for item in only_input if item!=None])>1:
		raise ValueError('Only one of {} is used at a time'.format(only_input))

	## set orientation of crytal (Z-direction)
	if zDirect: 
		if zDirect=='001':   
			orient = [[1, 0, 0], [0, 1, 0], [0, 0, 1]] 
		elif zDirect=='110': 
			orient = [[1, -1, 0], [0, 0, -1], [1, 1, 0]]
			Lx,Ly,Lz = round(Lx/sqrt(2)), Ly, round(Lz/sqrt(2)) 
		elif zDirect=='111': 
			orient = [[1, -1, 0], [1, 1, -2], [1, 1, 1,]]
			Lx,Ly,Lz = round(Lx/sqrt(2)), round(Ly/(sqrt(6)/2)), round(Lz/sqrt(3)) 
		elif zDirect=='112': 
			orient = [[-1, -1, 1], [1, -1, 0], [1, 1, 2]] 
			Lx,Ly,Lz = round(Lx/sqrt(3)), round(Ly/sqrt(2)), round(Lz/(sqrt(6)/2))
		else: raise Exception("Crystal orientation is not suitable. zDirect='001'/'110'/'111'/'112' ")

	## Define based on X-direction
	if xDirect: 
		if xDirect=='001' or xDirect=='100':   
			orient = [[1, 0, 0], [0, 1, 0], [0, 0, 1]] 
		elif xDirect=='110': 
			orient = [[1, -1, 0], [0, 0, -1], [1, 1, 0]]
			Lx,Ly,Lz = round(Lx/sqrt(2)), Ly, round(Lz/sqrt(2)) 
		elif xDirect=='111': 
			orient = [[-1, -1, 1], [1, -1, 0], [1, 1, 2]] 
			Lx,Ly,Lz = round(Lx/sqrt(3)), round(Ly/sqrt(2)), round(Lz/(sqrt(6)/2))   
		else: raise Exception("Crystal orientation is not suitable. xDirect='001'/'100'/'110'/'111' ")
	###
	return orient, (Lx,Ly,Lz)
########
