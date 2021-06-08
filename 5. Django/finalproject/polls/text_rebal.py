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

class text_rebal:
    def efficient_rebalancing(input,data_code,industry_data, start_data, end_data, initial,frequency, allocation, min_weight, max_weight, rebal_month):
        #if(frequency == 'y'):
        #    industry_5_list = web.DataReader('5_industry_Portfolios', 'famafrench', start_data, end_data)
        #    industry_5_list = industry_5_list[2]/100

        #else:
        #    industry_5_list = web.DataReader('5_industry_Portfolios', 'famafrench', start_data, end_data)
        #    industry_5_list = industry_5_list[0]/100 """
        symbols = ["AMZN","WMT","NVDA","TSLA","PG",
           "NKE","AAPL","JNJ",'GOOGL',"MSFT","PFE",
           "BRK","FB","MRK","V"]
        
        if (industry_data  == ['all']):
            stock = ["AMZN","WMT","NVDA","TSLA","PG",
           "NKE","AAPL","MSFT","FB","JNJ","PFE",
           "MRK","GOOGL","BRK","V"]
        else:
            stock = industry_data

        

        df = web.get_data_yahoo(symbols, start_data, end_data)['Adj Close']
        df = df.resample('M').agg('last').pct_change().dropna()
        df.index = df.index.strftime('%Y-%m-01')
        df.index = pd.to_datetime(df.index)
        df.index = df.index.to_period('M')

        #textox = pd.read_csv("textox.csv")
        ff3text_judge_p10_normalization = pd.read_csv("ff3text_judge_p10_normalization.csv")
        ff3text_judge_normalization = pd.read_csv("ff3text_judge_normalization.csv")        
        ind5 = df

        Date = []

        AMZN = []
        WMT = []
        NVDA = []
        TSLA = []
        PG = []
        NKE = []
        AAPL = []
        JNJ = []
        GOOGL = []
        MSFT = []
        PFE = []
        BRK = []
        FB = []
        MRK = []
        V = []

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
            #sentiment_ox = ff3text_judge_p10_normalization.iloc[i]
            sentiment_ox = ff3text_judge_normalization.iloc[i]
            Date.append(test_df.index[0].strftime("%Y-%m-%d"))
            ind5_ret = input_df
            mu = ind5_ret.mean() * 12
            sigma = ind5_ret.cov() * 12
            
            asset_list = ind5_ret.columns
            asset_num = len(asset_list)

            if (symbols[0] in stock):
                if sentiment_ox[1] > 0:
                    min_sec1 = 0.05
                    max_sec1 = 1
                elif sentiment_ox[1] < 0:
                    min_sec1 = 0
                    max_sec1 = 1 / len(stock)  
                else:                        
                    min_sec1 = 0
                    max_sec1 = 1
            else:
                min_sec1 = 0
                max_sec1 = 0
            if (symbols[1] in stock):
                if sentiment_ox[2] > 0:
                    min_sec2 = 0.05
                    max_sec2 = 1
                elif sentiment_ox[2] < 0:
                    min_sec2 = 0
                    max_sec2 = 1 / len(stock)  
                else:                        
                    min_sec2 = 0
                    max_sec2 = 1
            else:
                min_sec2 = 0
                max_sec2 = 0   
            if (symbols[2] in stock):
                if sentiment_ox[3] > 0:
                    min_sec3 = 0.05
                    max_sec3 = 1
                elif sentiment_ox[3] < 0:
                    min_sec3 = 0
                    max_sec3 = 1 / len(stock)  
                else:                        
                    min_sec3 = 0
                    max_sec3 = 1
            else:
                min_sec3 = 0
                max_sec3 = 0
            if (symbols[3] in stock):
                if sentiment_ox[4] > 0:
                    min_sec4 = 0.05
                    max_sec4 = 1
                elif sentiment_ox[4] < 0:
                    min_sec4 = 0
                    max_sec4 = 1 / len(stock)  
                else:                        
                    min_sec4 = 0
                    max_sec4 = 1
            else:
                min_sec4 = 0
                max_sec4 = 0
            if (symbols[4] in stock):
                if sentiment_ox[5] > 0:
                    min_sec5 = 0.05
                    max_sec5 = 1
                elif sentiment_ox[5] < 0:
                    min_sec5 = 0
                    max_sec5 = 1 / len(stock)  
                else:                        
                    min_sec5 = 0
                    max_sec5 = 1
            else:
                min_sec5 = 0
                max_sec5 = 0
            if (symbols[5] in stock):
                if sentiment_ox[6] > 0:
                    min_sec6 = 0.05
                    max_sec6 = 1
                elif sentiment_ox[6] < 0:
                    min_sec6 = 0
                    max_sec6 = 1 / len(stock)  
                else:                        
                    min_sec6 = 0
                    max_sec6 = 1
            else:
                min_sec6 = 0
                max_sec6 = 0
            if (symbols[6] in stock):
                if sentiment_ox[7] > 0:
                    min_sec7 = 0.05
                    max_sec7 = 1
                elif sentiment_ox[7] < 0:
                    min_sec7 = 0
                    max_sec7 = 1 / len(stock)  
                else:                        
                    min_sec7 = 0
                    max_sec7 = 1
            else:
                min_sec7 = 0
                max_sec7 = 0
            if (symbols[7] in stock):
                if sentiment_ox[8] > 0:
                    min_sec8 = 0.05
                    max_sec8 = 1
                elif sentiment_ox[8] < 0:
                    min_sec8 = 0
                    max_sec8 = 1 / len(stock)  
                else:                        
                    min_sec8 = 0
                    max_sec8 = 1
            else:
                min_sec8 = 0
                max_sec8 = 0
            if (symbols[8] in stock):
                if sentiment_ox[9] > 0:
                    min_sec9 = 0.05
                    max_sec9 = 1
                elif sentiment_ox[9] < 0:
                    min_sec9 = 0
                    max_sec9 = 1 / len(stock)  
                else:                        
                    min_sec9 = 0
                    max_sec9 = 1
            else:
                min_sec9 = 0
                max_sec9 = 0
            if (symbols[9] in stock):
                if sentiment_ox[10] > 0:
                    min_sec10 = 0.05
                    max_sec10 = 1
                elif sentiment_ox[10] < 0:
                    min_sec10 = 0
                    max_sec10 = 1 / len(stock)  
                else:                        
                    min_sec10 = 0
                    max_sec10 = 1
            else:
                min_sec10 = 0
                max_sec10 = 0
            if (symbols[10] in stock):
                if sentiment_ox[11] > 0:
                    min_sec11 = 0.05
                    max_sec11 = 1
                elif sentiment_ox[11] < 0:
                    min_sec11 = 0
                    max_sec11 = 1 / len(stock)  
                else:                        
                    min_sec11 = 0
                    max_sec11 = 1
            else:
                min_sec11 = 0
                max_sec11 = 0
            if (symbols[11] in stock):
                if sentiment_ox[12] > 0:
                    min_sec12 = 0.05
                    max_sec12 = 1
                elif sentiment_ox[12] < 0:
                    min_sec12 = 0
                    max_sec12 = 1 / len(stock)  
                else:                        
                    min_sec12 = 0
                    max_sec12 = 1
            else:
                min_sec12 = 0
                max_sec12 = 0
            if (symbols[12] in stock):
                if sentiment_ox[13] > 0:
                    min_sec13 = 0.05
                    max_sec13 = 1
                elif sentiment_ox[13] < 0:
                    min_sec13 = 0
                    max_sec13 = 1 / len(stock)  
                else:                        
                    min_sec13 = 0
                    max_sec13 = 1
            else:
                min_sec13 = 0
                max_sec13 = 0
            if (symbols[13] in stock):
                if sentiment_ox[14] > 0:
                    min_sec14 = 0.05
                    max_sec14 = 1
                elif sentiment_ox[14] < 0:
                    min_sec14 = 0
                    max_sec14 = 1 / len(stock)  
                else:                        
                    min_sec14 = 0
                    max_sec14 = 1
            else:
                min_sec14 = 0
                max_sec14 = 0
            if (symbols[14] in stock):
                if sentiment_ox[15] > 0:
                    min_sec15 = 0.05
                    max_sec15 = 1
                elif sentiment_ox[15] < 0:
                    min_sec15 = 0
                    max_sec15 = 1 / len(stock)  
                else:                        
                    min_sec15 = 0
                    max_sec15 = 1
            else:
                min_sec15 = 0
                max_sec15 = 0


            #trets = [0.01]
            
            #print(i)
            w = cp.Variable(asset_num)
            objective = cp.Minimize(cp.quad_form(w, sigma))
            constraints = [cp.sum(w) == 1, w >= 0,
            w[0] >= min_sec1,max_sec1 >= w[0],
            w[1] >= min_sec2,max_sec2 >= w[1],
            w[2] >= min_sec3,max_sec3 >= w[2],
            w[3] >= min_sec4,max_sec4 >= w[3],
            w[4] >= min_sec5,max_sec5 >= w[4],
            w[5] >= min_sec6,max_sec6 >= w[5],
            w[6] >= min_sec7,max_sec7 >= w[6],
            w[7] >= min_sec8,max_sec8 >= w[7],
            w[8] >= min_sec9,max_sec9 >= w[8],
            w[9] >= min_sec10,max_sec10 >= w[9],
            w[10] >= min_sec11,max_sec11 >= w[10],
            w[11] >= min_sec12,max_sec12 >= w[11],
            w[12] >= min_sec13,max_sec13 >= w[12],
            w[13] >= min_sec14,max_sec14 >= w[13],
            w[14] >= min_sec15,max_sec15 >= w[14]]                        
            problem = cp.Problem(objective, constraints)
            problem.solve(solver=cp.ECOS)
            #tvols.append(np.sqrt(np.dot(w.value.T, np.dot(sigma, w.value))))
                        
            AMZN.append(w.value[0])
            WMT.append(w.value[1])
            NVDA.append(w.value[2])
            TSLA.append(w.value[3])
            PG.append(w.value[4])
            NKE.append(w.value[5])
            AAPL.append(w.value[6])
            JNJ.append(w.value[7])
            GOOGL.append(w.value[8])
            MSFT.append(w.value[9])
            PFE.append(w.value[10])
            BRK.append(w.value[11])
            FB.append(w.value[12])
            MRK.append(w.value[13])
            V.append(w.value[14])       
            # dataframe
            #weight = pd.DataFrame({"Date":Date, "Cnsmr":Cnsmr , "Manuf":Manuf , "HiTec":HiTec , "Hlth":Hlth , "Other":Other}).set_index('Date')

        # 누적 weight 구하기    
        #dict
        weight = {"Date":Date, 
        "AMZN":AMZN , "WMT":WMT , "NVDA":NVDA , "TSLA":TSLA , "PG":PG,
        "NKE":NKE , "AAPL":AAPL , "JNJ":JNJ , "GOOGL":GOOGL , "MSFT":MSFT,
        "PFE":PFE , "BRK":BRK , "FB":FB , "MRK":MRK , "V":V}
        
        A = weight['AMZN']
        B = weight['WMT']
        C = weight['NVDA']
        D = weight['TSLA']
        E = weight['PG']
        F = weight['NKE']
        G = weight['AAPL']
        H = weight['JNJ']
        I = weight['GOOGL']
        J = weight['MSFT']
        K = weight['PFE']
        L = weight['BRK']
        M = weight['FB']
        N = weight['MRK']
        O = weight['V']

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
        ABCDEF = list()
        for i, j in zip(ABCDE, F):
            ABCDEF.append(i + j)
        ABCDEFG = list()
        for i, j in zip(ABCDEF, G):
            ABCDEFG.append(i + j)                        
        ABCDEFGH = list()
        for i, j in zip(ABCDEFG, H):
            ABCDEFGH.append(i + j)
        ABCDEFGHI = list()
        for i, j in zip(ABCDEFGH, I):
            ABCDEFGHI.append(i + j)
        ABCDEFGHIJ = list()
        for i, j in zip(ABCDEFGHI, J):
            ABCDEFGHIJ.append(i + j)
        ABCDEFGHIJK = list()
        for i, j in zip(ABCDEFGHIJ, K):
            ABCDEFGHIJK.append(i + j)
        ABCDEFGHIJKL = list()
        for i, j in zip(ABCDEFGHIJK, L):
            ABCDEFGHIJKL.append(i + j)
        ABCDEFGHIJKLM = list()
        for i, j in zip(ABCDEFGHIJKL, M):
            ABCDEFGHIJKLM.append(i + j)
        ABCDEFGHIJKLMN = list()
        for i, j in zip(ABCDEFGHIJKLM, N):
            ABCDEFGHIJKLMN.append(i + j)
        ABCDEFGHIJKLMNO = list()
        for i, j in zip(ABCDEFGHIJKLMN, O):
            ABCDEFGHIJKLMNO.append(i + j)

        abcde = [A,AB,ABC,ABCD,ABCDE,ABCDEF,ABCDEFG,ABCDEFGH,ABCDEFGHI,ABCDEFGHIJ,ABCDEFGHIJK,ABCDEFGHIJKL,ABCDEFGHIJKLM,ABCDEFGHIJKLMN,ABCDEFGHIJKLMNO]
        
        # 포트폴리오 수익률
        ind5_new = ind5.iloc[24:]
        pfo_return = []
        ind5_new = ind5_new.reset_index()
        del ind5_new['Date']
        for i in range(0,int(len(ind5_new)/rebal_month)):
            for j in range(0,rebal_month):
                return_result = list(ind5_new.iloc[(i*rebal_month)+j])
                return_weight = []
                return_weight.append(weight['AMZN'][i])
                return_weight.append(weight['WMT'][i])
                return_weight.append(weight['NVDA'][i])
                return_weight.append(weight['TSLA'][i])
                return_weight.append(weight['PG'][i])
                return_weight.append(weight['NKE'][i])
                return_weight.append(weight['AAPL'][i])
                return_weight.append(weight['JNJ'][i])
                return_weight.append(weight['GOOGL'][i])
                return_weight.append(weight['MSFT'][i])
                return_weight.append(weight['PFE'][i])
                return_weight.append(weight['BRK'][i])
                return_weight.append(weight['FB'][i])
                return_weight.append(weight['MRK'][i])
                return_weight.append(weight['V'][i])
                pfo_return.append(np.dot(return_result,return_weight))

            pfo_return_month = pfo_return
            
        # 변경된 코드    
        pfo_return = [x+1 for x in pfo_return]
        pfo_return = list(it.accumulate(pfo_return, operator.mul))
        pfo_return = [x-1 for x in pfo_return]


        a = [0]
        if (rebal_month != 1):
            pfo_return = a + pfo_return

        pfo_return_temp = []
        if (rebal_month == 1):
            pfo_return_temp = pfo_return
        elif (rebal_month == 3):
            for i in range(0, len(pfo_return), 3):
                pfo_return_temp.append(pfo_return[i])
        elif (rebal_month == 6):
            for i in range(0, len(pfo_return), 6):
                pfo_return_temp.append(pfo_return[i])
        
        pfo_return = pfo_return_temp


    #   pfo_return = list(it.accumulate(pfo_return))
        pfo_return_month = pd.DataFrame(pfo_return_month)
        return weight, abcde, pfo_return, pfo_return_month