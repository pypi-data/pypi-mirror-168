import re
import numpy     as np
import pandas    as pd
from datetime import datetime

### =============================================================================
### LOG file LAMMPS
### =============================================================================
class LmpLogFile:
	""" Create an Object of LOG file.
	
	Args:
		logfile (str): input LOG file

	Returns:
		LmpLogFile Obj

	Attributes:
		.mpi_break (list): list of pd.Dataframe
		.total_time (float): total runtime.
		
	Methods:
		read_log (str): read LOG file

	Notes: 
		run 0 without data
	"""
	def __init__(self, logfile=None):
		"""
		Args:
			logfile: input LOG file

		Examples:  
		    log = LmpLogFile('lammps_RDF/myRDF.txt')
		"""
		##==== optional Inputs 
		if logfile:
			self.read_log(logfile)
		return

	def read_log(self, logfile):
		""" Read LAMMPS logfile 
				logfile  : input LOG file
			*Output:
				self.frame: list of DataFrames (cannot use multi-row-index DataFrame, because some runs have different thermo-properties)
			  """
		with open(logfile,'r') as f:
			C = f.read().splitlines()

		## Extract positions of Thermo-properties blocks
		index = [i for i,line in enumerate(C) if 'MPI task timing breakdown' in line]

		## Extract each block as frame
		my_column = ['Pair','Bond','Kspace','Neigh','Comm','Output','Modify']
		mpis = [None]*len(index)                      # list
		for i,idx in enumerate(index):
			data = [line.split()[4] for line in C[idx+3:idx+10]]
			s = pd.Series(data=data, index=my_column, dtype=float)
			s['CPU'] = float( C[idx-2].split()[0].replace('%','') ) 
			s['Performance'] = None       #  NOTEs: run 0 does not have Performance line     
			if C[idx-3].split() :
				s['Performance'] = float( C[idx-3].split()[-2] )     # timesteps/s		
			
			mpis[i] = s     # create DataSeries

		## Extract total wall
		time = [line.split()[-1] for line in C if 'Total wall time' in line]
		t = datetime.strptime(time[0], '%H:%M:%S')
		total_minute = int(t.strftime("%H"))*60 + int(t.strftime("%M"))        # total time in minute
		
		## Save out put to CLASS's attributes
		self.file_name  = logfile
		self.mpi_break  = mpis         # List of DataFrame
		self.total_time = total_minute  
		return




### =============================================================================
### RDF LAMMPS
### =============================================================================
class LmpRDF:
	""" class to read Radial Distribution Fuction (RDF) file from Lammps compute
	Attributes:
		name        : file name
		frame       : 3d pandas Frame (multi-row-index DataFrame)
		
	Methods:
		ReadRDF       : read RDF file
		AverageRDF    : the Average RDF
	"""
	def __init__(self, file_name):
		""" 
		Args:
			file_name: input RDF file

		Examples:  
			RDF = LmpRDF('lammps_RDF/myRDF.txt')
		"""
		if file_name:
			self.read_RDF(file_name)
		return

	
	def read_RDF(self, file_name):
		""" 
		Args:
			file_name: input RDF file
		"""
		with open(file_name,'r') as f:
			C = f.read().splitlines()              # list-of-strings

		## Extract positions of block
		A = C[3:]
		coeff = [line.split() for line in A if line.split()]            # list-of-lists (str)
		blockIndex=[i for i,line in enumerate(coeff) if len(line)==2 ]
		if not blockIndex:
			raise ValueError('The input file contains no data: {:s}'.format(file_name) )
			
		## Extract each block as frame
		my_cols = C[2].replace('#','').split()
		frames = [None]* (len(blockIndex))
		for i,idx in enumerate(blockIndex):
			if i < (len(blockIndex)-1): 
				data = coeff[ blockIndex[i]+1 : blockIndex[i+1] ]    # convert array of lists to array of arrays
			else: 
				data = coeff[blockIndex[i]+1 : ]  

			frames[i] = pd.DataFrame(data=data, columns=my_cols, dtype=float)  # create DataFrame

		### convert list of dataFrames to multi-index DataFrame
		my_keys = ['fr%s'%i for i in range(len(frames)) ]
		mdf = pd.concat(frames, keys=my_keys)   # multi-index df

		## Save out put to CLASS's attributes
		self.file_name = file_name
		self.frame     = mdf           # List of DataFrame
		return


	def compute_AveRDF(self):
		"""compute average of RDF over all frames
		Returns: 
			df_ave (DataFrame): Average of RDF
		"""
		mdf = self.frame 
		df_ave = mdf.groupby(level=1).mean()     # compute average of histogram over multi-frames
		return df_ave
	##========

class LmpAveChunk:
	""" class to read Radial Distribution Fuction (RDF) file from Lammps compute
	Attributes:
		name        : file name
		frame       : 3d pandas Frame (multi-row-index DataFrame)
		
	Methods:
		ReadRDF       : read RDF file
		AverageRDF    : the Average RDF
	"""
	def __init__(self, file_name):
		""" 
		Args:
			file_name: input RDF file

		Examples:  
			RDF = LmpRDF('lammps_RDF/myRDF.txt')
		"""
		if file_name:
			self.read_AveChunk(file_name)
		return

	
	def read_AveChunk(self, file_name):
		""" 
		Args:
			file_name: input RDF file
		"""
		with open(file_name,'r') as f:
			C = f.read().splitlines()              # list-of-strings

		## Extract positions of block
		A = C[3:]
		coeff = [line.split() for line in A if line.split()]            # list-of-lists (str)
		blockIndex=[i for i,line in enumerate(coeff) if len(line)==3 ]
		if not blockIndex:
			raise ValueError('The input file contains no data: {:s}'.format(file_name) )

		## Extract each block as frame
		my_cols = C[2].replace('#','').split()
		frames = [None]* (len(blockIndex))
		for i,idx in enumerate(blockIndex):
			if i < (len(blockIndex)-1): 
				data = coeff[ blockIndex[i]+1 : blockIndex[i+1] ]    # convert array of lists to array of arrays
			else: 
				data = coeff[blockIndex[i]+1 : ]  

			frames[i] = pd.DataFrame(data=data, columns=my_cols, dtype=float)  # create DataFrame

		### convert list of dataFrames to multi-index DataFrame
		my_keys = ['fr%s'%i for i in range(len(frames)) ]
		mdf = pd.concat(frames, keys=my_keys)   # multi-index df

		## Save out put to CLASS's attributes
		self.file_name = file_name
		self.frame     = mdf           # List of DataFrame
		return


	def compute_AveChunk(self):
		"""compute average of RDF over all frames
		Returns: 
			df_ave (DataFrame): Average of RDF
		"""
		mdf = self.frame 
		df_ave = mdf.groupby(level=1).mean()     # compute average of histogram over multi-frames
		return df_ave
	##========


# =============================================================================
# HISTOGRAM Plumed
# =============================================================================
class PlumHistogram:
	""" Create an Object of DUMP file

	Args:
		name        : file name
		frame       : 3d pandas Frame (multi-row-index DataFrame)
		
	Methods:
		read_histogram       : read Histogram file
		average_histogram    : the Average Histogram
		AreaHisto       : Area under pdf curve
		find_tail()     : find limit of histogram
		find_center()   : find center of histogram
		
	Examples:  
		```python
		RDF = thaFileType.lmp_RDF(file_name='lammps_RDF/myRDF.txt')
		```
	"""
	
	def __init__(self, file_name):
		""" ** Optional Inputs:
				file_name: input RDF file
		Example:  RDF = thaFileType.lmp_RDF(file_name='lammps_RDF/myRDF.txt')
		"""
		if file_name:
			self.read_histogram(file_name)
		return

	def read_histogram(self, file_name):
		""" 
		Args:
			file_name  :  input HISTOGRAM file

		Returns:
			self.frame: multi-row-index DataFrame
		"""
		with open(file_name,'r') as f:
			C = f.read().splitlines()              # a list of strings

		## Extract positions of atoms, and its properties
		findStr = [re.search('#! FIELDS*', elem)  for elem in C]
		index1 = [i for i,v in enumerate(findStr) if v != None]
		findStr = [re.search('#! SET periodic_*', elem)  for elem in C]
		index2 = [i for i,v in enumerate(findStr) if v != None]

		## Extract each block as frame
		my_column = ['grid','hist','dHist']
		frames = [None]*len(index2)                      # list
		for i in range(len(index2)):
			if i < (len(index2)-1): P = C[ (index2[i]+1) : index1[i+1] ]     # list of strings
			else: P = C[ (index2[i]+1) : ]                          
			#--
			P = np.char.split(P)                            # split each elem of P, result is an array of lists
			P = np.vstack(P[:])                             # convert array of lists to array of arrays
			data = P.astype(np.float64)                     # convert str to float
			#--
			frames[i] = pd.DataFrame(data, columns=my_column)  # create DataFrame

		### convert list of dataFrames to multi-index DataFrame
		my_keys = ['fr%s'%i for i in range(len(frames)) ]
		mdf = pd.concat(frames, keys=my_keys)   # multi-index df

		## Save out put to CLASS's attributes
		self.file_name = file_name
		self.frame     = mdf           # List of DataFrame
		return

	def compute_average_histogram(self):
		"""compute average of histogram over all frames
		* Output: df_ave: DataFrame of avergave histogram
		"""
		mdf = self.frame 
		df_ave = mdf.groupby(level=1).mean()     # compute average of histogram over multi-frames
		return df_ave


	def areaHisto(self):
		hist = self.average_histogram()
		x, y = hist['grid'], hist['hist']
		return np.trapz(y, x)
	##-----

	def fit_std_gaussian(self):
		"""Fit the average-histogarm to Standard Gaussian function
		* Output: (amp, miu, sigma): parameters of Gaussian function"""
		from scipy.optimize import curve_fit
		hist = self.average_histogram()
		x, y = hist['grid'], hist['hist']
		##- define Gaussina function
		def std_gaussian(x, amp, miu, sigma):
			return amp * np.exp(-(x-miu)**2 / (2.*sigma**2))
		##--fitting
		params, params_covariance = curve_fit(std_gaussian, x, y)
		return params
	##-----


	def find_tail(self, tol=1e-4, gridSize=1e-6):
		hist = self.average_histogram()
		#-- interpolate xgrid (since X spacing in HISTO compute is large --> need to interpolate to have values at smaller interval)
		xp, yp = hist['grid'], hist['hist']
		if np.all(np.diff(xp) > 0):           # check if xp is increasing or not
			xInter = np.linspace( min(xp), max(xp), num=int( (max(xp)-min(xp))/gridSize) )
			yInter = np.interp(xInter, xp, yp)                                   

		#--find limits
		left_Index = np.where(yInter>tol )[0][0]        # find left_limit of the distribution tail
		right_Index = np.where(yInter>tol )[0][-1]       # find right_limit of the distribution tail
		#--
		left_tail = xInter[left_Index]
		right_tail = xInter[right_Index]
		#--
		return left_tail, right_tail
	##-----

	def find_center(self, gridSize=1e-6):
		hist = self.average_histogram()
		#-- interpolate xgrid (since X spacing in HISTO compute is large --> need to interpolate to have values at smaller interval)
		xp, yp = hist['grid'], hist['hist']
		if np.all(np.diff(xp) > 0):           # check if xp is increasing or not
			xInter = np.linspace( min(xp), max(xp), num=int( (max(xp)-min(xp))/gridSize) )
			yInter = np.interp(xInter, xp, yp)                                   

		#--find Max_value of Histogram
		center_Index = np.where(yInter==np.amax(yInter))[0][0]        # find index of max value
		#--
		Xcenter = xInter[center_Index]
		#--
		return Xcenter
	##-----

	## =========================================================================
	### Compute the probability density function (PDF) --> must input raw data, cannot compute from histogram
