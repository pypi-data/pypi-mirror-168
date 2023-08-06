import numpy as np
from misic_ui.misic.misic import *
from misic_ui.misic.extras import *
from misic_ui.misic.utils import *
from skimage.exposure import adjust_gamma
from skimage.filters import gaussian, laplace, unsharp_mask

def shape_data(data):
    size = data.shape
    N = len(size)
    # single image single channel
    if N ==2:
        # single frames
        return data[np.newaxis,:,:]

    return data 

def preprocess(im, params):
    im = (1.0 - normalize2max(im)) if params['invert'] else im

    im = im if params['scale']==1 else rescale(im,params['scale'],preserve_range=True)
    im = im if params['gamma'] == 1 else adjust_gamma(im,params['gamma'])
    im = unsharp_mask(im,params['sharpness_sigma'],params['sharpness_amount']) if params['sharpness_sigma'] > 0 else im
    
    if params['gaussian_laplace']:
        im = gaussian(laplace(im),2.2)
    im = add_noise(im,params['sensitivity']) if params['local_noise'] else random_noise(im,mode = 'gaussian',var = params['sensitivity']/100.0)
    return im