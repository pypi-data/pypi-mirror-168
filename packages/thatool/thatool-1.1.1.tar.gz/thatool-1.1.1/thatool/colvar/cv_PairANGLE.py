import sys          #, os, glob, re, natsort
sys.path.append("D:\work\myCodes\code_Python")
import thaModel         # thaFileType, thaTool, 
import numpy as np
import pandas as pd
import scipy.spatial
# from tess import Container





## 3. Atomic SMAC
def PairANGLE(Points, CENTER, SIGMA, **kwargs):
    """Order Parameter based on pair functions of Angles in the first shell: 
    [1]. Gobbob et al., "Nucleation of Molecular Crystals Driven by Relative Information Entropy"
    * Compulsory Inputs:
            Points   : Nx3 Matrix, contain bonding vectors between neighboring  atoms j and ref atom i
            CENTER=[pi/3, pi/2, 2*pi/3, pi] : list, centers of Gaussians
            SIGMA =[0.03,0.04,0.04,0.03]   : list, sigmas of Gaussians
    ** optional Inputs:
            switchFunc=[1,1...,1] : Nx1 array, contain values of switching function s(Rj) (Rj is positions of atom j)
    * Output:       
            gamma  : scalar, Order Parameter
        Example: S = thaTool.OrderPara.FCCcubic([1,0,0; 0,1,0], SW=sw)
    By Cao Thang, Aug 2020
    NOTE: Require to best chose Rcut for Switching function
    """
    ##==== compulsory Inputs 
    P = np.asarray(Points)	
    if P.shape[0] <=1: raise Exception('Input points is empty! please check it')
    
    ##==== optional Inputs 
    if 'switchFunc' in kwargs: 
        sw = kwargs['switchFunc']
        Rij = dist2_node2nodes([0,0,0], P)   
        mySW,_ = sw.Evaluate(Rij['bond_len'])
    else: mySW = np.ones(P.shape[0]) 

    ##==== Compute PairANGLE Parameter
    ## compute all possible nearest-angles 
    ksum = [None]*(P.shape[0] -1)   	#(k>j)
    for j in range(P.shape[0] -1):
        fixVector = P[j,:]
        ajik = angle_vector2vectors(fixVector, P[j+1:], unit='rad')  # list of angles jik, with fixed j 
        ##--
        gauss_sum = [None]*len(ajik)
        for n, phi in enumerate(ajik):
            gauss_sum[n] =  sum( [np.exp( -(phi-CENTER[m])**2. /(2.*SIGMA[m]**2.) ) for m in range(len(SIGMA)) ] ) 
        ##--
        ksum[j] = sum(gauss_sum *mySW[j+1:]) /sum(mySW[j+1:])
    ##--
    jsum = sum(ksum *mySW[:-1]) /sum(mySW[:-1])       # not compute final j, because no more k
    return  jsum  
##--------
 
 	

