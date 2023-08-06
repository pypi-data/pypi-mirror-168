import numpy as np

def detect_sign_change(y, x=[]):
	"""determine points where line y=y(x) change its sign
	* Compulsory inputs: 
		y: Nx1 arrays, contains dependent variable y
		x: (Optinal) Nx1 arrays, contains independent variable x of line y(x)
	* Output:
		idx: 1d array of indices where sign changes
	"""
	##-- compute derivative y'(x)
	if not(list(x)): d = np.gradient(y,1)
	else: d = np.gradient(y,x)
	## detect sign change
	idx = np.where( np.sign(d[:-1]) != np.sign(d[1:]) )[0] + 1
	return idx
	##--------