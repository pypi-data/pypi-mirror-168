from math import sqrt

def shells_fcc(a):
	"""Compute nearest-neighbor shells for FCC crystal

    Args:
        a (float): lattice constant

    Returns:
        shell(list): 5 nearest-neighbor shells
	"""
	## FCC_shells
	shell_1 = a/sqrt(2)
	shell_2 = a
	shell_3 = a*sqrt(6)/2
	shell_4 = a*sqrt(2)
	shell_5 = a*sqrt(3)

	shell = [shell_1, shell_2, shell_3, shell_4, shell_5]
	return shell

