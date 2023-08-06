import pandas 	     as pd
import numpy 	     as np
from ..io 	         import read_data


## compute Replica_MD_Average
def replica_MD_average(MD_out_files):
	""" compute Replica_MD_Average from output of MD.
	Requisites:
	1. Replica_* files from separate MD simulations

	* Inputs-Compulsory: <br>
		- MD_out_files: |`list`| of "MDout_replica.txt" files
	* Outputs: <br>
		- logPD file: contains logPD-based MeanForce
	* Usage: <br>
		thaFreeEnergy.replica_MD_average(MD_out_files)

	Cao Thang, Jul2020 (update: Sep 2021)
	"""
	## Inputs Compulsory:
	if (not MD_out_files): raise Exception('List of input files if empty, please check it!')

	list_df = [read_data.matrix_auto(file, column_line=0) for file in MD_out_files]    #list of DataFrames (each DF for each Replica)
    ## =============================================================================
    ## Compute The average over all replicas:  Average = sum_Repl / N_Repl
    ## =============================================================================
    ## compute Average Energy
	list_ds = [ pd.Series(df['Pe'].values, index=df['Timestep'].values)  for df in list_df]     # list-of-Series
	tmp = pd.concat(list_ds, axis=1)                                                        # each series is each column of df
	avePE = tmp.mean(axis=1)
	stdPE = tmp.std(axis=1)

    ## compute Average Volume
	list_ds = [ pd.Series(df['Lx'].values*df['Ly'].values*df['Lz'].values, index=df['Timestep'].values)  for df in list_df]
	tmp = pd.concat(list_ds, axis=1)
	aveVOL = tmp.mean(axis=1)
	stdVOL = tmp.std(axis=1)

    ## compute Average XY Area (use for Plate only)
	list_ds = [ pd.Series(df['Lx'].values*df['Ly'].values, index=df['Timestep'].values)  for df in list_df]
	tmp = pd.concat(list_ds, axis=1)
	aveAREA = tmp.mean(axis=1)
	stdAREA = tmp.std(axis=1)

	## =============================================================================
	## Write Output to file
	## =============================================================================
	step = pd.Series( list_df[0]['Timestep'].values, index=list_df[0]['Timestep'].values )
	myList = [step.rename('#Timestep'), avePE.rename('avePE'), aveVOL.rename('aveVOL'), aveAREA.rename('aveAREA'),
				stdPE.rename('stdPE'), stdVOL.rename('stdVOL'), stdAREA.rename('stdAREA')]
	df = pd.concat(myList, axis=1)   # list-of-Series to df
	##
	# df.rename(columns={'Timestep': '#Timestep'}, inplace=True)          # remame columns
	df.to_csv('Replica_PropertyAverage.out', index=False, sep='\t', float_format='%.7g', na_rep=np.NaN)
	return
	########
