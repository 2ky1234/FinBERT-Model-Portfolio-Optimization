import pandas as pd
import numpy as np
import pandas_datareader.data as web
import json
from datetime import date


class mv_return_graph:
    def Return(input,data_code,industry_data, start_data, end_data, initial,frequency, allocation, min_weight, max_weight):
        '''       
        if(frequency == 'y'):
            industry_5_list = web.DataReader(data_code, 'famafrench', start_data, end_data)
            industry_5_list = industry_5_list[2]/100
    
        else:
            industry_5_list = web.DataReader(data_code, 'famafrench', start_data, end_data)
            industry_5_list = industry_5_list[0]/100
        
        '''
        ind5 =  pd.read_csv("5_Industry_Portfolios_Daily.CSV")
        ind5.columns = ['Date', 'Cnsmr', 'Manuf', 'HiTec', 'Hlth ', 'Other']
        # 1980년부터 데이터 가져오기
        ind5 = ind5[14556:]
        ind5 = ind5.reset_index()
        del ind5['index']
        ind5['Date'] = pd.Series(ind5['Date'])
        ind5 = ind5.set_index(['Date'])
        ind5.index = pd.to_datetime(ind5.index, format = '%Y%m%d')  # day로 사용할때 필요

        ind5 = ind5/100
        

        ind5 = ind5.loc[start_data:end_data]  # day로 사용할때 필요

        industry_5_list = ind5
        
        industry_5_list['x_date'] = industry_5_list.index.strftime("%Y-%m-%d")
        graph = {'x_date' : industry_5_list['x_date'].tolist(), 'y_return' : industry_5_list[industry_data].tolist()}
        return graph