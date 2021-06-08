import pandas_datareader.data as web
import numpy as np
import pandas as pd
import json
from datetime import date
import cvxpy as cp

import itertools as it
import operator

class mv_rebal:
    def efficient_rebalancing(input,data_code,industry_data, start_data, end_data, initial,frequency, allocation, min_weight, max_weight, rebal_month):
        if(frequency == 'y'):
            industry_5_list = web.DataReader('5_industry_Portfolios', 'famafrench', start_data, end_data)
            industry_5_list = industry_5_list[2]/100

        else:
            industry_5_list = web.DataReader('5_industry_Portfolios', 'famafrench', start_data, end_data)
            industry_5_list = industry_5_list[0]/100

        textox = pd.read_csv("textox.csv")
        ind5 = industry_5_list

        Date = []
        Cnsmr = []
        Manuf = []
        HiTec = []
        Hlth = []
        Other = []

        if (rebal_month == '1m'):
            rebal_month = 1
        elif (rebal_month == '3m'):
            rebal_month = 3
        elif (rebal_month == '6m'):
            rebal_month = 6

        # 1980.01~1981.12 -> 1982.01
        # 1980.04~1982.03 -> 1982.04

        # 1980.02~1982.02 -> 1982.02
        # ...
        # 2018.09~2020.09 ->2020.10

        for i in range(0,len(ind5)-24, rebal_month):
            input_df = ind5.iloc[i:i+24]
            test_df = ind5.iloc[i+24:i+25]
            sentiment_ox = textox.iloc[i]

            Date.append(test_df.index[0].strftime("%Y-%m-%d"))
            
            ind5_ret = input_df
            mu = ind5_ret.mean() * 12
            sigma = ind5_ret.cov() * 12
            
            asset_list = ind5_ret.columns
            asset_num = len(asset_list)
            if sentiment_ox[1] == 1:
                min_sec1 = 0.1
                max_sec1 = 1
            else:                        
                min_sec1 = 0
                max_sec1 = 0.2
            if sentiment_ox[2] == 1:
                min_sec2 = 0.1
                max_sec2 = 1
            else:                        
                min_sec2 = 0
                max_sec2 = 0.2
            if sentiment_ox[3] == 1:
                min_sec3 = 0.1
                max_sec3 = 1
            else:                        
                min_sec3 = 0
                max_sec3 = 0.2
            if sentiment_ox[4] == 1:
                min_sec4 = 0.1
                max_sec4 = 1
            else:                        
                min_sec4 = 0
                max_sec4 = 0.2
            if sentiment_ox[5] == 1:
                min_sec5 = 0.1
                max_sec5 = 1
            else:                        
                min_sec5 = 0
                max_sec5 = 0.2   
            #trets = [0.01]
            
            #print(i)
            w = cp.Variable(asset_num)
            objective = cp.Minimize(cp.quad_form(w, sigma))
            constraints = [cp.sum(w) == 1, w >= 0]
       #       w[0] >= min_sec1,max_sec1 >= w[0],
       #       w[1] >= min_sec2,max_sec2 >= w[1],
       #       w[2] >= min_sec3,max_sec3 >= w[2],
       #       w[3] >= min_sec4,max_sec4 >= w[3],
       #       w[4] >= min_sec5,max_sec5 >= w[4]]
            problem = cp.Problem(objective, constraints)
            problem.solve(solver=cp.ECOS)
            #tvols.append(np.sqrt(np.dot(w.value.T, np.dot(sigma, w.value))))
                        
            Cnsmr.append(w.value[0])
            Manuf.append(w.value[1])
            HiTec.append(w.value[2])
            Hlth.append(w.value[3])
            Other.append(w.value[4])
            
            # dataframe
            #weight = pd.DataFrame({"Date":Date, "Cnsmr":Cnsmr , "Manuf":Manuf , "HiTec":HiTec , "Hlth":Hlth , "Other":Other}).set_index('Date')


        # 누적 weight 구하기    
        #dict
        weight = {"Date":Date, "Cnsmr":Cnsmr , "Manuf":Manuf , "HiTec":HiTec , "Hlth":Hlth , "Other":Other}
        
        A = weight['Cnsmr']
        B = weight['Manuf']
        C = weight['HiTec']
        D = weight['Hlth']
        E = weight['Other']

        AB = list()
        for i, j in zip(A, B):
            AB.append(i + j)

        ABC = list()
        for i, j in zip(AB, C):
            ABC.append(i + j)

        ABCD = list()
        for i, j in zip(ABC, D):
            ABCD.append(i + j)

        ABCDE = list()
        for i, j in zip(ABCD, E):
            ABCDE.append(i + j)

        abcde = [A,AB,ABC,ABCD,ABCDE]
        
        # 포트폴리오 수익률
        ind5_new = ind5.iloc[24:]
        pfo_return = []
        ind5_new = ind5_new.reset_index()
        del ind5_new['Date']
        for i in range(0,int(len(ind5_new)/rebal_month)):
            return_result = list(ind5_new.iloc[rebal_month * i])
            return_weight = []
            return_weight.append(weight['Cnsmr'][i])
            return_weight.append(weight['Manuf'][i])
            return_weight.append(weight['HiTec'][i])
            return_weight.append(weight['Hlth'][i])
            return_weight.append(weight['Other'][i])

            pfo_return.append(np.dot(return_result,return_weight))

        # 변경된 코드    
        pfo_return = [x+1 for x in pfo_return]
        pfo_return = list(it.accumulate(pfo_return, operator.mul))
        pfo_return = [x-1 for x in pfo_return]
    #   pfo_return = list(it.accumulate(pfo_return))
        
        return weight, abcde, pfo_return


        