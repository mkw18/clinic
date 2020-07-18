# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 19:36:24 2020

@author: SC
"""

import os
import os.path as osp
from matplotlib import pylab as plt
import nibabel as nib
from nibabel import nifti1
from nibabel.viewers import OrthoSlicer3D
from PIL import Image 
import numpy as np 
import nrrd

def leRead(path):
    lesion_data = []
    lesion_options = []
    for f in os.listdir(path):
        nrrd_data, nrrd_options = nrrd.read(osp.join(path, f))
        lesion_data.append(nrrd_data)
        lesion_options.append(nrrd_options)
        """leset = []
        for i in range(nrrd_data.shape[0]):
            for j in range(nrrd_data.shape[1]):
                for k in range(nrrd_data.shape[2]):
                    if nrrd_data[i,j,k] not in leset:
                        leset.append(nrrd_data[i,j,k])
        print(leset)"""
    return lesion_data, lesion_options

def loRead(path):
    lobe = []
    for f in os.listdir(path):
        img = nib.load(osp.join(path, f))
        lo = np.squeeze(img.get_fdata())
        lobe.append(lo)
        """loset = []
        for i in range(lo.shape[0]):
            for j in range(lo.shape[1]):
                for k in range(lo.shape[2]):
                    if lo[i,j,k] not in loset:
                        loset.append(lo[i,j,k])
        print(loset)"""
    return lobe

def SegGenerator(le_path, lo_path):
    lesion_data, lesion_options = leRead(le_path)
    lobe = loRead(lo_path)
    for i in range(len(lobe)):
        yield lesion_data[i], lobe[i]

def findPos(lesion, lobe):
    marked = np.nonzero(lesion)
    mark_lobe = lobe[marked]
    cnt = [0 for i in range(6)]
    for i in mark_lobe:
        cnt[int(i)] += 1
    pos = []
    for i in range(0, 6):
        if cnt[i] > 10:
            pos.append(i)
    return pos

def findDistrib(lesion, lobe):
    marked = np.nonzero(lesion)
    mark_lesion = lesion[marked]
    h = np.max(mark_lesion)
    x = [0 for i in range(h+1)]
    y = [0 for i in range(h+1)]
    z = [0 for i in range(h+1)]
    cnt = [0 for i in range(h+1)]
    for i in mark_lesion:
        cnt[int(i)] += 1
    print("",end = "")
    for i in range(mark_lesion.shape[0]):
        x[int(mark_lesion[i])] += marked[0][i]
        y[int(mark_lesion[i])] += marked[1][i]
        z[int(mark_lesion[i])] += marked[2][i]
    print("",end = "")
    for i in range(h+1):
        if cnt[i] != 0:
            x[i] /= cnt[i]
            y[i] /= cnt[i]
            z[i] /= cnt[i]
    print(x)
    print(y)
    print(z)
    #print(cnt)
    lobe_x = [0, 0]
    lobe_y = [0, 0]
    lobe_z = [0, 0]
    lobe_cnt = [0, 0]
    lobe_marked = np.nonzero(lobe)
    lobe_mark = lobe[lobe_marked]
    for i in lobe_mark:
        if i == 1 or i == 2:
            lobe_cnt[0] += 1
        elif i == 3 or i == 4 or i == 5:
            lobe_cnt[1] += 1
    print("", end = "")
    for i in range(lobe_mark.shape[0]):
        if lobe_mark[i] == 1 or lobe_mark[i] == 2:
            lobe_x[0] += lobe_marked[0][i]
            lobe_y[0] += lobe_marked[1][i]
            lobe_z[0] += lobe_marked[2][i]
        else:
            lobe_x[1] += lobe_marked[0][i]
            lobe_y[1] += lobe_marked[1][i]
            lobe_z[1] += lobe_marked[2][i]
    print("", end = "")
    for i in range(2):
        if lobe_cnt[i] != 0:
            lobe_x[i] /= lobe_cnt[i]
            lobe_y[i] /= lobe_cnt[i]
            lobe_z[i] /= lobe_cnt[i]
    

if __name__ == "__main__":
    le_path = "x/lesion"
    lo_path = "x/lobe"
    lesion_data, lesion_options = leRead(le_path)
    lobe = loRead(lo_path)
    for i in range(len(lobe)):
        findDistrib(lesion_data[i], lobe[i])
    for i in range(len(lobe)):
        pos = findPos(lesion_data[i], lobe[i])
        if 1 in pos:
            print("左上", end = '\t')
        if 2 in pos:
            print("左下", end = '\t')
        if 3 in pos:
            print("右上", end = '\t')
        if 4 in pos:
            print("右中", end = '\t')
        if 5 in pos:
            print("右下", end = '\t')
        print()
    for i in range(len(lobe)):
        pos = findPos(lesion_data[i], lobe[i])
        if 0 in pos:
            print("胸膜附近")
        else:
            print("中央")
        
    """for i in range(lesion_data[0].shape[0]):
        for j in range(lesion_data[0].shape[1]):
            print(lesion_data[0][i,j,143], end = " ")
        print()"""
    """leset = []
    for i in range(lesion_data[0].shape[0]):
        for j in range(lesion_data[0].shape[1]):
            for k in range(lesion_data[0].shape[2]):
                if lesion_data[0][i,j,k] not in leset:
                    leset.append(lesion_data[0][i,j,k])
    print(leset)"""
    """for i in range(lobe[0].shape[0]):
        for j in range(lobe[0].shape[1]):
            print(lobe[0][i,j,143], end = " ")
        print()"""
    """loset = []
    for i in range(lobe[0].shape[0]):
        for j in range(lobe[0].shape[1]):
            for k in range(lobe[0].shape[2]):
                if lobe[0][i,j,k] not in loset:
                    loset.append(lobe[0][i,j,k])
    print(loset)"""
    #print(list(set(np.array(lobe[0]))))
    #plt.imshow(lobe[4][:,256,:])
    #plt.show
    #for i in range(lesion_data[0].shape[2]):
        #img = Image.fromarray(lesion_data[0][:,:,i])
        #img.show()
        #plt.imshow(lesion_data[0][:,:,i])
        #plt.show()
        #print(i)
    #SegGene = SegGenerator(le_path, lo_path)
    #for (lesion, lobe) in SegGene:
        #print(type(lesion), type(lobe))
        #print(lesion.shape, lobe.shape)