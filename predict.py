import os
import h5py

import numpy as np
from PIL import Image

import matplotlib as plt
from matplotlib import cm as CM

from model import CSRNet

import torch
from torchvision import transforms
import random

model = CSRNet()
model.cuda()
checkpoint = torch.load('./model2.pth.tar')
model.load_state_dict(checkpoint['state_dict'])
model.eval()

transform = transforms.Compose([transforms.ToTensor(),transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229,0.224,0.225]),])
def get_prediction(file):
    frame = Image.open(file).convert('RGB') #Get prediction
    width , height = frame.size
    img = transform(frame).unsqueeze(0).cuda()

    # generate count
    density = model(img).data.cpu().numpy()
    prediction = density.sum()
    prediction = int(prediction)
    
    #normalize density
    density_min = np.min(density,axis=tuple(range(density.ndim-1)),keepdims=1)
    density_max = np.max(density,axis=tuple(range(density.ndim-1)),keepdims=1)
    density = (density - density_min) / (density_max - density_min)
    im = Image.fromarray((CM.jet(density.squeeze())*255).astype(np.uint8)) # apply colormap and transparency
    im=im.resize((width,height))
    frame.paste(im, (0, 0), im)
    x=random.randint(1,10000)
    densitymap = 'static/density_map'+str(x)+'.png'
    im.save(densitymap, subsampling=0, quality=100)
    return prediction, densitymap

