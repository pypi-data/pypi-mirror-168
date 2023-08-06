import platform, re
from logging     import warning
from glob        import glob
from natsort     import natsorted
import numpy as np
import pandas as pd

""" Module Collect of function to read various data type from TEXT files."""

# =============================================================================
# Function to read data from TEXT files
# =============================================================================
def matrix_auto(file_name, column_line=None, set_column_name=None, comment='#', read_note=False):
	""" Function to read Data that number of values in each line are not equal, ex: p2p binance (missing values)
	This cannot be read by Numpy, Pandas,...

	Args:
		file_name (str): the text file.
		column_line (int, optional): the line to extract column-names. Defaults to None.
		set_column_name (list, optional): Names of columns to extract. Defaults to None.
		comment (str): comment-line mark. Defaults to "#".

	Returns:
		df (pd.DataFrame)
	
	Notes:
		To return 2 lists from list comprehension, it is better (may faster) running 2 separated list comprehensions.
		.strip() function remove trailing and leading space in string.
	"""
	with open(file_name,'r') as f:
		C = f.read().splitlines()          # list-of-strings (string for each line)
	
	if column_line is not None:
		head_line = C.pop(column_line)     # delete column_line from C

	## Separate numeric-part and note-part
	coeff = [line.partition(comment)[0].split() for line in C if line.partition(comment)[0] ]   # list-of-lists (str)
	if not coeff:
		raise ValueError('The input file contains no data: {:s}'.format(file_name) )
	## Creat DataFrame from 2d_list
	df = pd.DataFrame(data=coeff, dtype=float)                  # .astype(float) ; pd.DataFrame(data=coeff, dtype=float);  to_numeric() just applied for 1d

	## extract column-names from column_line
	list_inputs = [column_line, set_column_name]
	if sum([1 for item in list_inputs if item is not None])>1:
		raise ValueError('Must set one of parameters: [column_line, set_column_name] at a time')

	if column_line is not None:
		my_column = head_line.replace('#','').split()     # string --> list
	elif set_column_name is not None:
		my_column = set_column_name
	else:
		my_column = None

	if my_column is not None:
		num_col = df.shape[1]
		if len(my_column) < num_col:
			extra_col = ['c'+str(i+1) for i in range(int(num_col-len(my_column)))]
			my_column += extra_col
		else:
			my_column = my_column[-num_col:]
		##
		df.columns = my_column

	## extract note
	if read_note:
		note  = [line.partition(comment)[-1].strip() for line in C if line.partition(comment)[0] ]          # list (str)
		df['note'] = note       
	return df



def matrix(file_name, column_line=None, set_column_name=None, usecols=None):
	""" Function to read Data that is as a regular matrix.
	The names of columns are exatract based on `set_column_name` or `column_line`.
	If both `set_column_name` and `column_line` are not available, the default column's name is: 0 1 2...

	Args:
		file_name (str): the text file.
		column_line (int, optional): the line to extract column-names. Defaults to None.
		set_column_name (list, optional): Names of columns to extract. Defaults to None.
		usecols (tuple, optional): only extract some columns. Defaults to None.

	Returns:
		df (pd.DataFrame)
	"""
	##=== refine inputs
	if not file_name: Exception('Input file is not found!')

	##==== read data
	if usecols is not None:
		if set_column_name is None:
			raise Exception('Must provide "columnName" for "usecols" ')
		if column_line is not None:
			data = np.loadtxt(file_name, usecols=usecols, skiprows=1)
		else:
			data = np.loadtxt(file_name, usecols=usecols)
	else:
		if column_line is not None:
			data = np.loadtxt(file_name,skiprows=1)
		else:
			data = np.loadtxt(file_name)
	## check dimension of data
	if data.ndim==2:
		num_col = data.shape[1]    # if data is 2d array
	if data.ndim==1:
		raise ValueError('Data is a series, not a matrix')

	##==== Set Column Names (optional Inputs)
	list_inputs = [column_line, set_column_name]
	if sum([1 for item in list_inputs if item is not None])>1:
		raise ValueError('Only one of {} is choose at a time'.format(list_inputs))

	if set_column_name is not None:
		my_column = set_column_name
	elif column_line is not None:  ## extract column-names from column_line
		with open(file_name,'r') as f:
			C = f.read().splitlines()          # list of strings (each line is 1 string)
		## extract column's name
		words = C[column_line].replace('#','').split()  # string --> list
		my_column = words[-num_col:]                    # get last items

	##==== create DataFrame if data is 2d; create Series if data is 1d
	if 'my_column' in locals():                        # check if VAR exist
		df = pd.DataFrame(data=data, columns=my_column)        
	else:                       
		df = pd.DataFrame(data=data)                       
	return df


def logMFD(file_name, dim=1):
	""" Function to read data from LogMFD calculation.

	Args:
		file_name (str): the logmfd.out file.
		dim (int, optional): dimension of LogMFD calulation. Defaults to 1.

	Raises:
		Exception: _description_

	Returns:
		df (pd.DataFrame)
	"""
	## extract column names
	my_column =['MFDstep','Flog','CV_Temp','eta', 'Veta']
	for i in range(dim):
		my_column.extend(['CV'+str(i+1), 'CV'+str(i+1)+'_vel', 'CV'+str(i+1)+'_force'])
	## read data
	df = matrix_auto(file_name)
	df.columns = my_column
	return df




def lammps_var(file_name, var_name=None):
	""" Function to extract variable values from LAMMPS input file.

	Args:
		file_name (str): the text file in LAMMPS input format.
		var_name (list, optional): list of varibalbes to be extracted. Default to None. mean extract all variables.

	Returns:
		ds (pd.Series): pandas Series contains variable in Lammps file
	"""
	##== read data
	with open(file_name,'r') as f:
		C = f.read().splitlines()

	## extract var_names and values
	B = [line.replace('\t',' ') for line in C if 'variable' in line]  # take all lines begins with "variable", and remove '\t'
	if var_name is not None:
		BB = [line for line in B for var in var_name if var in line]   # Nested List Comprehension to flatten a given 2-D matrix : https://www.geeksforgeeks.org/nested-list-comprehensions-in-python/
		varValue = [float(line.split()[3]) if line.split()[2]=='equal' else line.split()[3] for line in BB]
	else:
		var_name = [line.split()[1] for line in B]
		varValue = [float(line.split()[3]) if line.split()[2]=='equal' else line.split()[3] for line in B]

	## create Pandas Series
	ds = pd.Series(data=varValue, index=var_name)
	return ds


def plumed_var(file_name, var_name, block_name=None):
	""" Function to extract variable values from PLUMED input file.

	Args:
		file_name (str): the text file in LAMMPS input format.
		var_name (str): list of keyworks in PLUMED, ex: INTERVAL,...
		block_name (str, optional): block command in Plumed, ex: METAD, LOGMFD. Defaults to None.

	Returns:
		value (float): value of plumed_var.

	Search number: https://stackoverflow.com/questions/15814592/how-do-i-include-negative-decimal-numbers-in-this-regular-expression
	"""
	##== read data
	with open(file_name,'r') as f:
		C = f.read().splitlines()          # list of strings

	## extract block
	if block_name is not None:
		Index1=[i for i,line in enumerate(C) if block_name in line ][0]                # int
		Index2=[i for i,line in enumerate(C) if ('...' in line and i>Index1) ][0]
		C = C[Index1:Index2]

	## extract var_names and values
	A = [line.replace('\t',' ') for line in C if var_name in line]  # take all lines begins with "variable", and remove '\t'
	varString = re.search(var_name + r'.+\d+', A[0])[0]   
	varValue  = float( re.search(r'-?\d+\.\d+|-?\d+', varString)[0] )
	return varValue


def load_data_from_dir(search_key='deform_', file_ext='.txt', read_note=False, recursive=True):
    """ read data from all *.txt files in current and sub-folders.

	Args:
		search_key(str): a string to search file_name.
		file_ext(str): file extension. Default to '.txt'

	Returns:
		ldf (list-of-DataFrame): list of DataFrames.
        labels (list): list of labels
		files (list): list of file_names
	"""
    ## detect OS system to set separater
    if 'Linux' in platform.system():
        sep = '/'
    if 'Windows' in platform.system():
        sep = '\\'
	##
    files = natsorted( glob(''.join(["**/*", search_key, '*', file_ext]), recursive=recursive) )
    if not files: 
        raise ValueError('Files are not found with search_key = {}'.format(search_key))

    ldf    = [matrix_auto(file, column_line=0, read_note=read_note) for file in files]   
    labels = [file.split(sep)[-1].replace(file_ext,'').replace(search_key,'') for file in files]    

    return ldf, labels, files

