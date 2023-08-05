# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 11:47:51 2022

@author: noga mudrik
"""
from main_functions_graft import *

full_ask = str2bool(input('to ask full? (true / false)'))
if full_ask:
    use_former_kernel = str2bool(input('to use  former kernel? (true or false)') )
    usePatch = False #str2bool(input('to use patch? (true or false)') )
    portion =str2bool(input('To take portion?'))
    divide_med = str2bool(input('divide by median? (true or false)'))
    GD_type = input('GD type (e.g. full_ls_cor')# 'norm'
    to_save = str2bool(input('to save?'))
else:
    use_former_kernel = False
    usePatch = False #str2bool(input('to use patch? (true or false)') )
    portion =True# str2bool(input('To take portion?'))
    divide_med = False# str2bool(input('divide by median? (true or false)'))
    GD_type ='norm'# 'full_ls_cor'#'norm'
    data_0_1 = False
    to_save = False #str2bool(input('to save?'))


from datetime import date


if to_save:
    save_name = input('save name:')
params_full = {'max_learn': 1e3,
    'mean_square_error': 1,
    'learn_eps': 0.01,
    
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
    'verbose': 10,                                              # Default to full verbosity level
    'likely_form' : 'gaussian',                                      # Default to a gaussian likelihood ('gaussian' or'poisson')
    'step_s': 5, #1,                                               # Default step to reduce the step size over time (only needed for grad_type ='norm')
    'step_decay': 0.999,                                           # Default step size decay (only needed for grad_type ='norm')
    'max_learn': 1e3,                                             # Maximum number of steps in learning is 1000 
    'dict_max_error': 0.01,       # learn_eps                                    # Default learning tolerance: stop when Delta(Dictionary)<0.01
    'p': 4,                        # Default number of dictionary elements is a function of the data
    'verb': 1,                                               # Default to no verbose output
    'grad_type':GD_type,                                   # Default to optimizing a full optimization on all dictionary elements at each iteration
    'GD_iters': 1,                                               # Default to one GD step per iteration
    'bshow': 0,                                               # Default to no plotting
                                                  # Default to not having negativity constraints
    'nonneg': False,                                           # Default to not having negativity constraints on the coefficients
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
     'norm_by_lambdas_vec': False,
     'GD_type': GD_type#'full_ls_cor'
    }

xmin = 0
xmax = 0
path_images_def = r'E:\CODES FROM GITHUB\GraFT-analysis\code\neurofinder.02.00\images'
#image_example = 'image07971.tiff'

path_images = '0'#input('path images (0 for default)')
if path_images == '0': path_images = path_images_def
if portion: 
    if not full_ask:
        xmin = 151#151
        xmax = 200#350                                                            # Can sub-select a portion of the full FOV to test on a small section before running on the full dataset
        ymin = 151#101
        ymax = 200#300  
    else:
        xmin = int(input('xmin'))#151
        xmax = int(input('xmax'))#350                                                            # Can sub-select a portion of the full FOV to test on a small section before running on the full dataset
        ymin = int(input('ymin'))#101
        ymax = int(input('ymax'))#300 
    try:
        data = np.load('data_calcium_xmin_%d_xmax_%d_ymin_%d_ymax_%d.npy'%(xmin,xmax,ymin,ymax))
    except:
        data =  from_folder_to_array(path_images, max_images = 100)
                
        data = data[xmin:xmax, ymin:ymax,:]
        #print('data shape2')
        #print(data.shape)
        np.save('data_calcium_xmin_%d_xmax_%d_ymin_%d_ymax_%d.npy'%(xmin,xmax,ymin,ymax), data)
else:    
    try:
        data = np.load('data_calcium.npy')
    except:
        data =  from_folder_to_array(path_images, max_images = 100)
                
    #data = data[xmin:xmax, ymin:ymax,:]
#max_in_frame = [np.max(imarray[:,:,frame].flatten()) for frame in range(imarray.shape[2]) ]


if divide_med:
    data = data/np.median(data)
if data_0_1:
    data = data/data.sum()
if use_former_kernel:
    try:
        if xmin > 0 and xmax != 0:
            corr_kern = np.load('kernel_calcium_xmin_%d_xmax_%d_ymin_%d_ymax_%d.npy'%(xmin,xmax,ymin,ymax))
        else:
            corr_kern = np.load('kernel_calcium.npy')
    except:    
        corr_kern  = mkDataGraph(data, params_full, reduceDim = params_full['reduceDim'], 
                             reduceDimParams = {'alg':'PCA'}, graph_function = 'gaussian',
                    K_sym  = True, use_former = False, data_name = 'try_graft', toNormRows = True)
        if xmin > 0 and xmax != 0:
            np.save('kernel_calcium_xmin_%d_xmax_%d_ymin_%d_ymax_%d.npy'%(xmin,xmax,ymin,ymax), corr_kern)
        else:
            np.save('kernel_calcium.npy', corr_kern)
else:
    corr_kern  = mkDataGraph(data, params_full, reduceDim = params_full['reduceDim'], 
                         reduceDimParams = {'alg':'PCA'}, graph_function = 'gaussian',
                K_sym  = True, use_former = False, data_name = 'try_graft', toNormRows = True)
    if xmin > 0 and xmax != 0:
        np.save('kernel_calcium_xmin_%d_xmax_%d_ymin_%d_ymax_%d.npy'%(xmin,xmax,ymin,ymax), corr_kern)
    else:
        np.save('kernel_calcium.npy', corr_kern)
        
print('Running');

if usePatch:
    raise ValueError('Use Patch is not available yet!')
    #[S, D] = patchGraFT(data,params['p'],[],corr_kern,params_full);      # Learn the dictionary using patch-based code 
else:
    [phi, A] = GraFT(data, [], corr_kern, params_full);                    # Learn the dictionary (no patching - will be much more memory intensive and slower)

if to_save:
    path_name = 'date_'+ str(date.today())
    if not os.path.exists(path_name):
        os.makedirs(path_name)
    
    np.save(path_name + sep + save_name + '.npy', {'phi':phi, 'A':A, 'data':data, 'params':params_full, 'xmin': xmin, 
                                                   'xmax':xmax, 'ymin':ymin, 'ymax':ymax, 'divide_med':divide_med, 
                                                   'usePatch':usePatch, 'shape':data.shape})
print('Finished running GraFT.\n')

