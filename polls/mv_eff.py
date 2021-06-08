import pandas as pd
import numpy as np
import pandas_datareader.data as web
import json
from datetime import date
import cvxpy as cp

class mv_eff:
    def efficient_frontier(input,data_code,industry_data, start_data, end_data, initial,frequency, allocation, min_weight, max_weight):
        if(frequency == 'y'):
            industry_5_list = web.DataReader(data_code, 'famafrench', start_data, end_data)
            industry_5_list = industry_5_list[2]/100

        else:
            industry_5_list = web.DataReader(data_code, 'famafrench', start_data, end_data)
            industry_5_list = industry_5_list[0]/100
        
        ind5_ret = industry_5_list
        asset_list = ind5_ret.columns
        asset_num = len(asset_list)
        mu = ind5_ret.mean() * 12
        sigma = ind5_ret.cov() * 12
        
        
        gmv_ns2 = cp.Variable(asset_num)
        objective = cp.Minimize(cp.quad_form(gmv_ns2, sigma))
        constraints = [cp.sum(gmv_ns2) == 1, gmv_ns2 >= 0]
        problem = cp.Problem(objective, constraints)
        problem.solve(solver=cp.ECOS)
        gmv_ns2 = gmv_ns2.value
        gmv_ns2
        
        ret_gmv = np.dot(mu.T, gmv_ns2)       

        trets = np.linspace(ret_gmv, max(mu), 30)
        tvols = []
        for tret in trets:
            w = cp.Variable(asset_num)
            objective = cp.Minimize(cp.quad_form(w, sigma))
            constraints = [cp.sum(w) == 1, w >= 0, w @ mu >= tret]
            problem = cp.Problem(objective, constraints)
            problem.solve(solver=cp.ECOS)
            tvols.append(np.sqrt(np.dot(w.value.T, np.dot(sigma, w.value))))

        graph = {'xx' : list(tvols), 'yy' : list(trets)}
        return graph