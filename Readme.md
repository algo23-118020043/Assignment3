# MFE5210 Assigment3
任务详情描述：
+ 这是我的5210第3次作业
+ 尝试复现情绪因子

---------------------
## 详细描述

因子idea：
我将该项目的因子分为三类因子：词频因子、认知因子、情感分数因子
词频因子完全基于每一句话中，各个词性出现的频率进行生成，选取的代表为词性N，因子表现见下文
认知因子主要由发帖的数量等信息组成，选取的逻辑为，股民关注越多的股票帖子越多，选取的代表为word_num_total，因子表现见下文
情感分数因子是每一句话的情感打分，表现见下文

建议查看顺序
1. README.txt
2. sentense_character.py
3. POF_factor_csv_generate.ipynb
其它代码辅以中间查看

代码主要由五份文件组成，基于pysim5进行回测

1. AbsoluteX_new/Public_Opinion_Factor/sentense_character.py
用于对股吧txt文件进行处理，必须预先运行并且耗时较长，会生成新的pkl变量用于进一步处理

2. AbsoluteX_new/Public_Opinion_Factor/gen_freq_csv.py
用于处理生成的pkl变量并且进一步整合出词频信息，详情可见POF_factor_csv_generate.ipynb

3. AbsoluteX_new/Public_Opinion_Factor/get_motion_score.py
用于处理生成每一句舆情的分数，进一步在POF_factor_csv_generate.ipynb中处理

4. AbsoluteX_new/Public_Opinion_Factor/POF_factor_csv_generate.ipynb
包含从生成1中的freq后，直到生成factor_value的csv导入pysim回测的所有代码，notebook本身就是详细的instruction

5. /home/cqintern08/AbsoluteX_new/pysim5/config_test_match.xml  &  /home/cqintern08/AbsoluteX_new/pysim5/examples/try_match.py
包含在pysim中回测的自定义文件
其中主要自定义内容在try_match.py文件之中。
更改 code line 50 中的文件名可以更改调用的factor value csv文件
同时更改 code line 96 中的负号可以更改回测结果IR的正负（详情见下文）


上传的数据主要由 部分组成，主要作用是方便查看者的复现，作用如下
1./home/cqintern08/AbsoluteX_new/Public_Opinion_Factor/factorvalue
主要存储导出的 factor value csv文件，方便使用pysim回测并且调参

2./home/cqintern08/AbsoluteX_new/Public_Opinion_Factor/pnl_POF
主要用于生成的pnl文件，同样方便回测

另外数据为减少程序运行崩溃风险产生的辅助中间文件，POF_factor_csv_generate.ipynb中有详细的描述