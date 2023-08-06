import numpy as np

def unique_row(X, tol_decimal=2):
	"""find match_indices & mismatch_indices of arr(find_rows) in arr(X), return indices of X
	X, find_rows    : NxN numpy arrays
	tol_decimal : number of digits for round off input data
	"""
	# round off input data (trim float number)
	X = np.asarray(X);    
	X1 = np.round(X, decimals=tol_decimal)
	##
	_, uniIndex = np.unique(asvoid(X1), return_index=True)
	uniqueX = X[uniIndex]
	
	return uniqueX, uniIndex
##--------


def match_row(X, find_rows, tol_decimal=2):
	"""find match_indices & mismatch_indices of arr(find_rows) in arr(X), return indices of X
	  X, find_rows    : NxN numpy arrays
	  tol_decimal : number of digits for round off input data
	"""
	## make inputs as numpy-array 
	X = np.asarray(X);    find_rows = np.asarray(find_rows);  
	# round off input data (trim float number)
	X = np.round(X, decimals=tol_decimal)
	find_rows = np.round(find_rows, decimals=tol_decimal)
	##
	bool_elem = np.in1d(asvoid(X), asvoid(find_rows))   # boolean index
	match_index = np.flatnonzero(bool_elem)
	mismatch_index = np.flatnonzero(~bool_elem)
	
	return match_index, mismatch_index
##--------



def asvoid(arr):              # to view each row of array(arr) as a single value of void dtype
	""" Base on: https://stackoverflow.com/questions/38674027/find-the-row-indexes-of-several-values-in-a-numpy-array
	"""   
	arr = np.ascontiguousarray(arr)
	if np.issubdtype(arr.dtype, np.floating):
		arr += 0. 
	new_dtype = np.dtype((np.void, arr.dtype.itemsize * arr.shape[-1]))
	return arr.view(new_dtype)       # is (arr.shape[0],1) array
##--------
