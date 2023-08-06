""" This module contains some data for various ForceField. Data obtained from simulation
"""

### ============================================================================
### Class definition
### ============================================================================
## Potential Information
class EAM:
	""" Create an Object (class) of Potential, contain some pre-setup information
	* Attributes:
		atom_symbol         :  
		cutoff          : force cutoff of potential
		force_field  
		* thermal_coeff    : return values thermal expansion coefficients of input Structure
		* Energy barrier Coeff: an estimation of per-atom energy barrier for melting,
					for a system of N atoms  𝐹=𝑓∗𝑁^(2/3) , then perAtom barrier  𝑓=𝐹/𝑁^(2/3)
					This method return f(T)

	* Methods:
		lattice_constant      : compute lattice constant at a specific temperature
	"""

	def __init__(self, atom_symbol, force_field, model_type='BULK', zDirect='001', thickness=20):
		""" atom_symbol         : 'Al', 'Cu',...
			force_field  : 
				'Cu' : 'Mishin-2001'; 'Foiles-1986';...
				'Al' : 'Mishin-1999'; 'Sheng-2011';...
			model_type       : 'BULK' or 'PLATE'
			zDirect         : '001' or '110' or '111' or 
			thickness       : thickness of plate
		"""
				
		### Stored DATA (these data are compute from several simulations, or from papers)
		## Store thermal Expansion Coeff
		thermal_key = model_type +'_' +zDirect +'_' +str(int(thickness))
		D = {}      # a DICT, save lists of 4 coeffs: a0, a1, a2, a3
		## Store Energy barrier Coeff
		melt_barrier_key = model_type +'_' +zDirect
		melt_barrier = {}      # a DICT, save lists of 3 coeffs: a0, a1, a2
		###=====================================================================
		## Al - aluminum
		###=====================================================================
		if atom_symbol=='Al':
			## EAM/alloy Mishin-1999: “Interatomic Potentials for Monoatomic Metals from Experimental Data and Ab Initio Calculations.” Physical Review B 59, no. 5 (February 1, 1999): 3393–3407. https://doi.org/10.1103/PhysRevB.59.3393.
			if force_field=="Mishin1999":
				D["BULK_001_20"]  =[4.04997007, 3.84009733e-05, 4.19452913e-08, -1.0208113e-11]       # bulk Mishin, list
				#--
				D["PLATE_001_20"] =[4.04484, 4.13076E-5, 2.57811E-8, 0.0]       # plates
				D["PLATE_110_20"] =[4.04096, 4.21205E-5, 2.75193E-8, 0.0]
				D["PLATE_111_20"] =[4.04286, 4.34592E-5, 2.6116E-8 , 0.0]
				#--
				Rcut = 6.2872
				#-- Energy barrier
				melt_barrier['BULK_001'] = [ ]

			## EAM/alloy Sheng-2011: “Highly Optimized Embedded-Atom-Method Potentials for Fourteen Fcc Metals.” Physical Review B 83, no. 13 (April 20, 2011): 134118. https://doi.org/10.1103/PhysRevB.83.134118.
			if force_field=="Sheng2011":        
				D['BULK_001_20']  =[4.0182, 8.1345e-5, 5.47912e-8, 0.0]         # bulk Sheng
				#--
				D['PLATE_001_20'] =[4.0102, 8.14177E-5, 4.40013E-8, 0.0]        # plates
				D['PLATE_110_20'] =[4.00746, 8.03704E-5, 4.37293E-8, 0.0]
				D['PLATE_111_20'] =[4.00881, 7.98655E-5, 4.38535E-8, 0.0]
				#--
				D['PLATE_001_10'] =[4.00266, 8.21097E-5, 3.28338E-8, 0.0]       # thickness
				D['PLATE_001_30'] =[4.01282, 8.11224E-5, 4.77366E-8, 0.0]  
				#--
				Rcut = 6.5
				#-- Energy barrier
				melt_barrier['BULK_001'] = [ ]

			## EAM/alloy LiuEA-2004: “Aluminium Interatomic Potential from Density Functional Theory Calculations with Improved Stacking Fault Energy.” Modelling and Simulation in Materials Science and Engineering 12, no. 4 (July 1, 2004): 665–70. https://doi.org/10.1088/0965-0393/12/4/007.
			if force_field=="LiuEA2004":
				D['BULK_001_20']  = [4.0322638, 8.4429757e-05, -8.0313660e-08, 8.5394862e-11]       # bulk, list 
				#--
				D['PLATE_001_20'] = [4.0252071, 8.6235182e-05, -8.3757835e-08, 8.2616613e-11]      # plates
				#--
				Rcut = 6.063063461624161
				#-- Energy barrier
				melt_barrier['BULK_001'] = [ ]

			## EAM/fs Mendelev-2008: “Aluminium Interatomic Potential from Density Functional Theory Calculations with Improved Stacking Fault Energy.” Modelling and Simulation in Materials Science and Engineering 12, no. 4 (July 1, 2004): 665–70. https://doi.org/10.1088/0965-0393/12/4/007.
			if force_field=="Mendelev2008":
				D['BULK_001_20']  = [4.0454689, 1.0336804e-04, -4.4466155e-08, 4.4632912e-11]     # bulk, list
				D['PLATE_001_20'] = [4.0347989, 1.0792948e-04, -5.5895577e-08, 5.0793506e-11]
				#--
				Rcut = 6.5
				#-- Energy barrier
				melt_barrier['BULK_001'] = [ ]
	
			## EAM/fs Sturgeon-Laird_2000: 10.1103/PhysRevB.62.14720
			if force_field=="Laird2000":
				D['BULK_001_20']  = [4.04974777, 8.71969537e-05, -1.07367764e-08, 4.41772347e-11]     # bulk, list  
				#--
				D['PLATE_001_20'] =[4.0394702, 8.4161598e-05, -2.7853137e-09, 3.0159885e-11]        # plates
				D['PLATE_110_20'] =[4.0458061, 7.8232577e-05, 1.4048605e-08, 2.4295087e-11]
				D['PLATE_111_20'] =[4.0473768, 8.0597649e-05, 6.2126772e-09, 3.1094408e-11]				#--
				Rcut = 5.58441
				#-- Energy barrier
				melt_barrier['BULK_001'] = [ 2.50031245e+00, -4.31427372e-03,  1.85953745e-06]
				
		###=====================================================================
		## Cu - Copper
		###=====================================================================
		elif atom_symbol=='Cu':
			## EAM/alloy Mishin-2001: “Structural Stability and Lattice Defects in Copper: Ab Initio, Tight-Binding, and Embedded-Atom Calculations.” Physical Review B 63, no. 22 (May 21, 2001): 224106. https://doi.org/10.1103/PhysRevB.63.224106.
			if force_field=="Mishin2001":
				D['BULK_001_20']  = [3.6149674, 5.4768017e-05, 4.5114050e-09, 5.3555179e-12]       # Bulk
				#--
				D['PLATE_001_20'] = [3.6028054, 5.2949511e-05, 6.4528673e-09, 1.3428405e-12]       # plates
				#--
				Rcut = 5.506786
				#-- Energy barrier
				melt_barrier['BULK_001'] = [ ]
				
			## EAM/alloy Foiles-1986: “Embedded-Atom-Method Functions for the Fcc Metals Cu, Ag, Au, Ni, Pd, Pt, and Their Alloys.” Physical Review B 33, no. 12 (June 15, 1986): 7983–91. https://doi.org/10.1103/PhysRevB.33.7983.
			if force_field=="Foiles1986":  # NOT YET define
				# D['BULK_001_20']  =[0.0, 0.0, 0.0, 0.0]       # Bulk
				#--
				# D['PLATE_001_20'] =[0.0, 0.0, 0.0, 0.0]       # plates
				#--
				Rcut = 4.9499999999999886
				#-- Energy barrier
				melt_barrier['BULK_001'] = [ ]

			## EAM/fs Mendelev-2008: https://doi.org/10.1080/14786430802206482
			if force_field=="Mendelev2008":
				D['BULK_001_20']  = [3.6388550, 3.8132546e-05, 9.2355518e-09, -3.7569368e-12]       # Bulk
				#--
				D['PLATE_001_20'] = []       # plates
				#--
				Rcut = 6.0
				#-- Energy barrier
				melt_barrier['BULK_001'] = [3.79342593e+00, -4.51230909e-03,  1.34052708e-06]   # need to modify for Cu


		###=====================================================================
		## Ag - Silver
		###=====================================================================
		elif atom_symbol=='Ag':
			## EAM/alloy Foiles-1986: “Embedded-Atom-Method Functions for the Fcc Metals Cu, Ag, Au, Ni, Pd, Pt, and Their Alloys.” Physical Review B 33, no. 12 (June 15, 1986): 7983–91. https://doi.org/10.1103/PhysRevB.33.7983.
			if force_field=="Foiles1986":
				D['BULK_001_20']  = [4.0898248, 8.0310190e-05, -7.8616810e-10, 1.6850832e-11]       # Bulk
				#--
				D['PLATE_001_20'] = [4.0814423, 7.8061255e-05, -6.8120411e-10, 1.6416544e-11]       # plates
				#--
				Rcut = 5.55
				#-- Energy barrier
				melt_barrier['BULK_001'] = [ ]

		###=====================================================================
		## V - Vanadium
		###=====================================================================
		elif atom_symbol=='V':
			## EAM/alloy Olsson-2009: https://doi.org/10.1016/j.commatsci.2009.06.025
			if force_field=="Olsson2009":
				D['BULK_001_20']  = [3.0299999, 0, -0, 0]       # Bulk
				#--
				D['PLATE_001_20'] = []       # plates
				#--
				Rcut = 4.545
				
		###=====================================================================
		## LJ - Lenard-Jones
		###=====================================================================
		elif atom_symbol=='LJ':
			## LJ - BingQing2015: Cheng, Bingqing “Solid-Liquid Interfacial Free Energy out of Equilibrium.” Physical Review B 92, no. 18 (November 9, 2015): 180102. https://doi.org/10.1103/PhysRevB.92.180102.
			if force_field=="BingQing-2015":
				D['BULK_001_20'] =[1.50894, 0.352843, -0.582519, 0.479193]
				
		else: raise Exception("No Data is found for the atom_symbol")


		###=====================================================================
		## Set Attributes
		###=====================================================================
		self.atom_symbol = atom_symbol
		self.force_field = force_field

		self.thermal_coeff = D[thermal_key]
		self.cutoff = Rcut
		self.melt_barrierCoeff = melt_barrier[melt_barrier_key]
	####---------- End init --------------
	
	def lattice_constant(self, Temp):
		c = self.thermal_coeff
		return c[0] + c[1]*Temp + c[2]*Temp**2 + c[3]*Temp**3       # lattice constant
	##-----

	def atomic_volume_FCC(self, Temp):
		a = self.lattice_constant(Temp)
		return (a**3) /4                    # atomicVolume of FCC
	##-----

	def melt_barrier(self, Temp):
		"for a system of N atoms  𝐹=𝑓∗𝑁^(2/3) , then perAtom barrier  𝑓=𝐹/𝑁^(2/3). This method return f(T)"
		c = self.melt_barrierCoeff
		perAtom_deltaF = c[0] + c[1]*Temp + c[2]*Temp**2 
		return perAtom_deltaF 
	##-----
### =======================  End Class  ========================================

class ReaxFF:
	""" Create an Object (class) of Potential, contain some pre-setup information
	* Attributes:
		atom_symbol         :  
		force_field  
		* thermal_coeff    : return values thermal expansion coefficients of input Structure
		* Energy barrier Coeff: an estimation of per-atom energy barrier for melting,
					for a system of N atoms  𝐹=𝑓∗𝑁^(2/3) , then perAtom barrier  𝑓=𝐹/𝑁^(2/3)
					This method return f(T)

	* Methods:
		lattice_constant      : compute lattice constant at a specific temperature
	"""

	def __init__(self, atom_symbol, force_field, model_type='BULK', zDirect='001'):
		""" atom_symbol         : 'V2O5',...
			force_field  : 
				'V2O5' : 'Chenoweth2008';...
			model_type       : 'BULK' or 'PLATE'
			zDirect         : '001' 
		"""
				
		### Stored DATA (these data are compute from several simulations, or from papers)
		## Store thermal Expansion Coeff
		thermal_key = model_type +'_' +zDirect
		D = {}      # a DICT, save 2d_lists of 4 coeffs: a0, a1, a2, a3
		## Store Energy barrier Coeff
		melt_barrier_key = model_type +'_' +zDirect
		melt_barrier = {}      # a DICT, save lists of 3 coeffs: a0, a1, a2
		###=====================================================================
		## V2O5 - diVanadium Pentoxide
		###=====================================================================
		if atom_symbol=='V2O5':
			## EAM/alloy Mishin-1999: “Interatomic Potentials for Monoatomic Metals from Experimental Data and Ab Initio Calculations.” Physical Review B 59, no. 5 (February 1, 1999): 3393–3407. https://doi.org/10.1103/PhysRevB.59.3393.
			if force_field=="Chenoweth2008":
				D['BULK_001']  =[[11.4557293, -8.02831976e-06, 1.90213969e-07, -1.01234191e-10],
								 [3.43598733, -2.40843947e-06, 5.70529549e-08, -3.03642684e-11],
								 [4.78034085, -3.34752452e-06, 7.93687377e-08, -4.22410049e-11]]       # bulk Mishin, list
				#--
				Rcut = None
				#-- Energy barrier
				melt_barrier['BULK_001'] = [ ]
			

		###=====================================================================
		## Set Attributes
		###=====================================================================
		self.atom_symbol = atom_symbol
		self.force_field = force_field

		self.thermal_coeff = D[thermal_key]
		self.cutoff = Rcut
		self.melt_barrierCoeff = melt_barrier[melt_barrier_key]
	####---------- End init --------------
	
	def lattice_constant(self, Temp):
		t = self.thermal_coeff
		a = t[0][0] + t[0][1]*Temp + t[0][2]*Temp**2 + t[0][3]*Temp**3
		b = t[1][0] + t[1][1]*Temp + t[1][2]*Temp**2 + t[1][3]*Temp**3
		c = t[2][0] + t[2][1]*Temp + t[2][2]*Temp**2 + t[2][3]*Temp**3

		return [a,b,c]      # lattice constant
	##-----

### =======================  End Class  ========================================

