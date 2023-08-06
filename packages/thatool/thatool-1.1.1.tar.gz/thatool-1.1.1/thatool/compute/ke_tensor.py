import numpy as np


def ke_tensor(vx, vy, vz, mass, kb):
	"""Compute Kinetic Energy tensors, and Temp
	NOTE: - vx, vy, vz : 1D vector of components of per-atom velocity
		  - m : 1D vector of atomic mass
		  - inUNIT=['angstrom','ps','amu','eV'], outUNIT=['eV','K']
	Return: Kinetic energy tensor, Kinetic scalar, Temperature scalar"""
	import scipy.constants as sc
	# refine input & convert inUNIT to SI unit
	veloFact=sc.angstrom/sc.pico      # velocity unit A/ps --> m/s
	vx=np.asarray(vx)*veloFact; vy=np.asarray(vy)*veloFact; vz=np.asarray(vz)*veloFact
	m = np.asarray(mass)*sc.atomic_mass  # mass unit amu --> kg
	kb = kb*sc.eV                     # Boltzmann constant in eV/K --> J/K    
	# compute kinetic energy tensor  
	Kxx = (1/2)*np.einsum('i,i,i',m,vx,vx)  # Element-wise multiply, then summing
	Kyy = (1/2)*np.einsum('i,i,i',m,vy,vy)
	Kzz = (1/2)*np.einsum('i,i,i',m,vz,vz)
	Kxy = (1/2)*np.einsum('i,i,i',m,vx,vy)
	Kxz = (1/2)*np.einsum('i,i,i',m,vx,vz)
	Kyz = (1/2)*np.einsum('i,i,i',m,vy,vz)
	KEtensor = np.array([Kxx, Kyy, Kzz, Kxy, Kxz, Kyz])
	# Kinetic energy & Temperature
	KE = Kxx + Kyy + Kzz
	Temp = (2*KE)/ (3*vx.shape[0]*kb)
	# Convert SI unit to outUNIT 
	KEtensor = KEtensor/sc.eV   # energy J --> eV
	KE = KE/sc.eV
	return KEtensor, KE, Temp 
## --------
