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
#sns.set_style('darkgrid')

"""
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ hanlp -U
export PATH=/home/cqintern08/.python3.7.9/bin:$PATH
export PythonPATH=/home/cqintern08/.python3.7.9/bin:$PythonPATH
alias python=/home/cqintern08/.python3.7.9

ps u    check process id which grouped by user

Running:
cd /home/cqintern08/AbsoluteX_intern/Absolute_Alpha/
nohup /home/cqintern08/.python3.7.9/bin/python3.7 /home/cqintern08/AbsoluteX_intern/Absolute_Alpha/sentense_character.py&
"""

import hanlp
# MTL多任务，具体任务见模型名称，语种见名称最后一个字段或相应语料库

hanlp.pretrained.mtl.ALL
#调用hanlp.load进行加载，模型会自动下载到本地缓存。自然语言处理分为许多任务，分词只是最初级的一个。
#与其每个任务单独创建一个模型，不如利用HanLP的联合模型一次性完成多个任务：
HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)

# define your hyper-parameter here
data_path = '/dat/cqdata/socialmedia/eastmoney/guba/daily/'
file_list = os.listdir(data_path)
txt_file_list = list()
already_get = list()
temp = os.listdir('/home/cqintern08/AbsoluteX_intern/Absolute_Alpha/obj/')
for j in temp:
    already_get.append(j[-12:-4])
for i in file_list:
    if len(i)==8:
        if int(i[:4])>=2017:
            if i in already_get:
                continue
            txt_file_list.append(i)
print("process file num is:",len(txt_file_list))
txt_file_list.sort()
print(txt_file_list[:10])

def gen_character(txt_file_list,HanLP):
    for txt_name in tqdm(txt_file_list):
        file_path = data_path+str(txt_name)
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
        pos_sentense_day = HanLP(sentense, tasks='pos*')

        pos_sentense_day['last_change'] = last_change
        pos_sentense_day['build_day'] = build_day 
        pos_sentense_day['up_opinion'] = up_opinion
        pos_sentense_day['comments_num'] = comments_num
        pos_sentense_day['stock_code'] = stock_code
        pos_sentense_day['user_id'] = user_id

        joblib.dump(pos_sentense_day,"obj/pos_sentense_day"+txt_name+".pkl")
    return

"""
vehicles = []       # 新建车辆组
for num in range(4):
    text_list = txt_file_list[num*40:(num+1)*40]
    vehicle = threading.Thread(target=gen_character, args=(text_list,HanLP)) # 新建车辆
    vehicles.append(vehicle)     # 添加车辆到车辆组中

for vehicle in vehicles:
    vehicle.start()  # 分别启动车辆

for vehicle in vehicles:
    vehicle.join()      # 分别检查到站车辆
"""
gen_character(txt_file_list,HanLP)
print('/*----- mission successed -----*/')


"""
@inproceedings{he-choi-2021-stem,
    title = "The Stem Cell Hypothesis: Dilemma behind Multi-Task Learning with Transformer Encoders",
    author = "He, Han and Choi, Jinho D.",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2021",
    address = "Online and Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-main.451",
    pages = "5555--5577",
    abstract = "Multi-task learning with transformer encoders (MTL) has emerged as a powerful technique 
                to improve performance on closely-related tasks for both accuracy and efficiency while a question 
                still remains whether or not it would perform as well on tasks that are distinct in nature. 
                We first present MTL results on five NLP tasks, POS, NER, DEP, CON, and SRL, 
                and depict its deficiency over single-task learning. We then conduct an extensive pruning analysis 
                to show that a certain set of attention heads get claimed by most tasks during MTL, who interfere 
                with one another to fine-tune those heads for their own objectives. Based on this finding, 
                we propose the Stem Cell Hypothesis to reveal the existence of attention heads naturally talented 
                for many tasks that cannot be jointly trained to create adequate embeddings for all of those tasks. 
                Finally, we design novel parameter-free probes to justify our hypothesis and demonstrate 
                how attention heads are transformed across the five tasks during MTL through label analysis.",
}
"""