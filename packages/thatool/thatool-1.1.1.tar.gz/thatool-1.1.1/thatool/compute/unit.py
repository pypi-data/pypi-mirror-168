
""" This module to convert unit of some physical properties
	pressure

	Consider to use this module: https://unyt.readthedocs.io/en/stable/usage.html
"""


### From this site: https://www.unitconverters.net/force-converter.html

# class unit():
# 	""""""
# 	def __init__(self):
# 		return



def pressure(key_word='all_key'):
	"""convert unit of pressure
	Pa: Pascal
	atm: standard atmosphere
	at: technical atmosphere

	kgf/cm2 = kg/cm2
	1 Pa = 1 N/m^2
	1 kgf/cm2 = 1

	Args:
		key_word='all_key'

	Returns:
		factor: float, multiply factor of conversion 
		
	Examples:
		Ex: key_word='Pa_atm': convert from Pa (Pascal) to atm (Standard atmosphere)
	"""

	D = {'Pa_atm': 9.86923e-6, 'GPa_atm': 9.86923e3,
		'Pa_bar': 1e-5, 'GPa_bar': 1e4,
		'Pa_mmHg':0.0075006376,
		'Pa_N/m2':1, 'Pa_kgf/m2':0.1019716213,
		'Pa_kgf/cm2':0.0000101972 }

	if key_word=='all_key':
		return D.keys()
	else:
		return D[key_word]
#######


def force(key_word='all_key'):
	"""convert unit of force
	N: Newton
	kgf = m.g: kilogram-force (weight: one kilogram of mass in a 9.80665 m/s2 gravitational field)
	lbf: pound-force
	p: pond

	1 N = 1 J/m    (Work = Force.distance)
	1 kcal = 4184 J = 4184 N.m = 4184.10^10 N.Angstrom
	69.4786 pN = 1 kcal/mol Angstrom.     https://tinyurl.com/yb2gnlhc

	* Input:
		- key_word='all_key'
		Ex: key_word='Pa_atm': convert from Pa (Pascal) to atm (Standard atmosphere)
	* Output:
		factor: float, multiply factor of conversion """

	D = {'N_J/m':1, 'N_kgf':0.1019716213, 'N_lbf':0.2248089431, 'N_p':101.9716213,
	     'N_cal/m':0.2390057361, 'N_cal/A':0.2390057361e-10, 'N_kcal/A':0.2390057361e-13,
		 'N_kcal/(mol.A)':1.4393261854684511e10}
	##
	if key_word=='all_key':
		return D.keys()
	else:
		return D[key_word]
#######

def energy(key_word='all_key'):
	"""convert unit of energy
	J: Joule
	W.h: watt-hour
	cal: calorie (th)
	hp.h: horsepower hour
	eV: electron-volt

	1 J = 1 N.m    (Work = Force.distance)
	1J = 1 W.s

	* Input:
		- key_word='all_key'
		Ex: key_word='Pa_atm': convert from Pa (Pascal) to atm (Standard atmosphere)
	* Output:
		factor: float, multiply factor of conversion 
		
	Notes:
		## convert eV to kcal/mol
		eV2J = 1/unit_convert.energy('J_eV')
		J2Jmol = unit_convert.constant('1/mol')
		kj2kcal = 1/unit_convert.energy('kcal/mol_kJ/mol')
		eV2kcalmol = eV2J * J2Jmol * 1e-3 *kj2kcal
	"""

	D = {'J_cal':0.2390057361, 'J_W.h':0.0002777778, 'J_hp.h':3.725061361E-7, 'J_eV':6.241509e18,
	     'J_erg':1e7, 'J_W.s':1, 'J_N.m':1,
		 'kcal/mol_kJ/mol':4.184,
		 'eV_kcal/mol':23.066061026625206,}
	##
	if key_word=='all_key':
		return D.keys()
	else:
		return D[key_word]
#######

def constant(key_word='all_key'):
	"""list of constants
	Na = 6.02214076e23  (=1/mol): Avogadro number

	* Input:
		- key_word='all_key'
		Ex: key_word='Pa_atm': convert from Pa (Pascal) to atm (Standard atmosphere)
	* Output:
		factor: float, multiply factor of conversion """

	D = {'Avogadro':6.02214076e23, '1/mol':6.02214076e23,
		}
	##
	if key_word=='all_key':
		return D.keys()
	else:
		return D[key_word]
#######