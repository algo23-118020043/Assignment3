import datetime
import re
import time
import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import pickle
import joblib
import sys

"""
/home/cqintern08/.python3.7.9/bin/python3.7 /home/cqintern08/AbsoluteX_intern/Absolute_Alpha/gen_freq_csv.py
"""


path = '/home/cqintern08/AbsoluteX_intern/Absolute_Alpha/'
file_list = os.listdir(path+'obj/')
file_list.sort()

data_list = list()
already_get = list()
temp = os.listdir('/home/cqintern08/AbsoluteX_intern/Absolute_Alpha/freq_csv/')
for j in temp:
    already_get.append(int(j[-12:-4]))
for i in file_list:
    if int(i[-12:-4]) in already_get:
        continue
    data_list.append(i)
data_list.sort()
print(data_list[:10])

for data_name in tqdm(data_list):
    pos_sentense_day=joblib.load(path+'obj/'+data_name)
    data_date = int(data_name[-12:-4])

    #读取并且检查数据是否对齐，如果完全对齐则表示是一一对应的关系
    #如果数据没有对齐，会立刻退出运行程序
    dict_names = ['tok/fine','pos/ctb','pos/pku','pos/863','last_change',
                'build_day','up_opinion','comments_num','stock_code','user_id']
    dict_len = len(pos_sentense_day['tok/fine'])
    for dict_name in dict_names:
        if dict_len != len(pos_sentense_day[dict_name]):
            print('/*----- exist data not aligned!!!!! -----*/')
            sys.exit()

    """
    #根据每天的舆情数据创建pandas表单，生成词性频率表单
    #这里采用pku标准，并主观删除了部分可能没有作用的词性，对应词性如下所示
    A：形容词
    D：副词
    E：叹词
    M：数词
    N：名词
    V：动词
    Y：语气词
    """
    pos_sentense_day['word_num_total'] = np.zeros(dict_len)
    word_tags = ['A','D','E','I','M','N','V','Y']
    for word_tag in word_tags:
        pos_sentense_day[word_tag] = np.zeros(dict_len)
    #开始逐行统计出现词性的次数
    for i in range(dict_len):
        pos_list = pos_sentense_day['pos/pku'][i]
        pos_sentense_day['word_num_total'][i] = len(pos_list)
        for tag in pos_list:
            if tag[0].upper() in word_tags:
                pos_sentense_day[tag[0].upper()][i] = pos_sentense_day[tag[0].upper()][i]+1

    freq_table = pd.DataFrame(pos_sentense_day).drop(['tok/fine','pos/ctb','pos/pku','pos/863'],axis=1)
    freq_table['word_num_selected'] = freq_table[['A','D','E','I','M','N','V','Y']].sum(axis=1)
    freq_table.to_csv(path+'freq_csv/'+'freq'+str(data_date)+'.csv',index=False)
    

