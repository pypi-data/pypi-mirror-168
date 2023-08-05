# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 23:33:11 2022

@author: noga mudrik
"""

#%% Variables Explanation File:
"""
Assumptions
"""    
# Here (unlike in the MATLAB code), I followed the following dimensions:
# data \in [N X T]. If in 3d: [pixels X pixels X T]    
# A (neural maps) \in [N X p], p = number of neural maps
# phi (sometimes called dictionary/new_dict/old_dict/D) \in [T X p]
# s.t. Y.T = \phi @ A.T
# corr_kern: neurons X neurons
# lambdas: [N X p]
# updateTauMat -> updateLambdasMat
# mkDataEmbedding -> mkDataGraph
"""
Variables:
"""    

# structure: MATLAB -> Python
# D -> \Phi
# tau_mat -> lambdas
# tau -> tau ()
# au_mat = params.tau./(beta + S + CF); -> python: lambdas = epsilon/(beta + |A_i| + [H*A]_i)


"""
Omissions in the Python code
"""

# configParams.self_tune (appears in calcAffinityMat)







"""
Near Future Improvements
"""
# add poisson to takeGDStep
#  singlePoiNeuroInfer
# patchGraFT
# ask about error_dict > params['dict_max_error']

"""
Far Future Improvements (#future) ( #efficiencyMarker)
"""

# reduceDimParams 
# More graphs (not only gaussian)
# enable fundiotn sparseDeconvDictEs (GD type "sparse_deconv")
# add the option of non-negative for update_LSwithForb
# motion correction 

"""
Unusual Requirements
"""
#pip install qpsolvers #!pip install quadprog
# pylops
#skimage (!pip install -U scikit-image)



"""
Efficiency Markers
"""
# efficiencyMarker - parfor loop
# checkAdam - things to check w. Adam









"""
Main Differences from the MATLAB code
"""
# solver_L1RLS.m -> solve_Lasso_style















