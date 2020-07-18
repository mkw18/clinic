# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 08:17:10 2020

@author: SC
"""

import re
import numpy as np

filename = 'txt-clinic/554630郁小英.txt'
f = open(filename)
name = f.readline()
name = name.replace(" ", "")
while True:
    l = f.readline()
    if not l:
        break
    if '影像所见' in l:
        yxsj = l.replace(" ", "").replace("影像所见:", "")
        yxsj_vec = yxsj.split("。")
        if yxsj_vec[-1] == '\n' or yxsj_vec[-1] == ' ':
            del(yxsj_vec[-1])
        print(yxsj_vec)
    elif '附见' in l:
        fj = l.replace(" ", "").replace("附见：", "")
        fj_vec = fj.split("。")
        if fj_vec[-1] == '\n' or fj_vec[-1] == ' ':
            del(fj_vec[-1])
        print(fj_vec)
    elif '影像诊断' in l:
        yxzd = l.replace(" ", "").replace("影像诊断:", "")
        yxzd_vec = re.split(r'[。；]+', yxzd)
        if yxzd_vec[-1] == '\n' or yxzd_vec[-1] == ' ' or yxzd_vec[-1] == '':
            del(yxzd_vec[-1])
        print(yxzd_vec)
#yxsj = f.readline()
#yxsj = yxsj.replace(" ", "")
#print(yxsj)
#yxsj_vec = yxsj.split("。")
#print(yxsj_vec)