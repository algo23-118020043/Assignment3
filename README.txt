###############
### READ ME ###
###############

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


###############
### command ###
###############

cp -f /home/cqintern08/AbsoluteX_new/pysim5/pnl/Alpha_POF /dropbox/cqintern08/checkcorr/Alpha_POF_D
rm -f /home/cqintern08/AbsoluteX_new/pysim5/pnl/Alpha_POF

/dat/pysimrelease/pysim-4.0.0/tools/niub_2004 /dropbox/cqintern08/checkcorr/Alpha_POF_D

/dat/pysimrelease/pysim-4.0.0/tools/multibcorr Alpha_POF_word_num_total Alpha_POF_N 2 2
/dat/pysimrelease/pysim-4.0.0/tools/multibcorr Alpha_POF_word_num_total Alpha_POF_motion_score 2 2
/dat/pysimrelease/pysim-4.0.0/tools/multibcorr Alpha_POF_N Alpha_POF_motion_score 2 2


######################
### factor outcome ###
######################

简单测试过加入OpTradeConstraint，对IR影响不大，下降0.04-0.02
以下是回测细节，详情请见 config_test_match
<Op mId="OpDecay" days="10"/>
<Op mId="OpPow" exp="1" dense="false"/>
<Op mId="OpGroupNeutFast" group="WindIndustry.sw1"/>

注：若是出现回测IR为负的情况，请更改 try_math.py 文件中的
self.alpha[:] = di_values_ii[str(date_temp)][0:uv.instsz]  为
self.alpha[:] = - di_values_ii[str(date_temp)][0:uv.instsz] 反之同理

finally give 3 factors and mutlibcorr as under
freq factor N
cognition factor word_num_total
motion score factor

+0.2233    Alpha_POF_N  word_num_total
+0.0198 Alpha_POF_motion_score  word_num_total
+0.3949 Alpha_POF_motion_score  Alpha_POF_N


详细回测结果

/*----- freq factor A -----*/
            dates   long   short   pnl(M)    %ret    %tvr     shrp (IR)    %dd   %win margin  fitsc   lnum   snum tdays tratio
20170109-20171229  10.00  -10.00    0.088    0.91   36.27   0.33( 0.02)   3.62   0.52   0.51   0.05  583.4  584.7   240   1.00
20180102-20181228  10.00  -10.00    1.107   11.48   38.55   3.92( 0.25)   1.54   0.60   5.96   2.14  598.2  595.1   241   0.99
20190102-20191231  10.00  -10.00    1.084   11.11   38.09   3.98( 0.25)   1.11   0.56   5.83   2.15  606.7  603.2   244   1.00
20200102-20201127  10.00  -10.00    0.310    3.53   48.95   0.50( 0.03)   4.21   0.50   1.44   0.13  490.1  487.6   219   1.00

20170109-20201127  10.00  -10.00    2.588    6.85   40.27   1.63( 0.10)   4.21   0.55   3.41   0.67  571.6  569.6   944   1.00
-0.2263 3745_interval
-0.2253 4900_interval
-0.2029 3747_interval
-0.1962 3611_interval
-0.1946 241_price_volume
-0.1943 2592_interval
-0.1941 360_price_volume
-0.1904 7719_price_volume
-0.1894 5207_ml
-0.1865 3737_interval
-0.1823 3694_interval
+0.2797 1728_interval
+0.2806 83_price_volume
+0.2832 155_price_volume
+0.2835 902_interval
+0.2858 154_price_volume
+0.2860 62_price_volume
+0.2998 296_price_volume
+0.3012 301_price_volume
+0.3025 1810_flow
+0.3077 1212_interval
----------------------------------------------
+1.8136 816_flow
+1.8311 813_flow
+1.8344 1810_flow
+1.8564 817_flow
+1.8789 1541_price_volume
+1.8795 798_ga-price_volume
+1.9028 792_ga-price_volume
+1.9505 2601_ga-price_volume
+2.0115 2215_interval
+2.0522 2599_ga-price_volume


/*----- freq factor D -----*/
            dates   long   short   pnl(M)    %ret    %tvr     shrp (IR)    %dd   %win margin  fitsc   lnum   snum tdays tratio
20170109-20171229  10.00  -10.00    2.893   30.13   39.50   4.32( 0.27)   1.82   0.57  15.32   3.77  586.3  576.5   240   1.00
20180102-20181228  10.00  -10.00    2.262   23.46   42.49   3.41( 0.22)   3.10   0.59  11.04   2.54  606.1  583.4   241   0.99
20190102-20191231  10.00  -10.00    2.229   22.83   42.04   3.65( 0.23)   4.71   0.58  10.86   2.69  611.0  592.2   244   1.00
20200102-20201127  10.00  -10.00    3.200   36.54   54.20   4.15( 0.26)   4.25   0.60  13.48   3.41  492.9  475.1   219   1.00

20170109-20201127  10.00  -10.00   10.583   28.03   44.34   3.87( 0.24)   4.71   0.58  12.66   3.08  576.1  558.8   944   1.00
-0.6311 141_price_volume
-0.6023 45_price_volume
-0.5574 887_interval
-0.5376 618_interval
-0.5191 139_price_volume
-0.5097 364_price_volume
-0.5000 44_price_volume
-0.5000 46_price_volume
-0.4915 899_interval
-0.4804 134_price_volume
-0.4760 246_price_volume
+0.5227 154_price_volume
+0.5235 4650_interval
+0.5245 4445_fundamental
+0.5256 358_interval
+0.5359 665_flow
+0.5384 1804_event
+0.5491 1722_price_volume
+0.5549 1720_price_volume
+0.5587 2702_ga-price_volume
+0.5869 2706_ga-price_volume
----------------------------------------------
+1.0693 3176_interval
+1.1556 832_ga-price_volume
+1.1755 2719_ga-price_volume
+1.2151 1131_event
+1.2152 3129_ga-price_volume
+1.2452 2702_ga-price_volume
+1.2620 3261_interval
+1.3125 2603_ga-price_volume
+1.3408 2706_ga-price_volume
+1.3742 3133_ga-price_volume


/*----- freq factor E -----*/
            dates   long   short   pnl(M)    %ret    %tvr     shrp (IR)    %dd   %win margin  fitsc   lnum   snum tdays tratio
20170109-20171229  10.00  -10.00    1.738   18.11   40.68   3.85( 0.24)   1.45   0.60   8.94   2.57  589.1  573.6   240   1.00
20180102-20181228  10.00  -10.00    1.400   14.52   41.68   3.38( 0.21)   1.51   0.57   6.97   2.00  600.1  589.2   241   0.99
20190102-20191231  10.00  -10.00    1.425   14.60   40.67   3.79( 0.24)   1.68   0.58   7.18   2.27  609.1  594.1   244   1.00
20200102-20201127  10.00  -10.00    0.910   10.39   56.20   1.26( 0.08)   7.60   0.57   3.70   0.54  491.5  477.5   219   1.00

20170109-20201127  10.00  -10.00    5.473   14.49   44.54   2.65( 0.17)   7.60   0.58   6.52   1.51  574.4  560.6   944   1.00
-0.4045 364_price_volume
-0.4018 360_price_volume
-0.3954 141_price_volume
-0.3745 618_interval
-0.3739 887_interval
-0.3417 134_price_volume
-0.3240 45_price_volume
-0.3141 580_interval
-0.2948 637_price_volume
-0.2927 246_price_volume
-0.2893 137_price_volume
+0.3699 1727_interval
+0.3850 1733_price_volume
+0.3910 2159_interval
+0.3922 665_flow
+0.4046 1859_fundamental
+0.4311 1722_price_volume
+0.4478 154_price_volume
+0.4518 2706_ga-price_volume
+0.4570 1720_price_volume
+0.4806 2702_ga-price_volume
----------------------------------------------
+1.3018 1229_flow
+1.3095 815_flow
+1.3337 3176_interval
+1.3824 832_ga-price_volume
+1.4040 2599_ga-price_volume
+1.4472 3261_interval
+1.4879 2706_ga-price_volume
+1.5443 2702_ga-price_volume
+1.6290 2603_ga-price_volume
+1.6955 3133_ga-price_volume


/*----- freq factor I -----*/
            dates   long   short   pnl(M)    %ret    %tvr     shrp (IR)    %dd   %win margin  fitsc   lnum   snum tdays tratio
20170109-20171229  10.00  -10.00   -0.081   -0.85   45.87  -0.21(-0.01)   6.94   0.53  -0.37  -0.03  580.6  582.2   240   1.00
20180102-20181228  10.00  -10.00    0.475    4.93   43.86   1.53( 0.10)   5.75   0.51   2.25   0.51  603.1  586.3   241   0.99
20190102-20191231  10.00  -10.00    0.072    0.74   42.63   0.25( 0.02)   3.05   0.47   0.35   0.03  614.6  588.5   244   1.00
20200102-20201127  10.00  -10.00    0.821    9.37   59.09   1.08( 0.07)   4.11   0.51   3.17   0.43  499.0  469.6   219   1.00

20170109-20201127  10.00  -10.00    1.287    3.41   47.59   0.66( 0.04)   6.94   0.51   1.43   0.18  576.2  558.8   944   1.00


/*----- freq factor M -----*/
            dates   long   short   pnl(M)    %ret    %tvr     shrp (IR)    %dd   %win margin  fitsc   lnum   snum tdays tratio
20170109-20171229  10.00  -10.00    1.510   15.73   30.22   3.85( 0.24)   2.80   0.62  10.45   2.78  584.6  583.5   240   1.00
20180102-20181228  10.00  -10.00    2.199   22.81   32.70   4.08( 0.26)   2.60   0.59  13.95   3.41  596.2  597.1   241   0.99
20190102-20191231  10.00  -10.00    2.025   20.75   31.83   4.09( 0.26)   2.69   0.56  13.04   3.30  605.9  604.1   244   1.00
20200102-20201127  10.00  -10.00    2.275   25.97   39.94   2.56( 0.16)   3.79   0.54  13.01   2.07  486.7  491.3   219   1.00

20170109-20201127  10.00  -10.00    8.009   21.21   33.53   3.25( 0.21)   3.79   0.58  12.67   2.58  570.4  570.9   944   1.00
-0.4416 141_price_volume
-0.3720 45_price_volume
-0.3714 364_price_volume
-0.3707 354_interval
-0.3649 887_interval
-0.3636 1145_socialmedia
-0.3529 360_price_volume
-0.3478 899_interval
-0.3306 241_price_volume
-0.3257 2471_interval
-0.3225 618_interval
+0.4647 2809_ga-price_volume
+0.4650 2003_interval
+0.4747 4650_interval
+0.4925 1720_price_volume
+0.4958 1804_event
+0.4963 154_price_volume
+0.4970 1859_fundamental
+0.4984 2706_ga-price_volume
+0.5135 2702_ga-price_volume
+0.5345 1722_price_volume
----------------------------------------------
+1.4443 792_ga-price_volume
+1.4448 2702_ga-price_volume
+1.4677 817_flow
+1.4702 818_flow
+1.4777 1229_flow
+1.4896 2599_ga-price_volume
+1.5023 2603_ga-price_volume
+1.5562 3133_ga-price_volume
+1.5563 832_ga-price_volume
+1.5588 1541_price_volume


/*----- freq factor N -----*/
            dates   long   short   pnl(M)    %ret    %tvr     shrp (IR)    %dd   %win margin  fitsc   lnum   snum tdays tratio
20170109-20171229  10.00  -10.00    3.579   37.28   24.35   4.88( 0.31)   2.42   0.61  30.75   6.03  587.9  580.2   240   1.00
20180102-20181228  10.00  -10.00    2.331   24.18   28.22   4.23( 0.27)   1.66   0.57  17.14   3.91  597.6  595.8   241   0.99
20190102-20191231  10.00  -10.00    3.214   32.94   25.10   5.85( 0.37)   3.13   0.66  26.24   6.70  604.5  605.5   244   1.00
20200102-20201127  10.00  -10.00    2.307   26.33   35.47   3.28( 0.21)   2.82   0.61  14.85   2.82  487.0  491.0   219   1.00

20170109-20201127  10.00  -10.00   11.431   30.27   28.11   4.45( 0.28)   3.13   0.61  21.56   4.61  571.3  570.0   944   1.00
-0.5546 141_price_volume
-0.5370 618_interval
-0.5130 364_price_volume
-0.5117 360_price_volume
-0.5110 887_interval
-0.5068 45_price_volume
-0.4961 580_interval
-0.4857 139_price_volume
-0.4810 134_price_volume
-0.4723 44_price_volume
-0.4723 46_price_volume
+0.4504 1859_fundamental
+0.4663 1722_price_volume
+0.4666 4715_interval
+0.4774 5499_fundamental
+0.4870 358_interval
+0.4910 665_flow
+0.5165 1720_price_volume
+0.5258 2702_ga-price_volume
+0.5267 2706_ga-price_volume
+0.5521 154_price_volume
----------------------------------------------
+0.8765 2719_ga-price_volume
+0.9094 3129_ga-price_volume
+0.9202 7038_ga-price_volume
+0.9618 832_ga-price_volume
+1.0290 2603_ga-price_volume
+1.0312 3176_interval
+1.0811 2702_ga-price_volume
+1.1098 2706_ga-price_volume
+1.1114 3261_interval
+1.1675 3133_ga-price_volume


/*----- freq factor V -----*/
            dates   long   short   pnl(M)    %ret    %tvr     shrp (IR)    %dd   %win margin  fitsc   lnum   snum tdays tratio
20170109-20171229  10.00  -10.00    2.368   24.67   29.99   4.62( 0.29)   1.87   0.64  16.52   4.19  585.1  583.1   240   1.00
20180102-20181228  10.00  -10.00    2.071   21.48   33.26   3.85( 0.24)   2.30   0.56  12.92   3.09  597.1  596.2   241   0.99
20190102-20191231  10.00  -10.00    2.420   24.80   31.20   4.40( 0.28)   4.26   0.57  15.90   3.92  604.9  605.0   244   1.00
20200102-20201127  10.00  -10.00    1.784   20.36   40.27   2.25( 0.14)   3.97   0.60  10.11   1.60  490.6  487.1   219   1.00

20170109-20201127  10.00  -10.00    8.644   22.89   33.53   3.52( 0.22)   4.26   0.59  13.67   2.91  571.4  569.9   944   1.00
-0.4974 141_price_volume
-0.4942 360_price_volume
-0.4924 364_price_volume
-0.4621 618_interval
-0.4590 887_interval
-0.4429 3745_interval
-0.4231 580_interval
-0.4193 45_price_volume
-0.4157 134_price_volume
-0.3855 139_price_volume
-0.3732 246_price_volume
+0.4585 5530_event
+0.4631 5499_fundamental
+0.4910 2159_interval
+0.5139 665_flow
+0.5188 2706_ga-price_volume
+0.5218 1722_price_volume
+0.5305 1720_price_volume
+0.5320 1859_fundamental
+0.5563 2702_ga-price_volume
+0.5930 154_price_volume
----------------------------------------------
+1.2372 2599_ga-price_volume
+1.2529 1541_price_volume
+1.2555 3176_interval
+1.2804 1131_event
+1.3140 832_ga-price_volume
+1.3454 2603_ga-price_volume
+1.3598 3261_interval
+1.3808 2706_ga-price_volume
+1.4445 2702_ga-price_volume
+1.5870 3133_ga-price_volume


/*----- freq factor Y -----*/
            dates   long   short   pnl(M)    %ret    %tvr     shrp (IR)    %dd   %win margin  fitsc   lnum   snum tdays tratio
20170109-20171229  10.00  -10.00    3.503   36.49   30.19   5.09( 0.32)   1.71   0.62  24.28   5.60  584.6  583.6   240   1.00
20180102-20181228  10.00  -10.00    1.955   20.28   34.37   3.50( 0.22)   2.62   0.54  11.80   2.69  596.8  596.5   241   0.99
20190102-20191231  10.00  -10.00    3.042   31.17   32.21   5.22( 0.33)   3.13   0.64  19.36   5.14  607.5  602.5   244   1.00
20200102-20201127  10.00  -10.00    1.448   16.53   41.37   2.09( 0.13)   5.03   0.58   7.99   1.32  491.2  486.6   219   1.00

20170109-20201127  10.00  -10.00    9.949   26.35   34.38   3.91( 0.25)   5.03   0.60  15.35   3.42  571.9  569.3   944   1.00
-0.5677 141_price_volume
-0.5433 360_price_volume
-0.5392 364_price_volume
-0.5361 618_interval
-0.5280 887_interval
-0.5209 45_price_volume
-0.4940 134_price_volume
-0.4938 580_interval
-0.4662 139_price_volume
-0.4571 44_price_volume
-0.4571 46_price_volume
+0.4991 2159_interval
+0.5088 1859_fundamental
+0.5186 5499_fundamental
+0.5205 358_interval
+0.5291 1722_price_volume
+0.5554 665_flow
+0.5681 1720_price_volume
+0.5724 2706_ga-price_volume
+0.5900 2702_ga-price_volume
+0.6043 154_price_volume
----------------------------------------------
+1.0988 1229_flow
+1.1164 2719_ga-price_volume
+1.1409 7038_ga-price_volume
+1.1920 3176_interval
+1.3116 832_ga-price_volume
+1.3232 3261_interval
+1.3480 2603_ga-price_volume
+1.3716 2706_ga-price_volume
+1.3795 2702_ga-price_volume
+1.4783 3133_ga-price_volume


/*----- cognition factor user_id -----*/
            dates   long   short   pnl(M)    %ret    %tvr     shrp (IR)    %dd   %win margin  fitsc   lnum   snum tdays tratio
20170109-20171229  10.00  -10.00    1.008   10.50   14.60   1.63( 0.10)   8.17   0.59  14.44   1.38  589.4  578.8   240   1.00
20180102-20181228  10.00  -10.00    3.350   34.75   16.00   6.13( 0.39)   2.78   0.64  43.44   9.03  604.2  589.1   241   0.99
20190102-20191231  10.00  -10.00    3.982   40.79   12.37   6.29( 0.40)   5.85   0.66  65.93  11.41  605.6  604.3   244   1.00
20200102-20201127  10.00  -10.00    3.136   35.80   24.34   3.77( 0.24)   3.13   0.61  29.42   4.57  486.5  491.5   219   1.00

20170109-20201127  10.00  -10.00   11.475   30.39   16.64   4.26( 0.27)   8.17   0.63  36.56   5.76  573.5  567.8   944   1.00
-0.3219 1966_price_volume
-0.3066 1055_event
-0.2732 1818_flow
-0.2653 274_price_volume
-0.2538 364_price_volume
-0.2465 1914_price_volume
-0.2458 354_interval
-0.2432 1231_interval
-0.2410 1704_interval
-0.2386 235_price_volume
-0.2375 4782_interval
+0.5149 1227_flow
+0.5198 1032_interval
+0.5324 1228_flow
+0.5355 1023_interval
+0.5411 1048_interval
+0.5513 2727_ga-price_volume
+0.5634 2704_ga-price_volume
+0.5683 1225_interval
+0.5700 917_interval
+0.5845 2131_news
----------------------------------------------
+1.2952 2599_ga-price_volume
+1.3027 2727_ga-price_volume
+1.3524 819_flow
+1.3641 1230_flow
+1.3934 1227_flow
+1.3944 813_flow
+1.3946 1229_flow
+1.4222 818_flow
+1.5706 1541_price_volume
+1.5948 2215_interval


/*----- cognition factor word_num_total -----*/
            dates   long   short   pnl(M)    %ret    %tvr     shrp (IR)    %dd   %win margin  fitsc   lnum   snum tdays tratio
20170109-20171229  10.00  -10.00    1.264   13.16   17.17   1.84( 0.12)   9.12   0.57  15.40   1.61  565.5  597.3   240   1.00
20180102-20181228  10.00  -10.00    3.752   38.92   19.49   6.12( 0.39)   2.90   0.66  39.95   8.65  586.0  603.5   241   0.99
20190102-20191231  10.00  -10.00    4.933   50.55   16.39   6.30( 0.40)   8.10   0.65  61.66  11.06  592.9  610.3   244   1.00
20200102-20201127  10.00  -10.00    5.036   57.49   36.10   4.34( 0.27)   3.59   0.63  31.85   5.47  467.6  501.9   219   1.00

20170109-20201127  10.00  -10.00   14.985   39.69   21.96   4.39( 0.28)   9.12   0.63  36.19   5.91  555.1  580.1   944   1.00
-0.3086 1966_price_volume
-0.3005 1055_event
-0.2908 274_price_volume
-0.2819 364_price_volume
-0.2600 1818_flow
-0.2582 354_interval
-0.2546 275_price_volume
-0.2531 1231_interval
-0.2497 1704_interval
-0.2432 1914_price_volume
-0.2425 235_price_volume
+0.5070 6795_fundamental
+0.5082 1228_flow
+0.5275 1032_interval
+0.5287 1023_interval
+0.5312 1048_interval
+0.5313 2131_news
+0.5354 2727_ga-price_volume
+0.5430 917_interval
+0.5475 1225_interval
+0.5516 2704_ga-price_volume
----------------------------------------------
+1.2613 815_flow
+1.2790 816_flow
+1.3026 1227_flow
+1.3208 819_flow
+1.3309 813_flow
+1.3620 1230_flow
+1.3803 818_flow
+1.3973 1229_flow
+1.4908 2215_interval
+1.5530 1541_price_volume


/*----- motion score factor -----*/
            dates   long   short   pnl(M)    %ret    %tvr     shrp (IR)    %dd   %win margin  fitsc   lnum   snum tdays tratio
20170109-20171229  10.00  -10.00    0.913    9.51   14.40   1.52( 0.10)   8.01   0.58  13.27   1.23  588.9  579.3   240   1.00
20180102-20181228  10.00  -10.00    3.095   32.10   16.02   5.88( 0.37)   3.28   0.65  40.09   8.33  602.6  590.7   241   0.99
20190102-20191231  10.00  -10.00    3.779   38.72   12.36   6.15( 0.39)   5.68   0.65  62.66  10.89  606.3  603.6   244   1.00
20200102-20201127  10.00  -10.00    3.068   35.02   24.30   3.60( 0.23)   3.87   0.63  28.83   4.32  487.4  490.7   219   1.00

20170109-20201127  10.00  -10.00   10.855   28.75   16.58   4.06( 0.26)   8.01   0.63  34.71   5.34  573.3  568.0   944   1.00


-0.5024 282_interval
-0.4927 161_price_volume
-0.4548 248_price_volume
-0.4398 885_interval
-0.4329 201_price_volume
-0.4323 5_price_volume
-0.4259 2_price_volume
-0.4157 14_price_volume
-0.4135 47_price_volume
-0.4125 313_price_volume
-0.4104 283_interval
+0.3015 322_price_volume
+0.3040 3570_interval
+0.3052 6548_ga-price_volume
+0.3072 274_price_volume
+0.3156 2071_fundamental
+0.3286 2274_fundamental
+0.3319 323_price_volume
+0.3479 4924_interval
+0.4451 4445_fundamental
+0.4453 2592_interval
----------------------------------------------
+0.8580 2694_ga-price_volume
+0.8667 7017_ga-price_volume
+0.8715 4565_fundamental
+0.8782 6363_ga-price_volume
+0.9006 2719_ga-price_volume
+0.9738 3205_interval
+0.9961 6998_ga-price_volume
+1.0767 2705_ga-price_volume
+1.0798 3129_ga-price_volume
+1.1303 6548_ga-price_volume



