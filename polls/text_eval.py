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
        
        """param ret: return series
        return : just mean of all record of data and mul * 12
        """
        month_return =  np.mean(ret)
        return (month_return*12)

    def mdd(input,ret):
        """maximum drawdown

        :param ret: return series
        :return: maximum drawdown
        """
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
        """basic sharpe ratio

        :param ret: daily return series(default)
        :param rf: annual risk free rate
        :param num_of_year: using to transfer to yearly data
        :return: basic sharpe ratio
        """
        return ((np.mean(ret - (rf / num_of_year))) / (np.std(ret))) * np.sqrt(num_of_year)


    def calmar_ratio(input,ret, rf=0.002, num_of_year=252):
        """calmar ratio

        :param ret: daily return series
        :param rf: annual risk free rate
        :param num_of_year: using to transfer to yearly data
        :return: calmar ratio
        """
        return (np.mean(ret * num_of_year - rf)) / mdd(ret)


    def winning_rate(input,ret):
        """winning rate = num of win /total number

        :param ret: daily return series
        :return: winning rate
        """
        var_winning_rate = np.sum(ret > 0) / len(ret)
        return var_winning_rate


    def profit_loss_ratio(input,ret):
        """profit loss ratio

        :param ret: daily return series
        :return: 손익비
        """

        if np.sum(ret > 0) == 0:
            var_profit_loss_ratio = 0
        elif np.sum(ret < 0) == 0:
            var_profit_loss_ratio = np.inf
        else:
            win_mean = np.mean(ret[ret > 0])
            loss_mean = np.mean(ret[ret < 0])
            var_profit_loss_ratio = win_mean / loss_mean
        return abs(var_profit_loss_ratio)


    def value_at_risk(input,ret, para_or_hist="para", confidence_level=0.95):
        """value at risk

        :param ret: return series
        :param para_or_hist: para=Parametric VaR, hist=Non-Parametric historical VaR
        :param confidence_level: confidence level
        :return: value at risk
        """
        vol = np.std(ret)
        if para_or_hist == "para":
            VaR = np.mean(ret) - vol * norm.ppf(confidence_level)
        elif para_or_hist == "hist":
            # Sort Returns in Ascending Order
            sorted_ret = sorted(ret)
            VaR = np.percentile(sorted_ret, int((1.0 - confidence_level) * 100))
        else:
            raise Exception("check the value of para_or_hist")

        return VaR

    def evaluation_total(input,ret):
        """
        :param ret_data: return data
        :param risk_free: risk free return data
        :return: performance dataframe
        
        performance = {'MDD': ret_data.apply(eval.mdd),
                    'Sharpe ratio': ret_data.apply(lambda x: eval.sharpe_ratio(x)),
                    'VaR': ret_data.apply(eval.value_at_risk),
                    'Mean': ret_data.apply(eval.Arithmetic_Mean_Annual),
                    'Std': ret_data.std() * np.sqrt(12)}
                    """
        performance = {'MDD': text_eval.mdd(input,ret),
                    'Sharpe ratio': text_eval.sharpe_ratio(input,ret),
                    'VaR': text_eval.value_at_risk(input,ret),
                    'Mean': text_eval.Arithmetic_Mean_Annual(input,ret),
                    'Std': ret.std() * np.sqrt(12)}
        return performance
    def benchmark_function(input,ret, start_data_1, end_data_1):
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


        graph_data = {'g1' : temp_result[0],
                      'g2' : temp_result[1],
                      'g3' : temp_result[2],
                      'g4' : temp_result[3],
                      'g5' : temp_result[4],
                      'g6' : temp_result[5],
                      'g7' : temp_result[6]}


        return table_eval, graph_data

