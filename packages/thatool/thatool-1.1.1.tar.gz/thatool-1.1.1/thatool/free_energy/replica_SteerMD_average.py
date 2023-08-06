import pandas 	    as pd
import numpy 	    as np
from ..io 	        import read_data


def exp_normalize(x):
    b = x.max()
    y = np.exp(x - b)
    return y / y.sum()

def read_df(file,engine='LAMMPS'):
    "define lamda(x)"
    df = read_data.matrix_auto(file, column_line=0)
    if 'PLUMED' in engine:
        df.rename(columns = {'smd.d.z_cntr':'ideal_CV', 'd.z':'real_CV', 'smd.force2':'force2', 'smd.work':'work'}, inplace = True)
    return df

## compute Replica_MD_Average
def replica_SteerMD(SteerMD_files, beta=1.0, engine='Lammps'):
    """ compute Average Work from output of SteerMD.
    REf: [1]. https://github.com/sandeshkalantre/jarzynski/blob/master/code/Simulations%20on%20Harmonic%20Oscillator%20Model.ipynb
            [2]. https://www.plumed.org/doc-v2.6/user-doc/html/belfast-5.html#belfast-5-work
            [3] Exp-normalize trick: https://timvieira.github.io/blog/post/2014/02/11/exp-normalize-trick/

    Requisites:
    1. Replica_* files from separate MD simulations

        * Inputs-Compulsory: <br>
            - SteerMD_files: |`list`| of "SteerMD.txt" files
            - beta = 1.0/(TEMP*kB):  kB is Boltzmann constant (can be set to 1.0, regardless of kB unit)
            - engine='LAMMPS'/'PLUMED'
        * Outputs: <br>
            - aveSteerMD file: contains logPD-based MeanForce
        * Usage: <br>
            thaFreeEnergy.replica_SteerMD_average(SteerMD_files)

    Cao Thang, Jul2020 (update: Mar 2022)
    """
    ## Inputs Compulsory:
    if (not SteerMD_files): raise Exception('List of input files if empty, please check it!')

    ## read file
    list_df = [read_df(file,engine) for file in SteerMD_files]    #list of DataFrames (each DF for each Replica)

    ## check input data & trim length of DataFrames
    myROW = min([df.shape[0] for df in list_df])
    steer_ldf = [df.head(myROW) for df in list_df]

    ## =============================================================================
    ## Compute The average over all replicas:  Average = sum_Repl / N_Repl
    ## =============================================================================
    ## compute Average Energy
    list_ds = [np.exp(-beta*df['work'])  for df in steer_ldf]                  # list-of-Series
    tmp = pd.concat(list_ds, axis=1)                               # each series is each column of df
    aveWork = -1.0/beta * np.log(tmp.mean(axis=1))

    ## compute Average force
    aveforce = np.gradient(aveWork, steer_ldf[0]['ideal_CV'])   # derivative of work
    aveforce = pd.Series(aveforce, index=steer_ldf[0].index)    # convert to series

    ## compute Average real_CV
    list_ds = [df['real_CV']  for df in steer_ldf]                  # list-of-Series
    tmp = pd.concat(list_ds, axis=1)
    ave_real_CV = tmp.mean(axis=1)
    ## =============================================================================
    ## Write Output to file
    ## =============================================================================
    myList = [steer_ldf[0]['time'], aveforce, aveWork, ave_real_CV, steer_ldf[0]['ideal_CV']]     # list-of-Series
    df = pd.concat(myList, axis=1)                            # list-of-Series to df
    df = pd.DataFrame(df.values, columns=['#time', 'force', 'work', 'real_CV', 'ideal_CV'])     # to set colummns names

    df.to_csv('Replica_SteerMD.txt', index=False, sep='\t', float_format='%.7g', na_rep=np.NaN)
    return
    ########
