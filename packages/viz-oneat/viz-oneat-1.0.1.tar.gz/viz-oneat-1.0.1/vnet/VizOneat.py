import os
import sys
import tensorflow as tf
from oneat.NEATModels.nets import Concat
from oneat.NEATModels.loss import diamond_yolo_loss, class_yolo_loss, static_yolo_loss_segfree,static_yolo_loss, dynamic_yolo_loss
from pathlib import Path
from oneat.NEATUtils.utils import  load_json, normalizeFloatZeroOne
import numpy as np
from keras import models
from keras.models import load_model
from tifffile import imread
import napari
from vollseg import VollSeg, CARE, UNET, StarDist2D, StarDist3D, MASKUNET
class VizOneat(object):

    def __init__(self,  config, imagename, model_dir, model_name, oneat_vollnet = False,
                 oneat_lstmnet = False, oneat_cnnnet = False, oneat_staticnet = False,
                 voll_starnet_2D = False, voll_starnet_3D = False, voll_unet = False, voll_care = False,
                 catconfig=None, cordconfig=None, layer_viz_start = None, layer_viz_end = None, dtype = np.uint8, n_tiles = (1,1,1), normalize = True):

        self.config = config
        self.model_dir = model_dir
        self.model_name = model_name
        self.n_tiles = n_tiles
        self.imagename = imagename
        self.dtype = dtype
        self.catconfig = catconfig
        self.cordconfig = cordconfig
        self.oneat_vollnet = oneat_vollnet 
        self.oneat_lstmnet = oneat_lstmnet 
        self.oneat_cnnnet = oneat_cnnnet 
        self.oneat_staticnet = oneat_staticnet
        self.voll_starnet_2D = voll_starnet_2D
        self.voll_starnet_3D = voll_starnet_3D
        self.voll_unet = voll_unet
        self.voll_care = voll_care
        self.layer_viz_start = layer_viz_start 
        self.layer_viz_end = layer_viz_end
        self.image = imread(imagename).astype(self.dtype)
        self.normalize = normalize
        self.viewer = napari.Viewer()   
        self.all_max_activations = []
        if self.config != None:
            self.npz_directory = config.npz_directory
            self.npz_name = config.npz_name
            self.npz_val_name = config.npz_val_name
            self.key_categories = config.key_categories
            self.stage_number = config.stage_number
            self.last_conv_factor = 2 ** (self.stage_number - 1)
            self.show = config.show
            self.key_cord = config.key_cord
            self.box_vector = len(config.key_cord)
            self.categories = len(config.key_categories)
            self.depth = config.depth
            self.start_kernel = config.start_kernel
            self.mid_kernel = config.mid_kernel
            self.learning_rate = config.learning_rate
            self.epochs = config.epochs
            self.startfilter = config.startfilter
            self.batch_size = config.batch_size
            self.multievent = config.multievent
            self.imagex = config.imagex
            self.imagey = config.imagey
            self.imagez = config.imagez
            self.imaget = config.size_tminus + config.size_tplus + 1
            self.size_tminus = config.size_tminus
            self.size_tplus = config.size_tplus

            self.nboxes = config.nboxes
            self.gridx = 1
            self.gridy = 1
            self.gridz = 1
            self.yolo_v0 = config.yolo_v0
            self.yolo_v1 = config.yolo_v1
            self.yolo_v2 = config.yolo_v2
            self.stride = config.stride
        if self.config == None:
            if self.oneat_vollnet: 
               self.config = load_json(os.path.join(self.model_dir, self.model_name) + '_Parameter.json')
            

            self.npz_directory = self.config['npz_directory']
            self.npz_name = self.config['npz_name']
            self.npz_val_name = self.config['npz_val_name']
            self.key_categories = self.catconfig
            self.box_vector = self.config['box_vector']
            self.show = self.config['show']
            self.key_cord = self.cordconfig
            self.categories = len(self.catconfig)
            self.depth = self.config['depth']
            self.start_kernel = self.config['start_kernel']
            self.mid_kernel = self.config['mid_kernel']
            self.learning_rate = self.config['learning_rate']
            self.epochs = self.config['epochs']
            self.startfilter = self.config['startfilter']
            self.batch_size = self.config['batch_size']
            self.multievent = self.config['multievent']
            self.imagex = self.config['imagex']
            self.imagey = self.config['imagey']
            self.imagez = self.config['imagez']
            self.imaget = self.config['size_tminus'] + self.config['size_tplus'] + 1
            self.size_tminus = self.config['size_tminus']
            self.size_tplus = self.config['size_tplus']
            self.nboxes = self.config['nboxes']
            self.stage_number = self.config['stage_number']
            self.last_conv_factor = 2 ** (self.stage_number - 1)
            self.gridx = 1
            self.gridy = 1
            self.gridz = 1
            self.yolo_v0 = self.config['yolo_v0']
            self.yolo_v1 = self.config['yolo_v1']
            self.yolo_v2 = self.config['yolo_v2']
            self.stride = self.config['stride']
        if self.multievent == True:
                self.entropy = 'binary'

        if self.multievent == False:
            self.entropy = 'notbinary'

    def PrepareNet(self):
        
        if self.normalize: 
            self.image = normalizeFloatZeroOne(self.image, 1, 99.8, dtype = self.dtype)
            
        if self.oneat_vollnet: 
            
            self.pad_width = (self.image.shape[-3], self.image.shape[-2], self.image.shape[-1])  
            self.yololoss = diamond_yolo_loss(self.categories, self.gridx, self.gridy, self.gridz, self.nboxes,
                                            self.box_vector, self.entropy, self.yolo_v0, self.yolo_v1, self.yolo_v2)
        
        if self.oneat_cnnnet:
            self.pad_width = (self.image.shape[-3], self.image.shape[-2], self.image.shape[-1]) 
            self.yololoss = static_yolo_loss(self.categories, self.gridx, self.gridy, self.nboxes, self.box_vector,
                                                        self.entropy, self.yolo_v0)
        
        if self.oneat_lstmnet:
            self.pad_width = (self.image.shape[-3], self.image.shape[-2], self.image.shape[-1]) 
            self.yololoss = dynamic_yolo_loss(self.categories, self.gridx, self.gridy, self.gridt, self.nboxes,
                                          self.box_vector, self.entropy, self.yolo_v0, self.yolo_v1, self.yolo_v2)

        if self.oneat_staticnet:
            self.pad_width = (self.image.shape[-2], self.image.shape[-1]) 
            self.yololoss = static_yolo_loss(self.categories, self.gridx, self.gridy, self.nboxes, self.box_vector,
                                                        self.entropy, self.yolo_v0)

        
        
         
        
        if self.oneat_cnnnet or self.oneat_lstmnet or self.oneat_staticnet or self.oneat_vollnet:
                self.model = load_model(os.path.join(self.model_dir, self.model_name) + '.h5',
                                custom_objects={'loss': self.yololoss, 'Concat': Concat}) 
        elif self.voll_starnet_2D:
                self.pad_width = (self.image.shape[-2], self.image.shape[-1]) 
                self.model =  StarDist2D(None, name=self.model_name, basedir=self.model_dir)         
        elif self.voll_starnet_3D:
                self.pad_width = (self.image.shape[-3], self.image.shape[-2], self.image.shape[-1]) 
                self.model =  StarDist3D(None, name=self.model_name, basedir=self.model_dir)     
        elif self.voll_unet:
                if len(self.image.shape >=3):
                     self.pad_width = (self.image.shape[-3], self.image.shape[-2], self.image.shape[-1]) 
                else:
                     self.pad_width = (self.image.shape[-2], self.image.shape[-1])      
                self.model =  UNET(None, name=self.model_name, basedir=self.model_dir)   
        elif self.voll_care:
                if len(self.image.shape >=3):
                     self.pad_width = (self.image.shape[-3], self.image.shape[-2], self.image.shape[-1]) 
                else:
                     self.pad_width = (self.image.shape[-2], self.image.shape[-1])
                self.model =  CARE(None, name=self.model_name, basedir=self.model_dir)
                
        inputtime = int(self.size_tminus)   
                                 
        self.smallimage = CreateVolume(self.image, self.size_tminus, self.size_tplus, inputtime)
        
        self.smallimage = np.expand_dims(self.smallimage,0) 
        layer_outputs = [layer.output for layer in self.model.layers[self.layer_viz_start:self.layer_viz_end]]
        self.activation_model = models.Model(inputs= self.model.input, outputs=layer_outputs)
        
        if self.oneat_vollnet:
            self.VizVollNet()
        self.activations = self.activation_model.predict(self.smallimage)
        self.prediction = self.model.predict(self.smallimage)
        print(type(self.activations), len(self.activations), self.prediction)
        if self.layer_viz_start is None:
            self.layer_viz_start = 0 
        if self.layer_viz_start < 0:
             self.layer_viz_start = len(self.activations) + self.layer_viz_start    
        if self.layer_viz_end is None:
            self.layer_viz_end = len(self.activations)    
        if self.layer_viz_end < 0:
             self.layer_viz_end = self.layer_viz_end + self.layer_viz_end + 1
        assert self.layer_viz_end > self.layer_viz_start, f'The end layer {self.layer_viz_end} of activation should be greater than start layer {self.layer_viz_start}'
        
                 
        
        
        
        
    def VizActivations(self):
        
        for count, activation in enumerate(self.activations):
            max_activation = np.sum(activation, axis = -1)
            max_activation = normalizeFloatZeroOne(max_activation, 1, 99.8, dtype = self.dtype)
            if len(max_activation.shape) == 4:
               padz = (self.pad_width[0] - max_activation.shape[-3])//2
               pady = (self.pad_width[1] - max_activation.shape[-2])//2
               padx = (self.pad_width[2]- max_activation.shape[-1])//2
               
               max_activation_new = np.pad(max_activation, ((0,0),(padz,padz),(pady,pady), (padx,padx)))
               if max_activation_new.shape[1] < self.image.shape[1]:
                   max_activation_new = np.pad(max_activation_new, ((0,0),(0,1),(0,1), (0,1)))
               
            if len(max_activation.shape) == 3:
                pady = (self.pad_width[0] - max_activation.shape[-2])//2
                padx = (self.pad_width[1]- max_activation.shape[-1])//2
                max_activation_new = np.pad(max_activation, ((0,0),(pady,pady), (padx,padx)))
                if max_activation_new.shape[1] < self.image.shape[1]:
                   max_activation_new = np.pad(max_activation_new, ((0,0),(0,1), (0,1)))
            if len(max_activation.shape) == 2:
                pady = (self.pad_width[0] - max_activation.shape[-2])//2
                padx = (self.pad_width[1]- max_activation.shape[-1])//2
                max_activation_new = np.pad(max_activation, ((pady,pady), (padx,padx)))
                if max_activation_new.shape[0] < self.image.shape[0]:
                   max_activation_new = np.pad(max_activation_new, (((0,1), (0,1))))
            max_activation = np.sum(max_activation_new, axis = 0)
            
            self.all_max_activations.append(max_activation)
            
          
        self.all_max_activations = np.array(self.all_max_activations)    
        self.all_max_activations = np.swapaxes(self.all_max_activations, 0,1)
        self.image = np.swapaxes(self.image, 0,1)
        print(self.image.shape, self.all_max_activations.shape)
        self.viewer.add_image(self.all_max_activations, name= 'Activation' + str(count), blending= 'additive', colormap='inferno' )
        self.viewer.add_image(self.image, name= 'Image', blending= 'additive' )
        napari.run()
            
    def VizVollNet(self):
        
        self.smallimage = tf.reshape(self.smallimage, (self.smallimage.shape[0], self.smallimage.shape[2], self.smallimage.shape[3],self.smallimage.shape[4], self.smallimage.shape[1]))
        

def CreateVolume(patch, size_tminus, size_tplus, timepoint):
    starttime = timepoint - int(size_tminus)
    endtime = timepoint + int(size_tplus) + 1
    #TZYX needs to be reshaed to ZYXT
    smallimg = patch[starttime:endtime,]
    return smallimg