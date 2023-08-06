import pandas 	     as pd
import numpy 	     as np
from ..io 	         import read_data
from scipy.integrate import cumulative_trapezoid


## compute LogPD-based MeanForce
def replica_logPD_intergration(logmfd_files, replica_files, beta=1.0):
	""" The **function** to compute LogPD-based MeanForce
	Ref: <br>
	[1].https://pubs.acs.org/doi/10.1021/acs.jctc.7b00252 Free Energy Reconstruction from Logarithmic Mean-Force Dynamics Using Multiple Nonequilibrium TrajectoriesFree
	[2] Exp-normalize trick: https://timvieira.github.io/blog/post/2014/02/11/exp-normalize-trick/

	NOTEs: About the printed values in <replica.out> and <logmfd.out> as reply from Tetsuya Morishita
	```
	<logmfd.out>
	1:iter_md, 2:Flog(t), …, 6: X(t), 7: V(t), 8: Force(t)
	1   F(1), …, X(1), V(1), Force(0)
	2   F(3), …, X(2), V(2), Force(1)

	<replica.out>
	iter_md, work, weight, cv
	1  work(1)   weight(1)  cv(0)
	2  work(2)   weight(2)  cv(1)
	```
	Requisites:
	1. Run logMFD simulations to produce "replica_*/logmfd.out" and "replica_*/replica.out"

	Cao Thang, Jul2020 (update: Sep 2021)

	Args:
		logmfd_files (list): list of "logmfd.out" files
		replica_files (list): list of "replica.out" files
		beta (float, optional):  kB is Boltzmann constant (can be set to 1.0, regardless of kB unit)
			beta = 1.0/(TEMP*kB)

	Returns:
		logPD file: contains logPD-based MeanForce

	Examples:
		```python
		thatool.free_energy.replica_logPD_intergration(logmfd_files, replica_files)
		```
	"""
	## compute BETA-temperature
	# TEMP	= logmfd[0].loc[0,'CV_Temp']
	# beta    = 1.0/(TEMP*kB)

	## Inputs Compulsory:
	if (not logmfd_files) or (not replica_files):
		raise Exception('List of input files if empty, please check it!')
	## =============================================================================
	## Load data files from replica_* files
	## =============================================================================
	logmfd1  =[read_data.logMFD(file, dim=1) for file in logmfd_files]   #list of DataFrames (each DF for each Replica)
	replica1 =[read_data.matrix_auto(file, set_column_name=['MFDstep','work','weight','CV1']) for file in replica_files]

	## check input data & trim length of DataFrames
	myROW = min([df.shape[0] for df in logmfd1])
	logmfd = [df.head(myROW) for df in logmfd1]
	replica = [df.head(myROW) for df in replica1]

	## =============================================================================
	## Compute LogPD-based Mean-Force
	## =============================================================================
	### 1. Compute Weight, using Eq.(17) in Ref [1]
	## Way1: fast, but overflow encountered in exp
	# betaWork = [np.exp(-beta*elem['work']) for elem in replica]    # list-of-Series (each for each Replica);
	# sumReplica = sum(betaWork)                                     # sum list-of-Series --> Series (sum of all Replicas)
	# Weight =[elem/sumReplica for elem in betaWork]                 # list-of-Series (each series for each replica)

	## Way2: Use Exp-normalize trick to avoid overflow encountered in exp
	## compute Weight, using Eq.(17) in Ref [1]
	tmpList2d = [[None] *len(replica)] *len(replica[0].index)    # list-of-lists (each row for each replica)
	for i in range(len(replica[0].index)):                       # each MFD step
		w = np.asarray([r.iloc[i]['work'] for r in replica])         # list, work in each replica at MFD-step i
		tmp = -beta*min(w)                                           # normalize number to avoid overflow encountered in exp, see Ref. [2]
		Wl = np.exp(-beta*w -tmp)  /sum( np.exp(-beta*w -tmp) )      # Eq.(17); weight of each replica at MFD-step i
		tmpList2d[i][:] = Wl
	## convert list-of-lists to list-of-series (need transpose 2d-list)
	arrayT = np.asarray(tmpList2d).T                    # transpose 2d-list
	Weight = [pd.Series(r) for r in arrayT.tolist() ]   # list-of-lists to list-of-series

	### 2. Compute logPD Mean-Force, using Eq.(16) in Ref [1]
	Force = [elem['CV1_force'].shift(-1) for elem in logmfd ]                 # Shift the value of Col:Force(t) in <logmfd.out>
	Weight_Force = [Weight[l]*Force[l] for l in range(len(Weight))]           # list-of-Series (each series for each replica)
	PDMeanForce = sum(Weight_Force)                                           # Eq.(16);   Sum(list-of-Series) --> Series

	## =============================================================================
	## Integration Potential of Mean-Force
	## =============================================================================
	initPMF	= round(logmfd[0].loc[0,'Flog'], 1)
	PMF = cumulative_trapezoid(-PDMeanForce,logmfd[0]['CV1'],initial=0)
	PMF = PMF + initPMF

	## =============================================================================
	## Write Output to file
	## =============================================================================
	myList = [logmfd[0]['MFDstep'], pd.Series(PMF, name='Flog'), logmfd[0]['CV1'], logmfd[0]['CV1_vel'], logmfd[0]['CV_Temp'], pd.Series(PDMeanForce, name='PDforce')]
	df = pd.concat(myList, axis=1)   # list-of-Series to df
	##
	df.rename(columns={'MFDstep': '#MFDstep'}, inplace=True)          # remame columns
	df.to_csv('LogPD.out', index=False, sep='\t', float_format='%.8f', na_rep=np.NaN)
	return
