import numpy as np


def angle_vector2vectors(fixVector, arrayVectors, unit='rad'):
	"""copmute angles between a vector with set of vectors"""
	fixVector = np.asarray(fixVector)
	arrayVectors = np.asarray(arrayVectors)
	##--
	dot_Vec = np.einsum('ij,j->i', arrayVectors, fixVector )       # dot product
	norm_Vec = np.linalg.norm(arrayVectors, axis=1) *np.linalg.norm(fixVector)
	AngCosine = dot_Vec/norm_Vec
	AngCosine[AngCosine>=1] = 1-1e-32     # to void singular in np.arccos
	AngCosine[AngCosine<=-1] = -1+1e-32
	##--
	if unit=='rad': ang = np.arccos(AngCosine)
	elif unit=='deg': ang = np.arccos(AngCosine) *180/np.pi
	else: raise Exception("Choose Unit: 'rad' or 'deg' ")
	return ang
	##--------







