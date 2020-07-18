from excel_read import getInfo
import jieba
import jieba.posseg as psg
from jieba import analyse
import nltk
import numpy as np
import re

excel_path = r"excel-clinic/"

def SegJieba(InfoGene):
    (name, yxsj, fj, yxzd) = next(InfoGene)
    print(name)
    keywords = get_key(yxsj)
    yxsj_vec = re.split(r'[，。；]+', yxsj)
    # 也可以自定义user-dict
    word_list = jieba.lcut(yxsj)
    freq_dist = nltk.FreqDist(word_list)
    print(freq_dist)
    for i in freq_dist:
        print(i)
    jieba.add_word(word = "两肺", freq = None, tag = 'n')
    jieba.add_word(word = "支气管壁", freq = None, tag = 'n')
    jieba.add_word(word = "左肺", freq = None, tag = 'n')
    clinic_dict = {}
    discrip = ''
    for sent in yxsj_vec:
        print([(x.word,x.flag) for x in psg.lcut(sent)])
    for sent in yxsj_vec:
        for x in psg.lcut(sent):
            if x.word in keywords and x.flag == 'n':
                key = x.word
                discrip = clinic_dict.get(key, "")
            if x.word in keywords and (x.flag == 'a' or x.flag == 'v'):
                discrip = discrip + x.word
        clinic_dict[key] = discrip
        if discrip != "":
            print(key, clinic_dict[key])
                
    
def get_key(text):
    textrank = analyse.textrank
    keywords = textrank(text)
    for keyword in keywords:
        print(keyword, end = '/')
    return keywords
    
if __name__ == "__main__":
    check_file = []
    InfoGene = getInfo(excel_path, check_file)
    SegJieba(InfoGene)
    #get_key(InfoGene)