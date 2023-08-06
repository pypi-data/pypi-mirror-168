try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

## import required functions
import os
# ignore gpu: this needs to rectfied incase there is gpu access to tensorflow
# os.environ["CUDA_VISIBLE_DEVICES"]="-1" 
import tensorflow as tf
try:
    physical_devices = tf.config.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
except:
    pass

import numpy as np
from skimage.transform import rescale,resize
from skimage.feature import shape_index
from skimage.util import random_noise

# import MiSiC Stuff
from misic_ui.misic.misic import *
from misic_ui.misic.extras import *
from misic_ui.misic.utils import *
# get helper functions
from misic_ui.misic_helpers import *

from napari_plugin_engine import napari_hook_implementation
from magicgui import magic_factory
from magicgui.tqdm import trange
from napari import Viewer
from napari.layers import Image

import pathlib
import json

from magicgui.widgets import FunctionGui

# make misic
mseg = MiSiC()

# make default params dictionary
params = {}
params['invert'] = True
params['scale'] = 1.0
params['gamma'] = 0.5
params['sharpness_sigma'] = 0
params['sharpness_amount'] = 2
params['gaussian_laplace'] = False
params['sensitivity'] = 0.001
params['local_noise'] = True
params['post_process'] = True
params['roi'] = [0,0,256,256]
params['use_roi'] = True
params['mean_width'] = 10

standard_width = 9.87

def segment_single_image(im,params):
    '''
    Segments single iamge using the parameters dictionary.
    '''
    sr,sc = im.shape
    roi = params['roi'] 
    roi[0] = int(max(roi[0],0))
    roi[1] = int(max(roi[1],0))
    roi[2] = int(min(roi[2],sr))
    roi[3] = int(min(roi[3],sc))
    params['roi']  = roi
    
    if params['use_roi']:
        roi = params['roi']
        tmp = im[roi[0]:roi[2],roi[1]:roi[3]]
        tsr,tsc = tmp.shape
        tmp = preprocess(tmp,params)
        yp = mseg.segment(tmp,exclude = 16,invert = False)[:,:,0]
        yp = resize(yp,(tsr,tsc))   
        if params['post_process']:
            yp = postprocessing(im[roi[0]:roi[2],roi[1]:roi[3]] if params['invert'] else -im[roi[0]:roi[2],roi[1]:roi[3]],yp,int(standard_width/params['scale']))                
        #res = np.zeros((sr,sc),dtype = yp.dtype)
        #res[roi[0]:roi[2],roi[1]:roi[3]] = yp
    else:
        tmp = preprocess(im,params)
        yp = mseg.segment(tmp,exclude = 16,invert = False)[:,:,0]
        yp = resize(yp,(sr,sc))    
        if params['post_process']:
            yp = postprocessing(im if params['invert'] else -im,yp,int(standard_width/params['scale']))   
        #res = yp

    if np.max(yp) == 1:
        yp = yp *255

    return yp #(yp*255).astype(np.uint8)



@magic_factory(result_widget=True,call_button='get cell-width')
def get_width(viewer: Viewer) -> int:    
    '''
    Make a Shapes layer named 'cell_width' if it doesnt exists.
    Get the mean width of multiple lines to obtain the working scale
    '''
    try:
        lines = viewer.layers['cell_width'].data    
        mean_width0 = 0
        for l in lines:
            mean_width0 += np.sqrt((l[0][0]-l[1][0])**2 + (l[0][1]-l[1][1])**2)
        mean_width0/=len(lines)
        mean_width0 = round(mean_width0,2)
        params['scale'] = standard_width/mean_width0   
    except:
        viewer.add_shapes(shape_type='lines',name = 'cell_width',edge_width=2,edge_color='orange')
        mean_width0 = standard_width

    return mean_width0   


## MagicGui widget for single image segmentation
@magic_factory(auto_call=True,
use_roi = {"widget_type": "CheckBox", "value": params['use_roi'], 'tooltip': 'Select ROI for fast parameter selection.'}, 
light_background = {"widget_type": "CheckBox", "value": params['invert'],'tooltip': 'Select for phase contrast images.'}, 
use_local_noise = {"widget_type": "CheckBox", "value": params['local_noise'],'tooltip': 'Use local noise variance to reduce false positives.'}, 
gaussian_laplace = {"widget_type": "CheckBox", "value": params['gaussian_laplace'], 'tooltip': 'Select when segmenting fluorescence images.'}, 
adjust_scale = {"widget_type": "FloatSlider", "value": 1.0, "max": 1.5,"min": 0.7,"step":0.025,'tracking': False,'readout' : True,'tooltip': 'Fine-tune the scale around the mean cell width.'}, 
noise_var = {"widget_type": "FloatSlider", "value": params['sensitivity'], "max": 0.50,"min": 0.00,"step":0.0001,'tracking': False,'readout' : True,'tooltip': 'Reduce false positives by adding noise.'},
gamma = {"widget_type": "FloatSlider", "value": params['gamma'], "max": 2.5,"min": 0.1,"step":0.05,'tracking': False,'readout' : True,'tooltip': 'Gamma correction.'},
sharpness_sigma = {"widget_type": "FloatSlider", "value": params['sharpness_sigma'], "max": 3,"min": 0,"step":0.25,'tracking': False,'readout' : True,'tooltip': 'Sharpness scale in unsharp mask.'},
sharpness_amount = {"widget_type": "FloatSlider", "value": params['sharpness_amount'], "max": 5,"min": 0.5,"step":0.5,'tracking': False,'readout' : True,'tooltip': 'Sharpness amount in unsharp mask.'},
post_process = {"widget_type": "CheckBox", "value": params['post_process'], 'tooltip': 'select to post process and return labels instead of probability map.'}, 
run = {"widget_type": "PushButton", 'value': True,'tooltip': 'Run again.'})
def segment(viewer: Viewer,data: 'napari.types.ImageData',
use_roi: bool, 
light_background: bool,
use_local_noise : bool,
gaussian_laplace: bool,
adjust_scale : float,
noise_var: float, 
gamma: float,
sharpness_sigma: float,
sharpness_amount: float,
post_process: bool,
run = False,) -> 'napari.types.LayerDataTuple':
    '''
    Get parameters for a single image and output segmented image.
    '''
    # Make ROI
    try:
        roi = viewer.layers['roi'].data[0]
    except:
        roi = np.array([[0,0],[256,256]])
        viewer.add_shapes(roi, shape_type='rectangle', name = 'roi',edge_width=2,edge_color='red', face_color='black')

    # get roi and parameters dictionary
    roi = viewer.layers['roi'].data[0]
    roi = np.array(roi)
    params['roi'] = [np.min(roi[:,0]),np.min(roi[:,1]),np.max(roi[:,0]),np.max(roi[:,1])]
    scale = min(standard_width/params['mean_width'],2.5)*adjust_scale 
    params['invert'] = light_background
    params['scale'] = scale
    params['gamma'] = gamma
    params['sharpness_sigma'] = sharpness_sigma
    params['sharpness_amount'] = sharpness_amount
    params['gaussian_laplace'] = gaussian_laplace
    params['sensitivity'] = noise_var
    params['local_noise'] = use_local_noise
    params['post_process'] = post_process
    params['use_roi'] = use_roi

    #print('global: ', params)

    try:
        sr,sc = data.shape[-2],data.shape[-1]
    except:
        return 0        
    if viewer.dims.ndim == 3:
        fnum = viewer.dims.current_step[0]
        im = np.copy(data[fnum])        
    else:
        im = np.copy(data)            
    #status = 'MiSiC: processing ...'
    yp = segment_single_image(im,params)        

    if params['post_process']:
        if params['use_roi']:
            roi = params['roi']
            try:
                res = viewer.layers['segmentation'].data
                res[roi[0]:roi[2],roi[1]:roi[3]] = yp
            except:
                res = np.zeros((sr,sc),dtype = yp.dtype)
                res[roi[0]:roi[2],roi[1]:roi[3]] = yp
        else:
            res = yp

        try:
            del viewer.layers['probability-map']
            return (res,{'name': 'segmentation','opacity': 0.75}, 'labels')
        except:
            return (res,{'name': 'segmentation','opacity': 0.75}, 'labels')

    else:
        if params['use_roi']:
            roi = params['roi']
            try:
                res = viewer.layers['probability-map'].data
                res[roi[0]:roi[2],roi[1]:roi[3]] = yp
            except:
                res = np.zeros((sr,sc),dtype = yp.dtype)
                res[roi[0]:roi[2],roi[1]:roi[3]] = yp
        else:
            res = yp

        try:
            del viewer.layers['segmentation']
            return (res,{'name': 'probability-map','opacity': 0.75, 'blending': 'additive', 'colormap' : 'green'}, 'image') 
        except:
            return (res,{'name': 'probability-map','opacity': 0.75, 'blending': 'additive', 'colormap' : 'green'}, 'image') 

# once the parameters are the selected for single image, then process the stack
@magic_factory()
def segment_stack(data: "napari.types.ImageData") -> 'napari.types.LayerDataTuple':
    '''
    Segment the entire stack using the parameters obtained before
    '''
    params['scale'] = min(params['scale'],2.5)
    use_roi = params['use_roi']
    params['use_roi'] = False
        
    if len(data.shape) < 3:
        yp = segment_single_image(np.copy(data),params)
    else:
        im = np.copy(data)
        yp = np.array([segment_single_image(im[i],params) for i in trange(len(im))])  
    params['use_roi'] = use_roi       

    try:
        del viewer.layers['misic-seg']
    except:
        pass
    if params['post_process']:
        return (yp,{'name': 'misic-seg','opacity': 0.75}, 'labels')
    else:        
        return (yp,{'name': 'misic-seg','opacity': 0.75, 'blending': 'additive', 'colormap' : 'green'}, 'image') 


############ Save or Load parameters file
@magic_factory(output_folder={'mode': 'd'},call_button='Save')
def save_params(output_folder =  pathlib.Path.home(),filename = 'params'):
    '''
    Save parameters to file
    '''
    output_folder = os.path.normpath(output_folder)
    filename = output_folder + os.path.sep + filename + '.json'
    
    json.dump( params, open( filename, 'w' ) )

@magic_factory(result_widget = True,filename={'mode': 'r',"filter": "*.json"},call_button='Show')
def show_params(filename =  pathlib.Path.home()):
    '''
    Load parameters to file
    '''    
    params = json.load( open( filename, "rb" ) ) 
    s = ''
    for k in params.keys():
        s += k + ' : ' + str(params[k]) + '\n'    

    # print(segment)
    # gui = FunctionGui(segment)

    # segment(use_roi = params['use_roi'], light_background = params['invert'],
    #     use_local_noise = params['local_noise'],
    #     gaussian_laplace = params['gaussian_laplace'],
    #     adjust_scale = 1.0,
    #     noise_var = params['sensitivity'], 
    #     gamma = params['gamma'],
    #     sharpness_sigma = params['sharpness_sigma'],
    #     sharpness_amount = params['sharpness_amount'],
    #     post_process = params['post_process'])

    # # print('before:', globals()['segment'].light_background)
    # # globals()['segment'].use_roi = params['use_roi']
    # # globals()['segment'].light_background = params['invert']
    # # globals()['segment'].use_local_noise = params['local_noise']
    # # globals()['segment'].gaussian_laplace = params['gaussian_laplace']
    # # globals()['segment'].adjust_scale = params['local_noise']
    # # globals()['segment'].noise_var = params['sensitivity']
    # # globals()['segment'].gamma = params['gamma']
    # # globals()['segment'].sharpness_amount = params['sharpness_amount']
    # # globals()['segment'].sharpness_sigma = params['sharpness_sigma']
    # # globals()['segment'].post_process = params['post_process']
    # # print(globals()['segment'].light_background)

    return s


    
############ napari hooks
@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return [get_width,segment,segment_stack,save_params]

