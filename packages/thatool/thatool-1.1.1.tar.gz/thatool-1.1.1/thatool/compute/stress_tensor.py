import numpy as np

def stress_tensor(per_atom_stress_tensor, atomic_volume,unitFac=1):
	"""Compute local pressure/stress
	NOTE: - per_atom_stress_tensor : Nx6 array of the per-atom stress tensor
		  - atomVol    : Nx1 vector of atomVol
		  - inUNIT=['bar','angstrom'], outUNIT=['bar'] --> unitFac=1e-4 for ['GPa'] 
	Return: pressure scalar, Stress tensor """                                                                     
	# refine input
	S = np.array(per_atom_stress_tensor)                                                                       
	# compute stress/pressureure tensor
	Sxx = unitFac*sum(S[:,0])/sum(atomic_volume)
	Syy = unitFac*sum(S[:,1])/sum(atomic_volume)
	Szz = unitFac*sum(S[:,2])/sum(atomic_volume)
	Sxy = unitFac*sum(S[:,3])/sum(atomic_volume)
	Sxz = unitFac*sum(S[:,4])/sum(atomic_volume)
	Syz = unitFac*sum(S[:,5])/sum(atomic_volume)  
	stress_tensor = np.array([Sxx, Syy, Szz, Sxy, Sxz, Syz])
	# static pressureure   
	pressure = -(Sxx + Syy + Szz)/3
	return pressure, stress_tensor  
## --------
