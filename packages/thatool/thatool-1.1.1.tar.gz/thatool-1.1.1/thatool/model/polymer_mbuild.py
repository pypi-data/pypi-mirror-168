""" This module contains classes and functions to build models of atomic polymers
See this Python package:
[1] mBuild: https://mbuild.mosdef.org/en/stable/

See the files:
D:\code\code_simulate\polymer_c21_pickup_hBN_PMMA\ref_using_mBuild_foyer.ipynb

NOTEs:
    1. Due to mbuild cannot be installed with python 3.10, so import this package in functions to avoid checking in thatool
"""

import os
import numpy as np
# import mbuild as mb
# from mbuild.lib.recipes.polymer import Polymer

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


### ==================================
### Define functions
### ==================================
def PMMA_chain(chain_len):
    """ build polyPMMA from monomers 

    Args:
        chain_len (int): number of monomers in each polymer = degree of polymerization
    
    Returns:
        chain (mb.compound): polymer chain
    """
    import mbuild as mb
    from mbuild.lib.recipes.polymer import Polymer

    pmma = mb.load('CC(-C)C(=O)OC', smiles=True)
    CC_bond = np.linalg.norm(pmma[0].pos-pmma[1].pos)

    chain = Polymer()
    chain.add_monomer(compound=pmma, indices=[10, 8], separation=CC_bond, replace=True)
    chain.add_end_groups(compound=mb.load('CC', smiles=True),  index=3,  separation=CC_bond, label="head", duplicate=False)
    chain.add_end_groups(compound=mb.load('C', smiles=True),  index=3,  separation=CC_bond, label="tail", duplicate=False)

    chain.build(n=chain_len, sequence='A')
    return chain   # mb_compound

def packing_lammps(chain, chain_num, 
                    density=None, box_size=None, 
                    forcefield_name=None, forcefield_files=None, 
                    atom_style='full', unit_style='metal', 
                    combining_rule='geometric', file_name='polymer.dat'):
    """ Packing polymer chains into box, and write LAMMPS file
    Packing based on either density or box_size.

    Args:
        chain (mb.compound): polymer chain
        chain_num (int): number of chains to be packed.
        density (float, optional): density, unit in kg/m3 (= 1e-3 g/cm3)
        box_size (list, optional): box_size = [3,3,3]
        forcefield_name (str, optional): should be 'oplsaa'.
        forcefield_files (str, optional): path to the *.xml file.
        atom_style (str, optional): atom_style of LAMMPS.
        unit_style (str, optional): can be 'metal'/'real'/'lj'
    """
    import mbuild as mb
    from mbuild.lib.recipes.polymer import Polymer
        
    list_inputs = [density, box_size]
    check = sum([1 for item in list_inputs if item is not None])
    if check>1:
        raise ValueError('Only one of {} is choose at a time'.format(list_inputs))
    if check<1:
        raise ValueError('Must choose either: density or box_size')

    ## packing
    if density is not None:
        polymer_box = mb.fill_box(compound=chain, n_compounds=chain_num, density=density, edge=0.01)       # unist in nm, cubic box  # , box=mb.Box([3,3,3])
    if box_size is not None:
        polymer_box = mb.fill_box(compound=chain, n_compounds=chain_num, box=mb.Box(box_size), edge=0.01)  

    ## write LAMMPS 
    if forcefield_name:
        polymer_box.save(file_name+'.lmp', forcefield_name=forcefield_name, atom_style=atom_style, unit_style=unit_style, combining_rule=combining_rule, overwrite=True)  
    elif forcefield_files:
        polymer_box.save(file_name+'.lmp', forcefield_files=forcefield_files, atom_style=atom_style, unit_style=unit_style, combining_rule=combining_rule, overwrite=True)  
    else:
        polymer_box.save(file_name+'.lmp', atom_style=atom_style, unit_style=unit_style, combining_rule=combining_rule, overwrite=True)  

    ## rename file
    if os.path.exists(file_name): os.remove(file_name)
    os.rename(file_name+'.lmp', file_name)
    return polymer_box