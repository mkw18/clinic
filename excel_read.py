# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 08:16:20 2020

@author: SC
"""

import os
import os.path as osp
import xlrd
from string import digits
import warnings

excel_path = r"excel-clinic/"

def getInfo(path, check_file):
    for f in os.listdir(path):
        file_path = osp.join(path, f)
        remove_digits = str.maketrans('', '', digits)
        name = f.translate(remove_digits).replace(".xlsx", "")
        workbook = xlrd.open_workbook(file_path)
        #print(workbook.sheet_names())
        table1 = workbook.sheet_by_name('Table 1')
        nrows = table1.nrows
        ncols = table1.ncols
        #print(nrows, ncols)
        #print(name)
        yxsj = ""
        fj = ""
        yxzd = ""
        find = False
        for r in range(nrows):
            for c in range(ncols):
                cell1 = table1.cell(r,c).value.replace(" ", "")
                if "影像所见" in cell1:
                    find = True
                    break
            if find:
                break
        if find:
            yxsj = cell1.replace("影像所见:", "")
            for j in range(100):
                r = r + 1
                cell2 = table1.cell(r,c).value.replace(" ", "").replace("\n", "")
                if "附见" in cell2 or "影像诊断" in cell2 or r == nrows - 2:
                    break
                yxsj = yxsj + cell2
            #print(yxsj)
            if "附见" in cell2:
                fj = cell2.replace("附见：", "").replace("附见；", "").replace("附见", "")
                for j in range(100):
                    r = r + 1
                    cell3 = table1.cell(r,c).value.replace(" ","")
                    if "影像诊断" in cell3 or r == nrows - 2:
                        break
                    fj = fj + cell3.replace("\n","")
                #print(fj)
                if "影像诊断" in cell3:
                    yxzd = cell3.replace("影像诊断:","")
                    for j in range(100):
                        r = r + 1
                        cell4 = table1.cell(r,c).value.replace(" ", "")#.replace("\n", "")
                        if cell4 == "" or r == nrows - 2:
                            break
                        yxzd = yxzd + cell4
                    #print(yxzd)
                else:
                    warnings.warn(name + " does not have 影像诊断", RuntimeWarning)
            elif "影像诊断" in cell2:
                warnings.warn(name + " does not have 附见", RuntimeWarning)
                yxzd = cell2.replace("影像诊断:","")
                for j in range(100):
                    r = r + 1
                    cell3 = table1.cell(r,c).value.replace(" ","")#.replace("\n","")
                    if cell3 == "" or r == nrows - 2:
                        break
                    yxzd = yxzd + cell3
                #print(yxzd)
            else:
                warnings.warn(name + " does not have 附见 and 影像诊断", RuntimeWarning)
        else:
            check_file.append(file_path)
            warnings.warn(name + " can not find 影像所见, please check the file", RuntimeWarning)
        yield name, yxsj, fj, yxzd
    
    
if __name__ == "__main__":
    check_file = []
    InfoGene = getInfo(excel_path, check_file)
    print(check_file)
    for (name, yxsj, fj, yxzd) in InfoGene:
        print(name)
        print(yxsj)
        print(fj)
        print(yxzd)