import pandas_datareader.data as web
import numpy as np
import pandas as pd
import json
from datetime import date
import cvxpy as cp
import math
import itertools as it
import operator
from datetime import datetime
from scipy import stats
from scipy.stats import norm

class text_eval:
    def Arithmetic_Mean_Annual(input,ret) :
        
        month_return =  np.mean(ret)
        return (month_return*12)

    def mdd(input,ret):
        
        cum_ret = (1 + ret).cumprod()
        max_drawdown = 0
        max_ret = 1
        for ix_ret in cum_ret.values:
            if max_drawdown > (ix_ret - max_ret) / max_ret:
                max_drawdown = (ix_ret - max_ret) / max_ret
            if max_ret < ix_ret:
                max_ret = ix_ret

        return abs(max_drawdown)


    def sharpe_ratio(input,ret, rf=0.008, num_of_year=12):
        
        return ((np.mean(ret - (rf / num_of_year))) / (np.std(ret))) * np.sqrt(num_of_year)

    def value_at_risk(input,ret, para_or_hist="para", confidence_level=0.95):
        
        vol = np.std(ret)
        if para_or_hist == "para":
            VaR = np.mean(ret) - vol * norm.ppf(confidence_level)
        else:
            print('error!!!!!')

        return VaR

    def evaluation_total(input,ret):
       
        performance = {'MDD': text_eval.mdd(input,ret),
                    'Sharpe ratio': text_eval.sharpe_ratio(input,ret),
                    'VaR': text_eval.value_at_risk(input,ret),
                    'Mean': text_eval.Arithmetic_Mean_Annual(input,ret),
                    'Std': ret.std() * np.sqrt(12)}
        return performance
        
    def benchmark_function(input,ret, start_data_1, end_data_1, rebal_month):
        benchmark = pd.read_csv("benchmark.csv")

        # 기간 설정 맞추기
        start_data_index = list(benchmark['Date']).index(start_data_1)
        end_data_index = list(benchmark['Date']).index(end_data_1)
        benchmark = benchmark.loc[start_data_index+24:end_data_index]

        a1 = text_eval.evaluation_total(input,pd.DataFrame(benchmark['Equal_Weighted']))
        a1 = pd.DataFrame(a1).T
        a2 = text_eval.evaluation_total(input,pd.DataFrame(benchmark['SNP']))
        a2 = pd.DataFrame(a2).T
        a3 = text_eval.evaluation_total(input,pd.DataFrame(benchmark['Cnsmr']))
        a3 = pd.DataFrame(a3).T
        a4 = text_eval.evaluation_total(input,pd.DataFrame(benchmark['Manuf']))
        a4 = pd.DataFrame(a4).T
        a5 = text_eval.evaluation_total(input,pd.DataFrame(benchmark['HiTec']))
        a5 = pd.DataFrame(a5).T
        a6 = text_eval.evaluation_total(input,pd.DataFrame(benchmark['Hlth']))
        a6 = pd.DataFrame(a6).T
        a7 = text_eval.evaluation_total(input,pd.DataFrame(benchmark['Other']))
        a7 = pd.DataFrame(a7).T
        ev_dict = text_eval.evaluation_total(input,ret)
        ev_dict = pd.DataFrame(ev_dict).T
        ev_dict = ev_dict.rename(columns={0: 'textmining_pfo'})

        total_eval = pd.concat([ev_dict,a1,a2,a3,a4,a5,a6,a7], axis = 1)
        total_eval = total_eval.reset_index()
        table_eval = {'index' : total_eval['index'].tolist(),'textmining_pfo' : total_eval['textmining_pfo'].tolist(), 'Equal_Weighted' : total_eval['Equal_Weighted'].tolist(),
        'SNP' : total_eval['SNP'].tolist(),'Cnsmr' : total_eval['Cnsmr'].tolist(),'Manuf' : total_eval['Manuf'].tolist(),
        'HiTec' : total_eval['HiTec'].tolist(),'Hlth' : total_eval['Hlth'].tolist(),'Other' : total_eval['Other'].tolist()}


        temp = ['Equal_Weighted','SNP','Cnsmr','Manuf','HiTec','Hlth','Other']
        temp_result = []
        for i in range(0,len(temp)):
            temp2 = list(benchmark[temp[i]])
            temp2 = [x+1 for x in temp2]
            temp2 = list(it.accumulate(temp2, operator.mul))
            temp2 = [x-1 for x in temp2]
            temp_result.append(temp2)

      
        ### 수정

        g1 = temp_result[0]
        g2 = temp_result[1]
        g3 = temp_result[2]
        g4 = temp_result[3]
        g5 = temp_result[4]
        g6 = temp_result[5]
        g7 = temp_result[6]

        g1_temp = []
        g2_temp = []
        g3_temp = []
        g4_temp = []
        g5_temp = []
        g6_temp = []
        g7_temp = []

        if (rebal_month == '1m'):
            for i in range(0,len(g1)):
                g1_temp.append(g1[i])
                g2_temp.append(g2[i])
                g3_temp.append(g3[i])
                g4_temp.append(g4[i])
                g5_temp.append(g5[i])
                g6_temp.append(g6[i])
                g7_temp.append(g7[i])

        elif (rebal_month == '3m'):
            for i in range(0,len(g1),3):
                g1_temp.append(g1[i])
                g2_temp.append(g2[i])
                g3_temp.append(g3[i])
                g4_temp.append(g4[i])
                g5_temp.append(g5[i])
                g6_temp.append(g6[i])
                g7_temp.append(g7[i])

        elif (rebal_month == '6m'):
            for i in range(0,len(g1),6):
                g1_temp.append(g1[i])
                g2_temp.append(g2[i])
                g3_temp.append(g3[i])
                g4_temp.append(g4[i])
                g5_temp.append(g5[i])
                g6_temp.append(g6[i])
                g7_temp.append(g7[i])

        g1 = g1_temp
        g2 = g2_temp
        g3 = g3_temp
        g4 = g4_temp
        g5 = g5_temp
        g6 = g6_temp
        g7 = g7_temp

        graph_data = {'g1' : g1,
                      'g2' : g2,
                      'g3' : g3,
                      'g4' : g4,
                      'g5' : g5,
                      'g6' : g6,
                      'g7' : g7}
        
        """
        graph_data = {'g1' : temp_result[0],
                      'g2' : temp_result[1],
                      'g3' : temp_result[2],
                      'g4' : temp_result[3],
                      'g5' : temp_result[4],
                      'g6' : temp_result[5],
                      'g7' : temp_result[6]}
"""

        return table_eval, graph_data

