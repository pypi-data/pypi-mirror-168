# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 23:27:40 2022

@author: noga mudrik 
based on Adam Charles and Gal Mishne MATLAB code

"""
#%% Imports
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
#from quadprog import solve_qp 
from qpsolvers import solve_qp #https://scaron.info/doc/qpsolvers/quadratic-programming.html#qpsolvers.solve_qp https://pypi.org/project/qpsolvers/
#print(qpsolvers.available_solvers)
import matplotlib
import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import itertools

import pandas as pd
import seaborn as sns

import random

import os

from datetime import date

sep = os.sep

import os.path
import warnings
from scipy.optimize import nnls
import numbers
from sklearn import linear_model
import pylops
#from PIL import Image
from skimage import io

#%% Default Parameters 
global params_default
params_default = {'max_learn': 1e3,  # Maximum number of steps in learning 
    'mean_square_error': 1,

    
    'epsilon' : 1,                                               # Default tau values to be spatially varying
    'l1': 7, #0.00007,#0.7,#0.7,                                             # Default lambda parameter is 0.6
    'l2': 0,#0.00000000000005,# 0.2**2,    # lamForb                                      # Default Forbenius norm parameter is 0 (don't use)
    'l3': 0,  #lamCont                 # Default Dictionary continuation term parameter is 0 (don't use)
    'lamContStp': 1,                                               # Default multiplicative change to continuation parameter is 1 (no change)
    'l4': 0,#0.1,     #lamCorr  # Default Dictionary correlation regularization parameter is 0 (don't use)
    'beta': 0.09,                                          # Default beta parameter to 0.09
    'maxiter': 0.01,                                            # Default the maximum iteration to whenever Delta(Dictionary)<0.01
    'numreps': 2,                                               # Default number of repetitions for RWL1 is 2
    'tolerance': 1e-8,                                            # Default tolerance for TFOCS calls is 1e-8

    'likely_form' : 'gaussian',                                      # Default to a gaussian likelihood ('gaussian' or'poisson')
    'step_s': 5, #1,                                               # Default step to reduce the step size over time (only needed for grad_type ='norm')
    'step_decay': 0.999,                                           # Default step size decay (only needed for grad_type ='norm')
                                       
    'dict_max_error': 0.01,       # learn_eps                                    # Default learning tolerance: stop when Delta(Dictionary)<0.01
    'p': 4,                        # Default number of dictionary elements is a function of the data
    'verb': 1,                                               # Default to no verbose output
  
    'GD_iters': 1,                                               # Default to one GD step per iteration
    'bshow': 0,                                               # Default to no plotting
                                                  # Default to not having negativity constraints
    'nonneg':True,                                           # Default to not having negativity constraints on the coefficients
    'plot': False,                                           # Default to not plot spatial components during the learning
    'updateEmbed' : False,                                           # Default to not updateing the graph embedding based on changes to the coefficients
    'mask': [],                                              # for masked images (widefield data)
    'normalizeSpatial' : False,                                      # default behavior - time-traces are unit norm. when true, spatial maps normalized to max one and time-traces are not normalized
     
  
     'patchSize': 50, 
     'motion_correct': False, #future
     'kernelType': 'embedding',
     'reduceDim': False, #True,
     'w_time': 0,
     'n_neighbors':49,
     'n_comps':2,
     'solver_qp':'quadprog',
     'solver': 'inv',# 'lasso',#'spgl1',
     'nullify_some': False , 
     'norm_by_lambdas_vec': True, 
     'GD_type': 'norm',#'full_ls_cor'
     'xmin' : 151,#151
     'xmax' : 200,#350                                                            # Can sub-select a portion of the full FOV to test on a small section before running on the full dataset
     'ymin' : 151,#101
     'ymax' : 200,#300 
     'use_former_kernel' : False,
     'usePatch' : False, #str2bool(input('to use patch? (true or false)') )
     'portion' :True,# str2bool(input('To take portion?'))
     'divide_med' : False,# str2bool(input('divide by median? (true or false)'))
     
     'data_0_1' : False,
     'to_save' : True, #str2bool(input('to save?'))
     'default_path':  r'E:\CODES FROM GITHUB\GraFT-analysis\code\neurofinder.02.00\images', 
     'save_error_iterations': True,
     'max_images':800,
     'dist_init': 'uniform',
     'to_sqrt':True
     

     
    }



#%%  GraFT Functions

global params_config
params_config = {'self_tune':7, 'dist_type': 'euclidian', 'alg':'ball_tree',
                       'n_neighbors':49, 'reduce_dim':False}


def createDefaultParams(params = {}):
    dictionaryVals = {'step_s':1, 
                      'learn_eps':0.01,
                      'epsilon': 2,
                      'numreps': 2, 
                      }
    return  addKeyToDict(dictionaryVals,params)

def createLmabdasMat(epsilonVal, shapeMat):
    if isinstance(epsilonVal,  (list, tuple, np.ndarray)) and len(epsilonVal) == 1:
        epsilonVal = epsilonVal[0]
    if not isinstance(epsilonVal, (list, tuple, np.ndarray)):
        labmdas = epsilonVal * np.ones(shapeMat)
    else:
        epsilonVal = np.array(epsilonVal)
        if len(epsilonVal) == shapeMat[1]:
            lambdas = np.ones(shapeMat[0]).rehspae((-1,1)) @ epsilonVal.reshape((1,-1))
        elif len(epsilonVal) == shapeMat[0]:
            lambdas =  epsilonVal.reshape((-1,1)) @  np.ones(shapeMat[1]).rehspae((1,-1))
        else:
            raise ValueError('epsilonVal must be either a number or a list/tupe/np.array with the a number of elements equal to one of the shapeMat dimensions')



def addKeyToDict(dictionaryVals,dictionaryPut):
    return {**dictionaryVals, **dictionaryPut}


def validate_inputs(params)    :
    params['epsilon'] = float(params['epsilon'])
    params['step_s'] = float(params['step_s'])
    params['p'] = int(params['p'])
    params['nonneg'] = str2bool(params['nonneg'])
    params['reduceDim'] = str2bool(params['reduceDim'])
    params['solver'] = str(params['solver'])
    params['norm_by_lambdas_vec'] = str2bool(params['norm_by_lambdas_vec'])
    return params
    
def run_GraFT(data = [], corr_kern = [], params = {}, to_save = True, to_return = True,
               ask_selected = True, selected = ['epsilon','step_s', 'p', 'nonneg',
                                                'reduceDim','solver','norm_by_lambdas_vec'] ):
    """
    This function runs the main graft algorithm.

    Parameters
    ----------
    data : can be string of data path or a numpy array (pixels X pixels X time) or (pixels X time). 
        Leave empty for default
        The default is []. In this case the calcium imaging dataset will be used. 
    corr_kern : proximity kernel. Leave empty ([]) to re-create the kernel.  
    params : dictionary of parameters, optional
        the full default values of the optional parameters are mentioned in dict_default. 
    to_save : boolean, optional
        whether to save the results to .npy file. The default is True.
    to_return : boolean, optional
        whether to return results. The default is True.
    ask_selected : boolean, optional
        whether to ask the use about specific parameters. The default is True.
    selected : list of strings, optional
        relevant only if 'ask_selected' is true. 
        
        . The default is ['epsilon','step_s', 'p', 'nonneg',
                                     'reduceDim','solver','norm_by_lambdas_vec'].

    Raises
    ------
    ValueError
        If invalid path

    Returns
    -------
    A : np.ndarray (pixels X p) - neural maps
    phi : np.ndarray (time X p)   temporal traces
    additional_return : dictionary with additional returns. Including error over iterations

    """
    
    params = {**params_default, **params}
    if ask_selected:
        for select in selected:
            params[select] = input('Value of %s (def = %s)'%(select, str(params[select])))
            params = validate_inputs(params)
    if to_save:
        save_name = input('save_name')
        if ask_selected:
            addition_name = '_'.join([s +'_' + str(params[s] ) for s in selected])
            save_name_short = save_name
            save_name = save_name + '_' + addition_name
            
        
    """
    Create data
    """
    default = False
    if checkEmptyList(data):
        warnings.warn('Data is empty. Take default dataset (calcium imaging)')
        default = True
        data = 'data_calcium_xmin_%d_xmax_%d_ymin_%d_ymax_%d.npy'%(params['xmin'],params['xmax'],params['ymin'],params['ymax'])
        #data = params['default_path']
    if isinstance(data, str): # Check if path
        been_cut = False
        try:
            try:
                if data.endswith('.npy'):
                    data = np.load('data_calcium_xmin_%d_xmax_%d_ymin_%d_ymax_%d.npy'%(params['xmin'],params['xmax'],params['ymin'],params['ymax'])) 
                    been_cut = True
                else:
                    data =  from_folder_to_array(data, max_images = params['max_images'])   
            except:
                if default:
                    data =  from_folder_to_array(params['default_path'], max_images = params['max_images'])  
                else:
                    raise ValueError('Data loading failed')
                
        except:
            raise ValueError('Cannot locate data path! (your invalid path is %s)'%data)
    if isinstance(data,np.ndarray):
        if not been_cut:
            data = data[params['xmin']:params['xmax'], params['ymin']:params['ymax'],:]
            np.save('data_calcium_xmin_%d_xmax_%d_ymin_%d_ymax_%d.npy'%(params['xmin'],params['xmax'],params['ymin'],params['ymax']), data)        
        
    """
    Create Kernel
    """
    print('creating kernel...')
    if checkEmptyList(corr_kern):
        corr_kern  = mkDataGraph(data, params, reduceDim = params['reduceDim'], 
                             reduceDimParams = {'alg':'PCA'}, graph_function = 'gaussian',
                    K_sym  = True, use_former = False, data_name = 'try_graft', toNormRows = True)
        np.save('kernel_calcium_xmin_%d_xmax_%d_ymin_%d_ymax_%d.npy'%(params['xmin'],params['xmax'],params['ymin'],params['ymax']), corr_kern)
    elif isinstance(corr_kern, str): # Check if path
      try:
          corr_kern = np.load('kernel_calcium_xmin_%d_xmax_%d_ymin_%d_ymax_%d.npy'%(params['xmin'],params['xmax'],params['ymin'],params['ymax']))
      except:
          raise ValueError('Cannot locate kernel path! (your invalid path is %s)'%corr_kern)
           
          
    """
    run graft
    """

    if params['usePatch']:
        raise ValueError('Use Patch is not available yet!')
        
    else:
        [phi, A, additional_return] = GraFT(data, [], corr_kern, params)                    # Learn the dictionary (no patching - will be much more memory intensive and slower)
    
    if to_save:
        #save_name = input('save_name')
        path_name = 'date_'+ str(date.today()) + '_xmin_%d_xmax_%d_ymin_%d_ymax_%d.npy'%(params['xmin'],params['xmax'],params['ymin'],params['ymax'])
        if not os.path.exists(path_name):
            os.makedirs(path_name)
        try:
            np.save(path_name + sep + save_name + '.npy', {'phi':phi, 'A':A, 'data':data, 'params':params, 'divide_med':params['divide_med'], 
                                                           'usePatch':params['usePatch'], 'shape':data.shape, 'additional': additional_return})
        
        except:
            np.save(path_name + sep + save_name_short + '.npy', {'phi':phi, 'A':A, 'data':data, 'params':params, 'divide_med':params['divide_med'], 
                                                           'usePatch':params['usePatch'], 'shape':data.shape, 'additional': additional_return})
                    

    if to_return:
        return A, phi, additional_return
          
    
def GraFT(data, phi, kernel, params):
    """
    Function to learn a dictioanry for spatially ordered/ graph-based data using a
    re-weighted l1 spatial / graph filtering model.
    
    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    phi : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.
    params : TYPE
        DESCRIPTION.

    Returns
    -------
    None.
    
    """
    #print(params.get('nonneg'))
    additional_return  = {'MSE':[]}
    if len(data.shape) == 3: data = MovToD2(data)
    params = {**{'max_learn': 1e3, 'learn_eps': 0.01,'step_decay':0.995}, **params}
    #params = createDefaultParams(params)
    n_rows = data.shape[0] # number of neurons
    n_cols =params['p']# data.shape[1]
    n_times = data.shape[1]
    extras = {'dictEvo':[], 'presMap':[], 'wghMap':[]} # Store some outputs
    
    #%% Initialize dictionary
    #print('prarams in graft')
    #print(params)
    phi = dictInitialize(phi, (n_times, n_cols), params = params)
    if params['to_sqrt']:
        multi = np.sqrt(np.mean(data))
    else:
        multi = 1
    phi = phi * multi    
    step_GD = params['step_s']
    
    lambdas = []  # weights
    A = []
    
    n_iter = 0
    error_dict = np.inf
    cur_error = np.inf #
    print("params['max_learn']")
    print(params['max_learn'])
    while n_iter < params['max_learn'] and (error_dict > params['dict_max_error'] or cur_error > params['mean_square_error']):
        print('Iteration %d'%n_iter)
        n_iter += 1
        #%% compute the presence coefficients from the dictionary:
        A, lambdas = dictionaryRWL1SF(data, phi, kernel, params = params,A=A) # Infer coefficients given the data and dictionary
        print('A after update')
        print(A.sum())
        #%% Second step is to update the dictionary:
        dict_old = phi # Save the old dictionary for metric calculations
        #print('phi before update')
        #print(phi)
        phi = dictionary_update(phi, A, data, step_GD, GD_type = params['GD_type'], params = params) # Take a gradient step with respect to the dictionary
        print('phi after update')
        print(phi.sum())
        #raise ValueError('fdgfdgfdgfdgdfgsdfg')
        step_GD   = step_GD*params['step_decay']                                   # Update the step size

        error_dict    = norm((phi - dict_old).flatten())/norm(dict_old.flatten());        
        # Calculate the difference in dictionary coefficients
    
        params['l3'] = params['lamContStp']*params['l3'];                     # Continuation parameter decay
        cur_error  = np.mean((A @ phi.T - data)**2)
        additional_return['MSE'].append(cur_error)
        print('Current Error is: {:.2f}'.format(cur_error))
    ##  post-processing
    # Re-compute the presence coefficients from the dictionary:
    if params['normalizeSpatial']:
        A, lambdas = dictionaryRWL1SF(data, phi, kernel, params,A)   # Infer coefficients given the data and dictionary

    Dnorms   = np.sqrt(np.sum(phi**2,0))               # Get norms of each dictionary element
    Smax     = np.max(A,0)                                                    # Get maximum value of each spatial map
    actMeas  = Dnorms*Smax                                             # Total activity metric is the is the product of the above
    IX   = np.argsort(actMeas)[::-1]       # Get the indices of the activity metrics in descending order
    phi = phi[:,IX]                                                 # Reorder the dictionary
    A   = A[:,IX]                                                        # Reorder the spatial maps
    

    return phi, A, additional_return

def norm(mat):
    """
    Parameters
    ----------
    mat : np.ndarray
        l2 norm of mat.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if len(mat.flatten()) == np.max(mat.shape):
        return np.sqrt(np.sum(mat**2))
    else:
        _, s, _ = np.linalg.svd(mat, full_matrices=True)
        return np.max(s)
    
def mkCorrKern(params = {}):
    """
    Parameters
    ----------
    params : TYPE, optional
        DESCRIPTION. The default is {}.

    Returns
    -------
    corr_kern : TYPE
        DESCRIPTION.

    """
    # Make a kernel
    params = {**{'w_space':3,'w_scale':4,'w_scale2':0.5, 'w_power':2,'w_time':0}, **params}
    dim1  = np.linspace(-params['w_scale'], params['w_scale'], 1+2*params['w_space']) # space dimension
    dim2  = np.linspace(-params['w_scale2'], params['w_scale2'], 1+2*params['time']) # time dimension
    corr_kern  = gaussian_vals(dim1, std = params['w_space'], mean = 0 , norm = True, 
                               dimensions = 2, mat2 = dim2, power = 2)
    return corr_kern
    
def checkCorrKern(data, corr_kern, param_kernel = 'embedding', recreate = False, know_empty = False):
    if len(corr_kern) == 0: #raise ValueError('Kernel cannot ')
        if not know_empty: warnings.warn('Empty Kernel - creating one')
        if param_kernel == 'embedding' and recreate:
            corr_kern  = mkDataGraph(data, corr_kern) 
        elif  param_kernel == 'convolution'  and recreate:
            corr_kern  = mkCorrKern(corr_kern) 
        else:
            raise ValueError('Invalid param_kernel. Should be "embedding" or "convolution"')
            
    return corr_kern

    

def checkEmptyList(obj):
    return isinstance(obj, list) and len(obj) == 0
    
def dictionaryRWL1SF(data, phi, corr_kern, A = [], params = {}):
    #print('dictionaryRWL1SF')
    # compute the presence coefficients from the dictionary
  
    params = {**{'epsilon': 1 , 'likely_form':'gaussian', 'numreps':2, 'normalizeSpatial':False,
                 'thresANullify': 2**(-5)},**params}
    if len(data.shape) == 3: data = MovToD2(data)
    n_times = data.shape[1]
    n_neurons = data.shape[0]
    p = phi.shape[1]
    
    corr_kern     = checkCorrKern(data, corr_kern); 
    if params['to_sqrt']:
        multi = np.sqrt(np.mean(data))
    else:
        multi = 1
    if checkEmptyList(A):
        if params['dist_init'] == 'zeros':
            A = np.zeros((n_neurons, p))# np.zeros((n_neurons, p))
        else:
            A = np.random.rand(n_neurons, p) * multi
    
    if (isinstance( params['epsilon'] , list) and len(params['epsilon']) == 1):
        params['epsilon'] = params['epsilon'][0]
    if isinstance(params['epsilon'], numbers.Number):        
        lambdas = np.ones((n_neurons, p))*params['epsilon']
    elif (isinstance( params['epsilon'] , list) and len(params['epsilon']) == p):
        lambdas = np.repeat(params['epsilon'].reshape((1,-1)), n_neurons, axis = 0)#np.ones(n_neurons, p)*params['epsilon']
    elif (isinstance( params['epsilon'] , list) and len(params['epsilon']) == n_neurons):
        lambdas = np.repeat(params['epsilon'].reshape((-1,1)), p, axis = 1)#np.ones(n_neurons, p)*params['epsilon']
    else: 
        raise ValueError('Invalid length of params[epsilon]. Should be a number or a list with n_neurons or p elementts. Currently the params[epsilon] is ' + str(params['epsilon']))
    
   
    for repeat in range(params['numreps']):

        lambdas = updateLambdasMat(A, corr_kern, params['beta'], params) # Update the matrix of weights

        for n_neuron in range(n_neurons):
            if params['likely_form'].lower() == 'gaussian':
                print('A before gauss')
                print(A)
                print('---------')
                
                A[n_neuron, :] = singleGaussNeuroInfer(lambdas[n_neuron, :], data[n_neuron, :],
                phi, 
                l1 = params['l1'], 
                nonneg = params['nonneg'], A=A[n_neuron, :], params = params)
                #raise ValueError('fgfdgfdg')
            elif params['likely_form'].lower() == 'poisson':
                A[n_neuron, :] = singlePoiNeuroInfer(lambdas[n_neuron, :], data[n_neuron, :],
                phi, 
                params['lambda'], 
                params['tolerance'],
                params['nonneg'], A[n_neuron,:])
            else:
                raise ValueError('Invalid likely from value')
    if params['normalizeSpatial']:
        max_A_over_neurons = A.sum(0)
        max_A_over_neurons[max_A_over_neurons == 0] = 1
        A = A/max_A_over_neurons.reshape((1,-1))
    A[A < params['thresANullify']] = 0
        
    return A, lambdas

def singlePoiNeuroInfer(): #future
    raise ValueError('Need to be implemented')
    
    
    
def normalizeDictionary(D, cutoff = 1):
    D_norms = np.sqrt(np.sum(D**2,0))       # Get the norms of the dictionary elements 
    D       = D @ np.diag(1/(D_norms*(D_norms>cutoff)/cutoff+(D_norms<=cutoff))); # Re-normalize the basis
    return D

    
def dictionary_update(dict_old, A, data, step_s, GD_type = 'norm', params ={}):    
    dict_new = takeGDStep(dict_old, A, data, step_s, GD_type, params)
    if not params.get('normalizeSpatial'):
        dict_new = normalizeDictionary(dict_new,1)                            # Normalize the dictionary
    #print('phi after norm')
    #print(dict_old.sum())
    dict_new[np.isnan(dict_new)] = 0
    
    return dict_new
    

def takeGDStep(dict_old, A, data, step_s, GD_type = 'norm', params ={}):
    """
    Parameters
    ----------
    dict_old : TYPE
        DESCRIPTION.
    A : TYPE
        DESCRIPTION.
    data : TYPE
        DESCRIPTION.
    step_s : TYPE
        DESCRIPTION.
    GD_type : TYPE, optional
        DESCRIPTION. The default is 'norm'.
    params : TYPE, optional
        DESCRIPTION. The default is {}.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    dict_new : TYPE
        DESCRIPTION.

    """
    l2 = params['l2']
    l3 = params['l3']
    l4 = params['l4']
    
    if GD_type == 'norm':
        #print('phi before norm')
        #print(dict_old.sum())
        # Take a step in the negative gradient of the basis:
        # Minimizing the energy:    E = ||x-Da||_2^2 + lambda*||a||_1^2
        dict_new = update_GDiters(dict_old, A, data, step_s, params)
        #print('phi after norm')
        #print(dict_new.sum())
        
    elif GD_type == 'forb':
        # Take a step in the negative gradient of the basis:
        # This time the Forbenious norm is used to reduce unused
        # basis elements. The energy function being minimized is
        # then:     E = ||x-Da||_2^2 + lambda*||a||_1^2 + lamForb||D||_F^2
        dict_new = update_GDwithForb(dict_old, A, data, step_s, l2, params);
    elif GD_type ==  'full_ls':
        # Minimizing the energy:
        # E = ||X-DA||_2^2 via D = X*pinv(A)
        dict_new = update_FullLS(dict_old, A, data, params);
    elif GD_type == 'anchor_ls':
        # Minimizing the energy:
        # E = ||X-DA||_2^2 + lamCont*||D_old - D||_F^2 via D = [X;D_old]*pinv([A;I])
        dict_new = update_LSwithCont(dict_old, A, data, l3, params);
    elif GD_type == 'anchor_ls_forb':
        # Minimizing the energy:
        # E = ||X-DA||_2^2 + lamCont*||D_old - D||_F^2 + lamForb*||D||_F^2 
        #                  via D = [X;D_old]*pinv([A;I])
        dict_new = update_LSwithContForb(dict_old, A, data, l2, l3, params);
    elif GD_type == 'full_ls_forb':
        # Minimizing the energy:
        # E = ||X-DA||_2^2 + lamForb*||D||_F^2
        #              via  D = X*A^T*pinv(AA^T+lamForb*I)
        dict_new = update_LSwithForb(dict_old, A, data, l2, params);
    elif GD_type== 'full_ls_cor':
        # E = ||X-DA||_2^2 + l4*||D.'D-diag(D.'D)||_sav + l2*||D||_F^2
        #             + l3*||D-Dold||_F^2 
        dict_new = update_FullLsCor(dict_old, A, data, l2, l3, l4, params)
    elif GD_type =='sparse_deconv':
        dict_new   = sparseDeconvDictEst(dict_old,data,A,params.h,params); # This is a more involved function and needs its own function
    else:
        raise ValueError('GD_Type %s is not defined in the takeGDstep function'%GD_type)        

    return dict_new
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def dictInitialize(phi = [], shape_dict = [], norm_type = 'unit', to_norm = True, params = {}):

    """
    Parameters
    ----------
    phi : list of lists or numpy array or empty list
        The initializaed dictionary
    shape_dict : tuple or numpy array or list, 2 int elements, optional
        shape of the dictionary. The default is [].
    norm_type : TYPE, optional
        DESCRIPTION. The default is 'unit'.
    to_norm : TYPE, optional
        DESCRIPTION. The default is True.
    dist : string, optional
        distribution from which the dictionary is drawn. The default is 'uniforrm'.        
    Raises
    ------
    ValueError
        DESCRIPTION.
        
    Returns
    -------
    phi : TYPE
        The output dictionary

    """

    if len(phi) == 0 and len(shape_dict) == 0:
        raise ValueError('At least one of "phi" or "shape_dict" must not be empty!')
    if len(phi) > 0:        
        return norm_mat(phi, type_norm = norm_type, to_norm = to_norm)
    else:
        #if dist == 'uniform':
        phi = createMat(shape_dict, params)


        return dictInitialize(phi, shape_dict, norm_type, to_norm,  params)

    
def createMat(shape_dict,  params = params_default ):
    """
    Parameters
    ----------
    shape : TYPE
        DESCRIPTION.
    dist : TYPE, optional
        DESCRIPTION. The default is 'uniforrm'.
    params : TYPE, optional
        DESCRIPTION. The default is {'mu':0, 'std': 1}.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.
    """

    params = {**{'mu':0, 'std': 1}, **params}
    dist = params['dist_init']

    if dist == 'uniform':
        return np.random.rand(shape_dict[0], shape_dict[1]) 
    elif dist == 'norm':
        return params['mu'] + np.random.randn(shape_dict[0], shape_dict[1])*params['std']
    elif dist == 'zeros':
        return np.zeros((shape_dict[0], shape_dict[1]))
    else:
        raise ValueError('Unknown dist for createMat')
#<h1 id="header">Header</h1>    

def singleGaussNeuroInfer(lambdas_vec, data, phi, l1,  nonneg, A = [], ratio_null = 0.1, params = {}):
    # Use quadprog  to solve the weighted LASSO problem for a single vector
    
    if phi.shape[1] != len(lambdas_vec):
        raise ValueError('Dimension mismatch!')
        
    # Set up problem

    data = data.flatten()                                           # Make sure time-trace is a column vector
    lambdas_vec = lambdas_vec.flatten()                                                    # Make sure weight vector is a column vector
    p      = len(lambdas_vec)                                                  # Get the numner of dictionary atoms
    
    # Set up linear operator
    # Af = @(x) D*(x./tau_vec);                                                  # Set up the forward operator
    # Ab = @(x) (D.'*x)./tau_vec;                                                # Set up the backwards (transpose) operator
    # A  = linop_handles([numel(mov_vec), N2], Af, Ab, 'R2R');                   # Create a TFOCS linear operator object
    ## Run the weighted LASSO to get the coefficients

    
    if len(data) == 0 or np.sum(data**2) == 0:
        A = np.zeros(p)                       # This is the trivial solution to generate all zeros linearly.

        raise ValueError('zeros again')
    else:
        if nonneg:

            if A == [] or (A==0).all():
                print('A before')
                print(A)
                print(lambdas_vec)
                A = solve_qp(2*(phi.T @ phi) , -2*phi.T @ data + l1*lambdas_vec,  solver = params['solver_qp'] )       # Use quadratic programming to solve the non-negative LASSO
                print('A after')
                print(A)
                print(lambdas_vec)
                if np.nan in A: raise ValueError('fgfdgdfg')
                #lb = np.zeros((p,1)), 
                ub = np.inf*np.ones((p,1)),
            else:

                print('A before')
                print(A)
                print(lambdas_vec)
                A = solve_qp(2*(phi.T @ phi),-2*phi.T @ data+l1*lambdas_vec, 
                             solver = params['solver_qp'] ,   initvals = A)         # Use quadratic programming to solve the non-negative LASSO
                if np.isnan(A).any(): 
                    print(A)
                    raise ValueError('fgfdgdfg')
                #lb = np.zeros((p,1)), 
                #ub = np.inf*np.ones((p,1)),
          
        else:
           #params['nonneg'] = False
           #efficiencyMarker
           A = solve_Lasso_style(phi, data, l1, [], params = params, random_state = 0).flatten()
           #solver_L1RLS(phi, data, l1, zeros(N2, 1), params )         # Solve the weighted LASSO using TFOCS and a modified linear operator
           if params['norm_by_lambdas_vec']:
               A = A.flatten()/lambdas_vec.flatten();              # Re-normalize to get weighted LASSO values
               #  consider changing to oscar like here https://github.com/vene/pyowl/blob/master/pyowl.py 
    if params['nullify_some']:
        A[A<ratio_null*np.max(A)] = 0;    
    return A

def solve_Lasso_style(A, b, l1, x0, params = {}, lasso_params = {},random_state = 0):
  """
      Solves the l1-regularized least squares problem
          minimize (1/2)*norm( A * x - b )^2 + l1 * norm( x, 1 ) 
          
    Parameters
    ----------
    A : TYPE
        DESCRIPTION.
    b : TYPE
        DESCRIPTION.
    l1 : float
        scalar between 0 to 1, describe the reg. term on the cofficients.
    x0 : TYPE
        DESCRIPTION.
    params : TYPE, optional
        DESCRIPTION. The default is {}.
    lasso_params : TYPE, optional
        DESCRIPTION. The default is {}.
    random_state : int, optional
        random state for reproducability. The default is 0.

    Raises
    ------
    NameError
        DESCRIPTION.

    Returns
    -------
    x : np.ndarray
        the solution for min (1/2)*norm( A * x - b )^2 + l1 * norm( x, 1 ) .

  lasso_options:
               - 'inv' (least squares)
               - 'lasso' (sklearn lasso)
               - 'fista' (https://pylops.readthedocs.io/en/latest/api/generated/pylops.optimization.sparsity.FISTA.html)
               - 'omp' (https://pylops.readthedocs.io/en/latest/gallery/plot_ista.html#sphx-glr-gallery-plot-ista-py)
               - 'ista' (https://pylops.readthedocs.io/en/latest/api/generated/pylops.optimization.sparsity.ISTA.html)       
               - 'IRLS' (https://pylops.readthedocs.io/en/latest/api/generated/pylops.optimization.sparsity.IRLS.html)
               - 'spgl1' (https://pylops.readthedocs.io/en/latest/api/generated/pylops.optimization.sparsity.SPGL1.html)
               
               
               - . Refers to the way the coefficients should be claculated (inv -> no l1 regularization)
  """  
  if len(b.flatten()) == np.max(b.shape):
      b = b.reshape((-1,1))
  if 'solver' not in params.keys():
      warnings.warn('Pay Attention: Using Default (inv) solver for updating A. If you want to use lasso please change the solver key in params to lasso or another option from "solve_Lasso_style"')
  params = {**{'threshkind':'soft','solver':'inv','num_iters':50}, **params}
  #print(params['solver'])
  if params['solver'] == 'inv' or l1 == 0:
      #print(A.shape)
      #print(b.shape)
      x =linalg.pinv(A) @ b.reshape((-1,1))
      #print(x.shape)
  elif params['solver'] == 'lasso' :
      #herehere try without warm start
    clf = linear_model.Lasso(alpha=l1,random_state=random_state, **lasso_params)
    clf.fit(A,b.T )     
    x = np.array(clf.coef_)

  elif params['solver'].lower() == 'fista' :
      Aop = pylops.MatrixMult(A)
  
      #if 'threshkind' not in params: params['threshkind'] ='soft'
      #other_params = {'':other_params[''],
      x = pylops.optimization.sparsity.FISTA(Aop, b.flatten(), niter=params['num_iters'],
                                             eps = l1 , threshkind =  params.get('threshkind') )[0]
  elif params['solver'].lower() == 'ista' :

      #herehere try without warm start
      if 'threshkind' not in params: params['threshkind'] ='soft'
      Aop = pylops.MatrixMult(A)
      x = pylops.optimization.sparsity.ISTA(Aop, b.flatten(), niter=params['num_iters'] , 
                                                 eps = l1,threshkind =  params.get('threshkind'))[0]
      
  elif params['solver'].lower() == 'omp' :
  
      Aop = pylops.MatrixMult(A)
      x  = pylops.optimization.sparsity.OMP(Aop, b.flatten(), 
                                                 niter_outer=params['num_iters'], sigma=l1)[0]     
  elif params['solver'].lower() == 'spgl1' :
    
      Aop = pylops.MatrixMult(A)
      x = pylops.optimization.sparsity.SPGL1(Aop, b.flatten(),iter_lim = params['num_iters'],  tau = l1)[0]      
      
  elif params['solver'].lower() == 'irls' :
   
      Aop = pylops.MatrixMult(A)
      
      #herehere try without warm start
      x = pylops.optimization.sparsity.IRLS(Aop, b.flatten(),  nouter=50, espI = l1)[0]      
  else:     
    raise NameError('Unknown update c type')  
  return x


def updateLambdasMat(A, corr_kern, beta, params ):
    p = A.shape[1]
    n_neurons = A.shape[0]
    params = {**{'epsilon':1, 'updateEmbed': False, 'mask':[]}, **params}
    if params.get('updateEmbed')  :                                                    # If required, recalculate the graph based on the current estimate of coefficients
        H = mkDataGraph(A, []);   
                                            # This line actually runs that re-calculation of the graph
    if (isinstance( params['epsilon'] , list) and len(params['epsilon']) == 1):
        params['epsilon'] = params['epsilon'][0]
        
    if isinstance(params['epsilon'], numbers.Number):     # If the numerator of the weight updates is constant...
        
        if params['updateEmbed']  :                                              #  - If the numerator of the weight updates is the size of the dictionary (i.e., one tau per dictioary element)...
               
            lambdas = params['epsilon']/(beta + A + H @ A)                            #    - Calculate the wright updates tau/(beta + |s_i| + [P*S]_i)
        elif not params['updateEmbed']:     
                                                #  - If the graph was not updated, use the original graph (in corr_kern)
            if corr_kern.shape[0] ==  n_neurons    :                                 #    - If the weight projection matrix has the same number of rows as pixels, update based on a matrix multiplication                     

                lambdas = params['epsilon']/(beta + A + corr_kern @ A);                #      - Calculate the wright updates tau/(beta + |s_i| + [P*S]_i)
            else:
                raise ValueError('This case is not defined yet') #future
                # CF = np.zeros(A.shape);
                # for net_num in range(p):
                #     if not params.get('mask')
                #         CF[:,net-num] = np.convolve(conv2(reshape(S(:,i),params.nRows,params.nCols), corr_kern, mode = 'same');
                #     else
                #         temp = zeros(params.nRows,params.nCols);
                #         temp(params.mask(:)) = S(:,i);
                #         temp = conv2(temp ,corr_kern,'same');
                #         CF(:,i) = temp(params.mask(:));

                # lambdas = params['epsilon']/(beta + A + CF);  #      - Calculate the wright updates tau/(beta + |s_i| + [P*S]_i)

    elif len(params['epsilon'].flatten()) == p:            # If the numerator of the weight updates is the size of the dictionary (i.e., one tau per dictioary element)...
   
        if params['updateEmbed'] :                                            #  - If the graph was updated, use the new graph (i.e., P)
            lambdas = params['epsilon'].reshape((1,-1))/(beta + A + corr_kern @ A)         #    - Calculate the wright updates tau/(beta + |s_i| + [P*S]_i)
        else   :                                       #  - If the graph was not updated, use the original graph (in corr_kern)
            if corr_kern.shape[0] == n_neurons :                                    #    - If the weight projection matrix has the same number of rows as pixels, update based on a matrix multiplication
                lambdas =  params['epsilon'].reshape((1,-1))/(beta + A + corr_kern @ A) #    - Calculate the wright updates tau/(beta + |s_i| + [P*S]_i)
            else   :
                raise ValueError('Invalid kernel shape') #future                #  - Otherwise, the graph was updated; use the original graph (in corr_kern)
            # I'm not sure what option is supposed to go here
            #    lambdas = reshape(convn(reshape(S, [im_x, im_y, nd]),...
            #                                  corr_kern,'same'), im_x*im_y,1); #    - Get base weights
            #    lambdas = bsxfun(@times, params['epsilon'], 1./(beta + S + lambdas)); #    - Calculate the wright updates tau/(beta + |s_i| + [P*S]_i) 

    elif params['epsilon'].shape[0] == A.shape[0] and params['epsilon'].shape[1] == A.shape[1]: #future
    
        raise ValueError('This option is not available yet')
        # If the numerator of the weight updates is the size of the image
        #CF = np.zeros(A.shape)
        #for net_num in range(A.shape[1]): #future
            #if not params.get('mask')
            #    CF(:,i) = vec(conv2(reshape(S(:,i),params.nRows,params.nCols)  ,corr_kern,'same'));
            #else
            #         temp = zeros(params.nRows,params.nCols);
            #         temp(params.mask(:)) = S(:,i);
            #         CF(:,i) = vec(conv2(temp ,corr_kern,'same'));
        
            # lambdas = bsxfun(@times, params['epsilon'], ones(1,1,nd))./(beta+S+CF);  %  - Calculate the wright updates tau/(beta + |s_i| + [P*S]_i)
            
    else:
        raise ValueError('Invalid Option')
    return lambdas
    
def MovToD2(mov, ):
    """
    Parameters
    ----------
    mov : can be list of np.ndarray of frames OR 3d np.ndarray of [pixels X pixels X time]
        The data

    Returns
    -------
    array 
        a 2d numpy array of the movie, pixels X time 

    """
    if isinstance(mov, list):
        return np.hstack([frame.flatten().reshape((-1,1)) for frame in mov])
    elif isinstance(mov, np.ndarray) and len(np.shape(mov)) == 2:
        return np.hstack([mov[:,:,frame_num].flatten().reshape((-1,1)) for frame_num in range(mov.shape[2])])
    elif isinstance(mov, np.ndarray) and len(np.shape(mov)) == 3:
        return np.hstack([mov[:,:,frame_num].flatten().reshape((-1,1)) for frame_num in range(mov.shape[2])])    
    else:
        raise ValueError('Unrecognized dimensions for mov (cannot change its dimensions to 2d)')
    
def D2ToMov(mov, frameShape, type_return = 'array'):
    """
    Parameters
    ----------
    mov : TYPE
        DESCRIPTION.
    frameShape : TYPE
        DESCRIPTION.
    type_return : string, can be 'array' or 'list', optional
        The default is 'array'.
        
    Raises
    ------
    ValueError - if dimensions do not fit


    Returns
    -------
    list or np.ndarray (according to the input "type return") of frames with shape frameShape X time
    """
    
    if mov.shape[0] != frameShape[0]*frameShape[1] :
        raise ValueError('Shape of each frame ("frameShape") is not consistent with the length of the data ("mov")')
    if type_return == 'array':
        return np.dstack([mov[:,frame].reshape(frameShape) for frame in range(mov.shape[1])])
    elif type_return == 'list':     
        return [mov[:,frame].reshape(frameShape) for frame in range(mov.shape[1])]
    else:
        raise ValueError('Invalid "type_return" input. Should be "list" or "array"')
    
    
    

def mkDataGraph(data, params = {}, reduceDim = False, reduceDimParams = {}, graph_function = 'gaussian',
                K_sym  = True, use_former = True, data_name = 'none', toNormRows = True):
    """
    Parameters
    ----------
    data : should be neurons X time OR neurons X p
        DESCRIPTION.
    params : TYPE, optional
        DESCRIPTION. The default is {}.
    reduceDim : TYPE, optional
        DESCRIPTION. The default is False.
    reduceDimParams : TYPE, optional
        DESCRIPTION. The default is {}.
    graph_function : TYPE, optional
        DESCRIPTION. The default is 'gaussian'.
    K_sym : TYPE, optional
        DESCRIPTION. The default is True.
    use_former : TYPE, optional
        DESCRIPTION. The default is True.
    data_name : TYPE, optional
        DESCRIPTION. The default is 'none'.
    toNormRows : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    reduceDimParams = {**{'alg':'PCA'},  **reduceDimParams}
    params = addKeyToDict(params_config,
                 params)
    if len(data.shape) == 3:
        data = np.hstack([data[:,:,i].flatten().reshape((-1,1)) for i in range(data.shape[2])])
        print('data was reshaped to 2d')
        # Future: PCA
    if reduceDim:
        pca = PCA(n_components=params['n_comps'])
        data = pca.fit_transform(data)

    #raise ValueError('stop here')
    K = calcAffinityMat(data, params,  data_name, use_former, K_sym, graph_function)
   
    K = K - np.diag(np.diag(K) ) 
    if toNormRows:
        K = K/K.sum(1).reshape((-1,1))
    return K
    

    
def calcAffinityMat(data, params,  data_name, use_former, K_sym = True, graph_function = 'gaussian'):
    
    # data = neurons X time
    n_cols = data.shape[1]
    n_rows = data.shape[0]
    numNonZeros = params['n_neighbors'] * n_cols
    
    # knn_dict is a dictionary with keys 'dist' and 'ind'
    knn_dict = findNeighDict(data, params, data_name, use_former, addi = '_knn', to_save = True)

    matInds = createSparseMatFromInd(knn_dict['ind'], is_mask = True)
    matDists = createSparseMatFromInd(knn_dict['ind'], defVal = knn_dict['dist'], is_mask = False)

    if graph_function == 'gaussian':

        K = gaussian_vals(matDists, std = np.median(matDists[matInds != 0 ]))

    else:
        raise ValueError('Unknown Graph Function')
    if K_sym:
        K = (K + K.T)/2
    return K
    
def findNeighDict(data, params, data_name = 'none', 
                    use_former = True, addi = '_knn', to_save = True):
    """
    """
    save_knn_path = data_name + '%s.npy'%addi #np.save()
    if use_former and os.path.isfile(save_knn_path) :
        knn_dict = np.load(save_knn_path, allow_pickle=True).item()
    else:
        if params['n_neighbors'] > data.shape[1]:
            print('Too many neighbors were required, set it to %d'%int(data.shape[1]/2))
            params['n_neighbors'] = int(data.shape[1]/2)

        nbrs = NearestNeighbors(n_neighbors=params['n_neighbors'], 
                                algorithm=params['alg']).fit(data)
        distances, indices = nbrs.kneighbors(data)
        knn_dict = {'dist': distances, 'ind': indices}
        if to_save:
            np.save(save_knn_path, knn_dict)
    return knn_dict
    
    
def createSparseMatFromInd(inds, M = 0, defVal = 1, is_mask = True ):

    """
    This function find a 0-1 matrix where the non-zeros are located according to inds
    Parameters
    ----------
    inds : np.ndarray [sample index X number of neighbors]
        indices of the neighbors
    M : int, optional
        DESCRIPTION. The default is 0.
    defVal : number OR numpy.ndarray with the same shape of inds, optional
        DESCRIPTION. The default is 1.        

    Returns
    -------
    mat :  np.ndarray of size M X M of 0/1 values

    """
    if M == 0 or M < np.max(inds):
        M = np.max([np.max(inds)+1, inds.shape[0]])
        print('M was changed in "createSparseMatFromInd"')
    mat = np.zeros((M,M))
    if not is_mask: mat += np.inf
    rows = np.repeat(np.arange(inds.shape[0]).reshape((-1,1)),inds.shape[1], axis=1)
    mat[rows,inds] = defVal
    
    return mat
    

def gaussian_vals(mat, std = 1, mean = 0 , norm = False, dimensions = 1, mat2 = [], power = 2):
    """
    check_again
    Parameters
    ----------
    mat : the matrix to consider
    std : number, gaussian std
    mean : number, optionalis 
        mean gaussian value. The default is 0.
    norm : boolean, optional
        whether to divide values by sum (s.t. sum -> 1). The default is False.

    Returns
    -------
    g : gaussian values of mat

    """    
    if dimensions == 1:
        if not checkEmptyList(mat2): warnings.warn('Pay attention that the calculated Gaussian is 1D. Please change the input "dimensions" in "gaussian_vals" to 2 if you want to consider the 2nd mat as well')
        g = np.exp(-((mat-mean)/std)**power)
        if norm: return g/np.sum(g)

    elif dimensions == 2:
        #dim1_mat = np.abs(mat1.reshape((-1,1)) @ np.ones((1,len(mat1.flatten()))))
        #dim2_mat = np.abs((mat2.reshape((-1,1)) @ np.ones((1,len(mat2.flatten())))).T)
        #g= np.exp(-0.5 * (1/std)* (dim1_mat**power + (dim1_mat.T)**power))
        g = gaussian_vals(mat, std , mean , norm , dimensions = 1, mat2 = [], power = power)
        g1= g.reshape((1,-1))
        g2 = np.exp(-0.5/np.max([int(len((mat2-1)/2)),1])) * mat2.reshape((-1,1))
        g = g2 @ g1 
        
        g[int(g.shape[0]/2), int(g.shape[1]/2)] = 0
        if norm:
            g = g/np.sum(g)
        
    else:
        raise ValueError('Invalid "dimensions" input')
    return g
        
    
#%% GD Updates
def update_GDiters(dict_old, A, data, step_s, params):
    """
    Take a step in the negative gradient of the basis: Minimizing the energy E = ||x-Da||_2^2 + lambda*||a||_1^2

    Parameters
    ----------
    dict_old : TYPE
    A : TYPE
    data : TYPE
    step_s : TYPE
        DESCRIPTION.
    l2 : TYPE
        DESCRIPTION.
    params : TYPE,
        DESCRIPTION.

    Returns - new dict
    -------
    """
    for index2 in range(params.get('GD_iters')):
        # Update The basis matrix
        print('dict old inside update_GDiters')
        print(dict_old.sum())
        dict_old = dict_old + (step_s/A.shape[0])*((data.T - dict_old @ A.T) @ A) 
        print('dict old inside update_GDiters')
        print(dict_old.sum())
    # This part is basically the same, only for the hyyperspectral, care needs to be taken to saturate at 0,
    # so that no negative relflectances are learned. 
    if params.get('nonneg'):
        dict_old[dict_old < 0] = 0
        if np.sum(dict_old) ==0:
            raise ValueError('fgdgdfgdfgfgfdgfgfdglkfdjglkdjglkfdjglkdjflgk')
    return dict_old
    
def update_GDwithForb(dict_old, A, data, step_s, l2, params):
    """
    Take a step in the negative gradient of the basis:
    This time the Forbenious norm is used to reduce unused basis elements. The energy function being minimized is then:
    E = ||x-Da||_2^2 + lambda*||a||_1^2 + lamForb||D||_F^2
    
    Parameters
    ----------
    dict_old : TYPE
    A : TYPE
    data : TYPE
    step_s : TYPE
        DESCRIPTION.
    l2 : TYPE
        DESCRIPTION.
    params : TYPE
        DESCRIPTION.

    Returns - new dict
    -------
    """
    for index2 in range(params.get('GD_iters')):
        # Update The basis matrix
        dict_new = dict_old + (step_s)*((data.T - dict_old @ A.T) @ A -l2*dict_old) @ np.diag(1/(1+np.sum(A != 0, 0)));
    
        # For some data sets, the basis needs to be non-neg as well
        if params.get('nonneg'):
            dict_new[dict_new < 0] = 0
    return dict_new
    
def update_FullLS(dict_old, A, data, params):
    """
    Minimizing the energy:
    E = ||X-DA||_2^2 via D = X*pinv(A)
    
    Parameters
    ----------
    dict_old : TYPE
    A : TYPE
    data : TYPE
    params : TYPE

    Returns
    -------     dict_new
    """
    raise ValueError('how did you arrive here?')
    if params.get('nonneg'):
        dict_new = np.zeros(size(dict_old))                                  # Initialize the dictionary
        n_times = dict_old.shape[0]
        for  t in range(n_times):
            dict_new[t,:] = nnls(A, data[:,t]) # Solve the least-squares via a nonnegative program on a per-dictionary level                   
    else:
        dict_new = data.T @ np.pinv(A);                                         # Solve the least-squares via an inverse

    return  dict_new


def  update_LSwithCont(dict_old, A, data, l3, params):    
    """    
    Minimizing the energy:    E = ||X-DA||_2^2 + l3*||D_old - D||_F^2 via D = [X;D_old]*pinv([A;I])    
    
    Parameters
    ----------
    dict_old : TYPE
    A : TYPE
    data : TYPE
    l2 : TYPE
    l3 : TYPE
    params : TYPE

    Returns
    -------     dict_new
    """
    if params.get('nonneg'):
        dict_new = np.zeros(dict_old.shape)                                      # Initialize the dictionary
        n_times = dict_old.shape[0]
        n_neurons = A.shape[0]
        for t  in range(n_times):
            dict_new[t,:] = nnls( np.vstack([A.T, l3*np.eye(n_neurons)  ]),
                                            np.vstack([data[:,t].reshape((-1,1)),
                                                       l3*dict_old[t,:].reshape((-1,1)) ]) );     # Solve the least-squares via a nonnegative program on a per-dictionary level

    else:
        dict_new = np.vstack([data,l3*dict_old.T,l2*dict_old]) @ np.linalg.pinv(np.vstack([A.T,l3*np.eye(n_neurons)])) # Solve the least-squares via an inverse
    return  dict_new
 
def update_LSwithContForb(dict_old, A, data, l2, l3, params):
    """
    Minimizing the energy:
    E = ||data.T-DA.T||_2^2 + l3*||D_old - D||_F^2 + l2*||D||_F^2 ,                      via phi = [data.T;phi_old]*pinv([A.T;I])
    
    Parameters
    ----------
    dict_old : TYPE
    A : TYPE
    data : TYPE
    l2 : TYPE
    l3 : TYPE
    params : TYPE

    Returns
    -------
    dict_new
    """
    if params.get('nonneg'):
        dict_new = np.zeros(dict_old.shape)                                      # Initialize the dictionary
        n_times = dict_old.shape[0]
        n_neurons = A.shape[0]
        for t  in range(n_times):
            dict_new[t,:] = nnls( np.vstack([A.T, l3*np.eye(n_neurons),np.zeros((n_neurons, n_neurons))  ]),
                                            np.vstack([data[:,t].reshape((-1,1)),
                                                       l3*dict_old[t,:].reshape((-1,1)),
                                                      l2*dict_old[t,:].reshape((-1,1)) ]) );     # Solve the least-squares via a nonnegative program on a per-dictionary level

    else:
        dict_new = np.vstack([data,l3*dict_old.T,l2*dict_old]) @  np.linalg.pinv(np.vstack([A.T,l3*np.eye(n_neurons),zeros((n_neurons, n_neurons))])); # Solve the least-squares via an inverse
    return  dict_new
     
def   update_LSwithForb(dict_old, A, data, l2, params):
    """
    Minimizing the energy:
    E = ||X-DA||_2^2 + l2*||D||_F^2
                 via  D = X*A^T*pinv(AA^T+lamForb*I)
    
    Parameters
    ----------
    dict_old : np.ndarray, T X p
        temporal profiles dict
    A : np.ndarray, N X p
        neural nets
    data : np.ndarray, N X T
        neural recordings
    l2: number (regularization)
    params : options

    Returns
    -------
    dict_new : np.ndarray, T X p
        temporal profiles dict

    """

    if params.get('nonneg'):
        #future
        warnings.warn('Regularized non-negative ls is not implemented yet! Solving without non-negative constraints...\n')  
    dict_new = data.T @ A @ np.linalg.pinv(A.T @ A + l2*np.eye(A.shape[1])); # Solve the least-squares via an inverse
    return dict_new
    
def  update_FullLsCor(dict_old, A, data, l2, l3, l4, params):
    """
    E = ||X-DA||_2^2 + l4*||D.'D-diag(D.'D)||_sav + l2*||D||_F^2 + l3*||D-Dold||_F^2 
        
    Parameters
    ----------
    dict_old : np.ndarray, T X p
        temporal profiles dict
    A : np.ndarray, N X p
        neural nets
    data : np.ndarray, N X T
        neural recordings
    l2, L3, L4 : numbers (regularization)
    params : options

    Returns
    -------
    dict_new : np.ndarray, T X p
        temporal profiles dict

    """
    if params.get('nonneg'): # if non-negative matrix factorization
        dict_new = np.zeros(dict_old.shape);                                  # Initialize the dictionary
        n_nets    = dict_old.shape[1]
        n_times    = dict_old.shape[0]   

        # Solve the least-squares via a nonnegative program on a per-dictionary level
        for t in range(n_times): #efficiencyMarker
            dict_new[t,:] = solve_qp(2*A.T @ A + l4 + (l3+l2-l4)*np.eye(n_nets), 
                                     ( -2*A.T @ data[:,t] + l3*dict_old[t,:]).reshape((1,-1)) 
                                     , solver = params['solver_qp'] )

    else:
        dict_new = data.T @ A @ np.linalg.pinv(A.T @ A + l4*(1-np.eye(A.shape[1]))) ; # Solve the least-squares via an inverse
    return dict_new

def sparseDeconvDictEst(dict_old, A, data, l2, params):
    """
    This function should return the solution to the optimiation
    S = argmin[||A - (l2*S)data||_F^2 + ]
    D_i = l2*S_i
    
    
    Parameters
    ----------
    dict_old : np.ndarray, T X p
        temporal profiles dict
    A : np.ndarray, N X p
        neural nets
    data : np.ndarray, N X T
        neural recordings
    l2 : number (regularization)
    params : dict
    
    Returns
    -------
    phi : np.ndarray, T X p
        temporal profiles dict

    """
    

    #return phi
    raise ValueError('Function currently not available. Please change the "GD_type" from "sparse_deconv"')
    pass




    
    
    
    
    
    
#%%  Other pre-processing
def norm_mat(mat, type_norm = 'evals', to_norm = True):
  """
  This function comes to norm matrices by the highest eigen-value
  Inputs:
      mat       = the matrix to norm
      type_norm = what type of normalization to apply. Can be 'evals', 'unit' or 'none'.
      to_norm   = whether to norm or not to.
  Output:  
      the normalized matrix
  """    
  if to_norm and type_norm != 'none':
    if type_norm == 'evals':
      eigenvalues, _ =  linalg.eig(mat)
      mat = mat / np.max(np.abs(eigenvalues))
    elif type_norm == 'unit':
      mat = mat @ np.diag(1 / np.sqrt(np.sum(mat**2,0))) 
         
  return mat

def str2bool(str_to_change):
    """
    Transform 'true' or 'yes' to True boolean variable 
    Example:
        str2bool('true') - > True
    """
    if isinstance(str_to_change, str):
        str_to_change = (str_to_change.lower()  == 'true') or (str_to_change.lower()  == 'yes')
    return str_to_change


#%% Plotting Functions

def visualize_images(to_use_array = True, to_norm = True,
        folder_path =  r'E:\CODES FROM GITHUB\GraFT-analysis\code\neurofinder.02.00\images'  ):
    if to_use_array: 
        array_images =  from_folder_to_array(folder_path)
        if to_norm:
            array_images = array_images/np.maximum([np.max(array_images,0 ), np.max(array_images,1)]).reshape((1,1,-1))
            
    
    
def from_folder_to_array(path_images =  r'E:\CODES FROM GITHUB\GraFT-analysis\code\neurofinder.02.00\images' 
                         , max_images = 100):
    if isinstance(path_images,(np.ndarray, list)):
        pass
    elif isinstance(path_images,str):
        files = os.listdir(path_images)
        files = np.sort(files)
    return np.dstack([load_image_to_array(path_images = path_images, image_to_load = cur_file) for counter, cur_file in enumerate(files) if counter < max_images])
    
    
def load_image_to_array(path_images =  r'E:\CODES FROM GITHUB\GraFT-analysis\code\neurofinder.02.00\images',
               image_to_load = 'image07971.tiff'):
    im_path = path_images + '\%s'%image_to_load
    im = io.imread(im_path)
    imarray = np.array(im)
    return imarray

    
def slider_changed(event):  
    val = slider.get()
    ax.imshow(array_images[:,:,int(val)])

    
    
    
 
    