# 시각화용
import numpy as np
import matplotlib.pyplot as plt
import io
import urllib, base64
import pandas as pd

class text_visual:
    def show_graph(input,industry_data):
        A = pd.read_csv('google_master.csv')

        stock = industry_data    

        if (stock[0] in ['AMZN', 'WMT','NVDA']):
            stock = ['AMZN', 'WMT','NVDA']

        elif (stock[0] in ['TSLA','PG','NKE']):
            stock = ['TSLA','PG','NKE']

        elif (stock[0] in ['AAPL', 'MSFT', 'FB']):
            stock = ['AAPL', 'MSFT', 'FB']

        elif (stock[0] in ['JNJ', 'PFE', 'MRK']):
            stock = ['JNJ', 'PFE', 'MRK']
            
        elif (stock[0] in ['GOOGL', 'BRK', 'V']):
            stock = ['GOOGL', 'BRK', 'V']

        mean0 = list(A[A['Company'] == stock[0]]['mean'])
        mean1 = list(A[A['Company'] == stock[1]]['mean'])
        mean2 = list(A[A['Company'] == stock[2]]['mean'])

        mean = [mean0,mean1,mean2]

        date = list(A[A['Company'] == stock[0]]['Date'])

        graph = {'stock' : stock, 'mean' : mean, 'date' : date }

        return graph

    def show_graph_seeking(input,industry_data):
        B = pd.read_csv('seeking_master.csv')

        stock = industry_data    

        if (stock in ['AMZN', 'WMT','NVDA']):
            stock = ['AMZN', 'WMT','NVDA']
        elif (stock in ['TSLA','PG','NKE']):
            stock = ['TSLA','PG','NKE']
        elif (stock in ['AAPL', 'MSFT', 'FB']):
            stock = ['AAPL', 'MSFT', 'FB']
        elif (stock in ['JNJ', 'PFE', 'MRK']):
            stock = ['JNJ', 'PFE', 'MRK']
        elif (stock in ['GOOGL', 'BRK', 'V']):
            stock = ['GOOGL', 'BRK', 'V']

        mean0 = list(B[B['Company'] == stock[0]]['mean'])
        mean1 = list(B[B['Company'] == stock[1]]['mean'])
        mean2 = list(B[B['Company'] == stock[2]]['mean'])

        mean = [mean0,mean1,mean2]

        date = list(B[B['Company'] == stock[0]]['Date'])

        graph = {'stock' : stock, 'mean' : mean, 'date' : date }

        return graph