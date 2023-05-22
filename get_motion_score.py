#/home/cqintern08/.python3.7.9/bin/python3.7
import datetime
import re
import time
import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import pickle
import threading
import joblib
import pandas as pd
import jiagu
#sns.set_style('darkgrid')

"""
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ hanlp -U
export PATH=/home/cqintern08/.python3.7.9/bin:$PATH
export PythonPATH=/home/cqintern08/.python3.7.9/bin:$PythonPATH
alias python=/home/cqintern08/.python3.7.9

ps u    check process id which grouped by user

Running:
cd /home/cqintern08/AbsoluteX_intern/Absolute_Alpha/
nohup /home/cqintern08/.python3.7.9/bin/python3.7 /home/cqintern08/AbsoluteX_intern/Absolute_Alpha/get_motion_score.py&
"""

# define your hyper-parameter here
data_path = '/dat/cqdata/socialmedia/eastmoney/guba/daily/'
file_list = os.listdir(data_path)
txt_file_list = list()
already_get = list()
temp = os.listdir('/home/cqintern08/AbsoluteX_intern/Absolute_Alpha/motion_scores/')
for j in temp:
    already_get.append(j[-12:-4])
for i in file_list:
    if len(i)==8:
        if int(i[:4])>=2019:
            if int(i[:4])<2021:
                if i in already_get:
                    continue
                txt_file_list.append(i)
print("process file num is:",len(txt_file_list))
txt_file_list.sort()
print(txt_file_list[:10])

def get_opinion_df(file_path):
    content = list()
    with open(file_path,"r",encoding="utf-8") as f:
        for lines in f.readlines():
            content.append(lines[:-1].split('|'))
    sentense = list()
    original_content = list()
    for i in content:
        if len(i)==6:
            sentense.append(i[-1])
            original_content.append(i)
        if len(i)>6:
            concat_sen = ''
            for j in i[5:]:
                concat_sen = concat_sen+ str(j)
            sentense.append(j)
            original_content.append(i)

    last_change = list()
    build_day = list()
    up_opinion = list()
    comments_num = list()
    stock_code = list()
    user_id = list()
    for i in original_content:
        try:
            last_change.append(i[0])
            build_day.append(i[1])
            up_opinion.append(i[2])
            comments_num.append(i[3])
            stock_code.append((i[4].split(','))[0])
            user_id.append((i[4].split(','))[1])
        except:
            sentense.pop(original_content.index(i))

    pos_sentense_day = dict()
    pos_sentense_day['last_change'] = last_change
    pos_sentense_day['stock_code'] = stock_code
    pos_sentense_day['sentense'] = sentense
    return pd.DataFrame(pos_sentense_day)

for target_file in tqdm(txt_file_list):
    opinion_df = get_opinion_df(data_path+target_file)
    def gen03(x):
        import jiagu
        result = jiagu.sentiment(x)
        if result[0]=='negative':
            return 1-result[1]
        else:
            return result[1]
    opinion_df['score03'] = opinion_df.sentense.astype(str).apply(lambda x: gen03(x))
    opinion_df.to_csv('/home/cqintern08/AbsoluteX_intern/Absolute_Alpha/motion_scores/motion_score'+target_file+'.csv',
                    index=False,
                    encoding='utf_8_sig')