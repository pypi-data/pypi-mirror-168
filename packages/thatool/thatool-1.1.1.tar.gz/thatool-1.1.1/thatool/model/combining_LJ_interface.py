from   math   import sqrt
import pandas as pd

def pair_LJ(dict_group1, dict_group2, 
			unit_style,                   #   'real' or 'metal'
			combining_rule='geometric', 
			pair_style='lj/cut',
			): 
	""" compute parameters (epsilon & sigma) of LJ potential at interface
	Note that in LAMMPS: 'Lorentz_Berthelot'='arithmetic'   https://tinyurl.com/yzpwg2hs
	* Input:
		- dict_group1, dict_group2: Dicts contain sig & eps of each element of 2 surfaces. 
			Must contain keys: 'atom_name', 'type', 'sigma', 'epsilon'
		- unit_style:   'real' or 'metal'
        - combining_rule='arithmetic' (also 'Lorentz_Berthelot')
			+ 'arithmetic'/'Lorentz_Berthelot'
			+ 'geometric'
			+ 'sixthpower'
		- pair_style='lj/cut': pair_style of Lammps  lj/cut/coul/long
		- external_interaction: require
	* Return: 
		- list-of-string: contain pair_coeffs for LAMMPS
	* NOTEs: 
		- energy unit is kcal/mol, but in OPLSaa of Foyer is kJ/mol.
		- types in 2 dict must either completely different or indentical
	
	Ex:	PMMA/h_BN interface
	dict_group1 = {'element':['CT','CT','CT','CT','HC','HC','C_2','O_2','OS','CT','HC'], 
         	'atom_name':['opls_135','opls_136','opls_137','opls_139','opls_140','opls_282','opls_465','opls_466','opls_467','opls_468','opls_469'],
         	'type':[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 
         	'sigma': [3.5, 3.5, 3.5, 3.5, 2.5, 2.42, 3.75, 2.96, 3.0, 3.5, 2.42], 
         	'epsilon':[0.066, 0.066, 0.066, 0.066, 0.03, 0.015, 0.105, 0.21, 0.17, 0.066, 0.015]}
	dict_group2 = {'element':['B','N'], 
			'atom_name':['B','N'],
			'type':[12,13], 
			'sigma': [3.453, 3.365], 
			'epsilon':[0.094988, 0.1448671]}
	combining_LJ(dict_group1, dict_group2, combining_rule='Lorentz_Berthelot', pair_style='lj/cut/coul/long')
    """
	## unit conversion
	if unit_style=="real":
		eng_fact = 1
	elif unit_style=="metal":
		eng_fact = 0.043364115    # kcal/mol  to  eV
	else:
		raise ValueError("unit_styles are supported: 'real' or 'metal'")

	### Create DataFrame from dict 
	d1 = {key:value for key,value in dict_group1.items() if key in ('atom_name','type','sigma','epsilon') }  #filter specific keys in dict
	d2 = {key:value for key,value in dict_group2.items() if key in ('atom_name','type','sigma','epsilon') }
	df1 = pd.DataFrame(d1).drop_duplicates(subset=['type'])   #unique type
	df2 = pd.DataFrame(d2).drop_duplicates(subset=['type'])
	df1.sort_values(['type'], inplace=True)
	df2.sort_values(['type'], inplace=True)
	## Extract same type 
	df2_same = df2[ df2['type'].isin(df1['type']) ]
	df2_diff = df2[ ~df2['type'].isin(df1['type']) ]
	df1_same = df1[ df1['type'].isin(df2['type']) ]
	df1_diff = df1[ ~df1['type'].isin(df2['type']) ]

	### combine LJ
	L = []
	## for atom in df2 same type as df1
	for i,row1 in df1_same.iterrows():
		for j,row2 in df2_same.iterrows():
			type1,type2 = row1['type'], row2['type']
			if type1<=type2:
				name1,name2 = row1['atom_name'], row2['atom_name']
				eps1,eps2   = row1['epsilon'], row2['epsilon']
				sig1,sig2   = row1['sigma'], row2['sigma']
				eps,sig = _compute_LJ_param(combining_rule, eps1, eps2, sig1, sig2)
				L.append('pair_coeff  %i \t%i \t%s  %.6f %.6f \t\t# %s %s' % (type1, type2, pair_style, eps*eng_fact, sig, name1, name2) )
	for i,row1 in df1_diff.iterrows():
		for j,row2 in df2_same.iterrows():
			type1,type2 = row1['type'], row2['type']
			name1,name2 = row1['atom_name'], row2['atom_name']
			eps1,eps2   = row1['epsilon'], row2['epsilon']
			sig1,sig2   = row1['sigma'], row2['sigma']
			eps,sig = _compute_LJ_param(combining_rule, eps1, eps2, sig1, sig2)
			L.append('pair_coeff  %i \t%i \t%s  %.6f %.6f \t\t# %s %s' % (type1, type2, pair_style, eps*eng_fact, sig, name1, name2) )
	
	## for different types	
	for i,row1 in df1.iterrows():
		for j,row2 in df2_diff.iterrows():
			type1,type2 = row1['type'], row2['type']
			name1,name2 = row1['atom_name'], row2['atom_name']
			eps1,eps2   = row1['epsilon'], row2['epsilon']
			sig1,sig2   = row1['sigma'], row2['sigma']
			eps,sig = _compute_LJ_param(combining_rule, eps1, eps2, sig1, sig2)
			L.append('pair_coeff  %i \t%i \t%s  %.6f %.6f \t\t# %s %s' % (type1, type2, pair_style, eps*eng_fact, sig, name1, name2) )
	return L


### define mixing rule
def _lorentz(eps1, eps2, sig1, sig2):
    eps12 = sqrt(eps1 * eps2)
    sig12 = (sig1 + sig2)/2
    return eps12, sig12

def _geometric(eps1, eps2, sig1, sig2):
    eps12 = sqrt(eps1 * eps2)
    sig12 = sqrt(sig1 * sig2)
    return eps12, sig12

def _sixthpower(eps1, eps2, sig1, sig2):
    eps12 = (2*sqrt(eps1*eps2) *pow(sig1,3) *pow(sig2,3)) /(pow(sig1,6) + pow(sig2,6)) 
    sig12 = pow((pow(sig1,6) + pow(sig2,6))/2, 1/6)
    return eps12, sig12

def _compute_LJ_param(combining_rule, eps1, eps2, sig1, sig2):
	if combining_rule=='Lorentz_Berthelot' or combining_rule=='arithmetic':
		eps,sig = _lorentz(eps1, eps2, sig1, sig2)
	elif combining_rule=='geometric':
		eps,sig = _geometric(eps1, eps2, sig1, sig2)
	elif combining_rule=='sixthpower':
		eps,sig = _sixthpower(eps1, eps2, sig1, sig2)
	else: raise Exception('mixing rule is not available. Please choose one of: "Lorentz-Berthelot"/"geometric"/"sixthpower"')
	return eps,sig