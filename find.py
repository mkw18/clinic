# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 13:02:17 2020

@author: SC
"""

import os

path_pdf = "pdf-clinic/"
path_excel = "excel-clinic/"

def getnamelist(path):
    names = []
    for f in os.listdir(path):
        name = f.replace(".xlsx", "").replace(".pdf", "")
        names.append(name)
    return names



pdf = getnamelist(path_pdf)
excel = getnamelist(path_excel)
file = [i for i in pdf if i not in excel]
print(len(file))
print(file)