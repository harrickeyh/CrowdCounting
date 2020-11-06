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
checkpoint = torch.load('./model.pt', map_location='cpu')
model.load_state_dict(checkpoint['state_dict'])
model.eval()

transform = transforms.Compose([transforms.ToTensor()])
def get_prediction(file):
    img = Image.open(file).convert('RGB') #Get prediction
    img = transform(img)
    img = img.unsqueeze(0)

    output = model(img)
    prediction = int(output.detach().cpu().sum().numpy())
    temp = np.asarray(output.detach().cpu().reshape(output.detach().cpu().shape[2],output.detach().cpu().shape[3]))

    norm = temp / temp.max() # normalize 0 to 1
    im = Image.fromarray(np.uint8(CM.jet(norm)*255)) # apply colormap
    if im.mode != 'RGB': # prevent oserror
        im = im.convert('RGB')
    x=random.randint(1,100)
    density = 'static/density_map'+str(x)+'.jpg'
    im.save(density)
    return prediction, density

