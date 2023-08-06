# import sys, re, glob, types
import thaModel, thaTool, thaFileType
import numpy as np
import pandas as pd


### ============================================================================
### Class definition
### ============================================================================
## Potential Information
class LogMFD_FCCUBIC:
	""" Create an Object (class) of Potential, contain some pre-setup information for Energy barrier for LogMFD calculation
	NOTEs: Energy barrier of System does not depend on CV (same value for energy CV: meanCV, nAtomLiquid,...)
	* Attributes:
		Element         :  
		Cutoff          : force cutoff of potential
		Potential_Name  :
		* Energy barrier Coeff: an estimation of per-atom energy barrier for melting,
					for a system of N atoms  𝐹=𝑓∗𝑁^(2/3) , then perAtom barrier  𝑓=𝐹/𝑁^(2/3)
					This method return f(T)
		* histo_point_coeff: the CV-value at which histogram of solid and liquid meets, coeff of function f(T) = a0 + a1T

	* Methods:
		Latt_Const      : compute lattice constant at a specific temperature
	"""

	def __init__(self, Element, Potential_Name, modelType='Bulk', zDirect='001'):
		""" Element         : 'Al', 'Cu',...
			Potential_Name  : 
				'Cu' : 'Mishin-2001'; 'Foiles-1986';...
				'Al' : 'Mishin-1999'; 'Sheng-2011';...
			modelType       : 'Bulk' or 'Plate'
			zDirect         : '001' or '110' or '111' or 
			thickness       : thickness of plate
		"""
				
		### Stored DATA (these data are compute from several simulations, or from papers)
		## Store Energy barrier Coeff
		melt_barrier_key = modelType +'_' +zDirect
		melt_barrier_coeff = {}      # a DICT, save lists of 3 coeffs: a0, a1, a2
		###=====================================================================
		## Al - aluminum
		###=====================================================================
		if Element=='Al':
			## EAM/alloy Mishin-1999: “Interatomic Potentials for Monoatomic Metals from Experimental Data and Ab Initio Calculations.” Physical Review B 59, no. 5 (February 1, 1999): 3393–3407. https://doi.org/10.1103/PhysRevB.59.3393.
			if Potential_Name=="Mishin1999":
				melt_barrier_coeff['Bulk_001']     = [ ]
				melt_barrier_coeff['Plate_001_20'] = []       # plates

			## EAM/alloy Sheng-2011: “Highly Optimized Embedded-Atom-Method Potentials for Fourteen Fcc Metals.” Physical Review B 83, no. 13 (April 20, 2011): 134118. https://doi.org/10.1103/PhysRevB.83.134118.
			if Potential_Name=="Sheng2011":        
				melt_barrier_coeff['Bulk_001']     = [ ]
				melt_barrier_coeff['Plate_001_20'] = []       # plates

			## EAM/alloy LiuEA-2004: “Aluminium Interatomic Potential from Density Functional Theory Calculations with Improved Stacking Fault Energy.” Modelling and Simulation in Materials Science and Engineering 12, no. 4 (July 1, 2004): 665–70. https://doi.org/10.1088/0965-0393/12/4/007.
			if Potential_Name=="LiuEA2004":
				melt_barrier_coeff['Bulk_001']     = [ ]
				melt_barrier_coeff['Plate_001_20'] = []       # plates

			## EAM/fs Mendelev-2008: “Aluminium Interatomic Potential from Density Functional Theory Calculations with Improved Stacking Fault Energy.” Modelling and Simulation in Materials Science and Engineering 12, no. 4 (July 1, 2004): 665–70. https://doi.org/10.1088/0965-0393/12/4/007.
			if Potential_Name=="Mendelev2008":
				melt_barrier_coeff['Bulk_001']     = [ ]
				melt_barrier_coeff['Plate_001_20'] = []       # plates

			## EAM/fs Sturgeon-Laird_2000: 10.1103/PhysRevB.62.14720
			if Potential_Name=="Laird2000":
				melt_barrier_coeff['Bulk_001'] = [ 2.50031245e+00, -4.31427372e-03,  1.85953745e-06]
				histo_point_coeff = [0.8518212774963803, -0.00043274594790159045]
				
		###=====================================================================
		## Cu - Copper
		###=====================================================================
		elif Element=='Cu':
			## EAM/alloy Mishin-2001: “Structural Stability and Lattice Defects in Copper: Ab Initio, Tight-Binding, and Embedded-Atom Calculations.” Physical Review B 63, no. 22 (May 21, 2001): 224106. https://doi.org/10.1103/PhysRevB.63.224106.
			if Potential_Name=="Mishin2001":
				melt_barrier_coeff['Bulk_001']     = [ ]
				melt_barrier_coeff['Plate_001_20'] = []       # plates
				
			## EAM/alloy Foiles-1986: “Embedded-Atom-Method Functions for the Fcc Metals Cu, Ag, Au, Ni, Pd, Pt, and Their Alloys.” Physical Review B 33, no. 12 (June 15, 1986): 7983–91. https://doi.org/10.1103/PhysRevB.33.7983.
			if Potential_Name=="Foiles1986":  # NOT YET define
				melt_barrier_coeff['Bulk_001']     = [ ]
				melt_barrier_coeff['Plate_001_20'] = []       # plates

			## EAM/fs Mendelev-2008: https://doi.org/10.1080/14786430802206482
			if Potential_Name=="Mendelev2008":
				melt_barrier_coeff['Bulk_001'] = [3.79342593e+00, -4.51230909e-03,  1.34052708e-06]   # need to modify for Cu


		###=====================================================================
		## Ag - Silver
		###=====================================================================
		elif Element=='Ag':
			## EAM/alloy Foiles-1986: “Embedded-Atom-Method Functions for the Fcc Metals Cu, Ag, Au, Ni, Pd, Pt, and Their Alloys.” Physical Review B 33, no. 12 (June 15, 1986): 7983–91. https://doi.org/10.1103/PhysRevB.33.7983.
			if Potential_Name=="Foiles1986":
				melt_barrier_coeff['Bulk_001']     = [ ]


		###=====================================================================
		## V - Vanadium
		###=====================================================================
		elif Element=='V':
			## EAM/alloy Olsson-2009: https://doi.org/10.1016/j.commatsci.2009.06.025
			if Potential_Name=="Olsson2009":
				melt_barrier_coeff['Bulk_001']     = [ ]

		###=====================================================================
		## Set Attributes
		###=====================================================================
		self.Element = Element
		self.Potential_Name = Potential_Name

		self.melt_barrier_coeff = melt_barrier_coeff[melt_barrier_key]
		self.histo_point_coeff = histo_point_coeff
	####---------- End init --------------
	

	def meltingBarrier(self, Temp):
		"for a system of N atoms  𝐹=𝑓∗𝑁^(2/3) , then perAtom barrier  𝑓=𝐹/𝑁^(2/3). This method return f(T)"
		c = self.melt_barrier_coeff
		perAtom_deltaF = c[0] + c[1]*Temp + c[2]*Temp**2 
		return perAtom_deltaF 
	##-----

	def histo_point(self, Temp):
		"Value of CV at intersection point of histogram as function y = a + bx"
		a = self.histo_point_coeff
		value_CV = a[0] + a[1]*Temp 
		return value_CV 
	##-----
### =======================  End Class  ========================================


### ============================================================================
### Functions definition
### ============================================================================
