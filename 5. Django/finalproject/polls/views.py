from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
import pandas as pd
import pandas_datareader.data as web

from polls.mv_return_graph import mv_return_graph
from polls.mv_eff import mv_eff
from polls.mv_rebal import mv_rebal

from polls.text_rebal import text_rebal
from polls.text_eval import text_eval
from polls.text_visual import text_visual


# Create your views here.

# 처음 화면
def index(request):
    context={
    }
    return render(request, 'polls/startpage.html',context)

# mv 모델 input 값 선택 화면
def mv_input(request):
    context={
    }
    return render(request, 'polls/mv_input.html',context)

# textmining 모델 input 값 선택 화면
def text_input(request):
    context={
    }
    return render(request, 'polls/text_input.html',context)

# mv 모델 버튼들
def mv_return(request):

    # 수익률 그래프
    return_gra = mv_return_graph()
    
    start_data_1 = str(request.POST['start'][0:4]+"-"+request.POST['start'][5:7]+"-"+request.POST['start'][8:10])
    end_data_1 =  str(request.POST['end'][0:4]+"-"+request.POST['end'][5:7]+"-"+request.POST['end'][8:10])

    graph = return_gra.Return("5_industry_Portfolios",request.POST['chk_Industry'],start_data_1,end_data_1,10000,'m',0,0,0)

    context={
        'industry_data' : request.POST['chk_Industry'],
        'start_data' : request.POST['start'],
        'end_data' : request.POST['end'],
        'rebal':request.POST['Rebalancing'],
        'return_graph_x':graph['x_date'],
        'return_graph_y':graph['y_return'],
    }
    return render(request, 'polls/mv_return.html',context)

def mv_efficient(request):
    # efficient_frontier 그래프
    a = mv_eff()

    start_data_1 = str(request.POST['start'][0:4]+"-"+request.POST['start'][5:7]+"-"+request.POST['start'][8:10])
    end_data_1 =  str(request.POST['end'][0:4]+"-"+request.POST['end'][5:7]+"-"+request.POST['end'][8:10])
    
    eff_graph = a.efficient_frontier("5_industry_Portfolios",request.POST['chk_Industry'],start_data_1,end_data_1,10000,'m',0,0,0)

    context={
        'industry_data' : request.POST['chk_Industry'],
        'end_data' : request.POST['end'],
        'eff_graph_x' : eff_graph['xx'],
        'eff_graph_y' : eff_graph['yy'],
    }

    return render(request, 'polls/mv_efficient.html', context)

def mv_rebalancing(request):
    b = mv_rebal()

    start_data_1 = str(request.POST['start'][0:4]+"-"+request.POST['start'][5:7]+"-"+request.POST['start'][8:10])
    end_data_1 =  str(request.POST['end'][0:4]+"-"+request.POST['end'][5:7]+"-"+request.POST['end'][8:10])

    rebal_month = request.POST['Rebalancing']

    rebal_graph, abcde, pfo_return = b.efficient_rebalancing("5_industry_Portfolios",request.POST['chk_Industry'],start_data_1,end_data_1,10000,'m',0,0,0, rebal_month)

    context  = {
        'industry_data' : request.POST['chk_Industry'],
        'start_data' : request.POST['start'],
        'end_data' : request.POST['end'],

        'rebal_graph_Date': rebal_graph['Date'],
        'rebal_graph_Cnsmr': rebal_graph['Cnsmr'],
        'rebal_graph_Manuf': rebal_graph['Manuf'],
        'rebal_graph_HiTec': rebal_graph['HiTec'],
        'rebal_graph_Hlth': rebal_graph['Hlth'],
        'rebal_graph_Other': rebal_graph['Other'], 

        'rebal': request.POST['Rebalancing'],

        'A' : abcde[0],
        'AB' :abcde[1],
        'ABC' : abcde[2],
        'ABCD' : abcde[3],
        'ABCDE' : abcde[4],      
    }

    return render(request, 'polls/mv_rebalancing.html',context)


# textmining 모델 버튼들

# textmining rebalancing 버튼
def text_rebalancing(request):

    b = text_rebal()
    pfo = text_eval()
    start_data_1 = str(request.POST['start'][0:4]+"-"+request.POST['start'][5:7]+"-"+request.POST['start'][8:10])
    end_data_1 =  str(request.POST['end'][0:4]+"-"+request.POST['end'][5:7]+"-"+request.POST['end'][8:10])

    rebal_month = request.POST['Rebalancing']

    if request.method == 'POST':
        selected = request.POST.getlist('chk_Industry')

    rebal_graph, abcde, pfo_return, pfo_return_month= b.efficient_rebalancing("5_industry_Portfolios",selected,start_data_1,end_data_1,10000,'m',0,0,0, rebal_month)
    sharpe_eval = pfo.sharpe_ratio(pfo_return_month)[0]
    mdd_eval = pfo.mdd(pfo_return_month)[0]
    value_at_risk_eval = pfo.value_at_risk(pfo_return_month)[0]



    context  = {
        'industry_data' : request.POST['chk_Industry'],
        'start_data' : request.POST['start'],
        'end_data' : request.POST['end'],

        'rebal_graph_Date': rebal_graph['Date'],
        'rebal_graph_AMZN': rebal_graph['AMZN'],
        'rebal_graph_WMT': rebal_graph['WMT'],
        'rebal_graph_NVDA': rebal_graph['NVDA'],
        'rebal_graph_TSLA': rebal_graph['TSLA'],
        'rebal_graph_PG': rebal_graph['PG'], 
        'rebal_graph_NKE': rebal_graph['NKE'],
        'rebal_graph_AAPL': rebal_graph['AAPL'],
        'rebal_graph_JNJ': rebal_graph['JNJ'],
        'rebal_graph_GOOGL': rebal_graph['GOOGL'],
        'rebal_graph_MSFT': rebal_graph['MSFT'], 
        'rebal_graph_PFE': rebal_graph['PFE'],
        'rebal_graph_BRK': rebal_graph['BRK'],
        'rebal_graph_FB': rebal_graph['FB'],
        'rebal_graph_MRK': rebal_graph['MRK'],
        'rebal_graph_V': rebal_graph['V'], 
        'rebal':request.POST['Rebalancing'],

        'sharpe_ratio' : sharpe_eval,
        'mdd' : mdd_eval,
        'value_at_risk' : value_at_risk_eval,

        'A' : abcde[0],
        'AB' :abcde[1],
        'ABC' : abcde[2],
        'ABCD' : abcde[3],
        'ABCDE' : abcde[4],      
        'ABCDEF' : abcde[5],
        'ABCDEFG' :abcde[6],
        'ABCDEFGH' : abcde[7],
        'ABCDEFGHI' : abcde[8],
        'ABCDEFGHIJ' : abcde[9],  
        'ABCDEFGHIJK' : abcde[10],
        'ABCDEFGHIJKL' :abcde[11],
        'ABCDEFGHIJKLM' : abcde[12],
        'ABCDEFGHIJKLMN' : abcde[13],
        'ABCDEFGHIJKLMNO' : abcde[14],  

        'stock' : selected,
    }

   
    return render(request, 'polls/text_JourneyMap.html', context)

# textmining 시각화 버튼
def text_result_visual(request):
    e = text_visual()
    if request.method == 'POST':
        selected = request.POST.getlist('chk_Industry')
    visual_graph = e.show_graph(selected)

    visual_seeking_graph = e.show_graph_seeking(selected)
    
    context = {
        'stock' : selected,

        'stock0' : visual_graph['stock'][0],
        'stock0_mean' : visual_graph['mean'][0],

        'stock1' : visual_graph['stock'][1],
        'stock1_mean' : visual_graph['mean'][1],

        'stock2' : visual_graph['stock'][2],
        'stock2_mean' : visual_graph['mean'][2],

        'date' : visual_graph['date'],

        'seeking_stock0' : visual_seeking_graph['stock'][0],
        'seeking_stock0_mean' : visual_seeking_graph['mean'][0],

        'seeking_stock1' : visual_seeking_graph['stock'][1],
        'seeking_stock1_mean' : visual_seeking_graph['mean'][1],

        'seeking_stock2' : visual_seeking_graph['stock'][2],
        'seeking_stock2_mean' : visual_seeking_graph['mean'][2],

    }
    return render(request, 'polls/text_result_visual.html', context)

# 텍스트마이닝 그래프 버튼
def text_result_graph(request):
    c = text_rebal()

    start_data_1 = str(request.POST['start'][0:4]+"-"+request.POST['start'][5:7]+"-"+request.POST['start'][8:10])
    end_data_1 =  str(request.POST['end'][0:4]+"-"+request.POST['end'][5:7]+"-"+request.POST['end'][8:10])

    rebal_month = request.POST['Rebalancing']

    if request.method == 'POST':
        selected = request.POST.getlist('chk_Industry')

    rebal_graph, abcde, pfo_return, pfo_return_month = c.efficient_rebalancing("5_industry_Portfolios",selected,start_data_1,end_data_1,10000,'m',0,0,0,rebal_month)

    pfo = text_eval()
    table_eval, graph_data = pfo.benchmark_function(pfo_return_month, start_data_1, end_data_1, rebal_month)
    

    context = {
        'industry_data' : request.POST['chk_Industry'],
        'start_data' : request.POST['start'],
        'end_data' : request.POST['end'],

        'g0' : pfo_return,
        'rebal_graph_Date': rebal_graph['Date'],

        'rebal':request.POST['Rebalancing'],
        'stock' : selected,
        'abcde' : abcde,

        'g1' : graph_data['g1'],
        'g2' : graph_data['g2'],
        'g3' : graph_data['g3'],
        'g4' : graph_data['g4'],
        'g5' : graph_data['g5'],
        'g6' : graph_data['g6'],
        'g7' : graph_data['g7'],
    }
    return render(request, 'polls/text_result_graph.html', context)

# 텍스트마이닝 테이블 버튼
def text_table(request):

    if request.method == 'POST':
        selected = request.POST.getlist('chk_Industry')


    b = text_rebal()
    pfo = text_eval()
    start_data_1 = str(request.POST['start'][0:4]+"-"+request.POST['start'][5:7]+"-"+request.POST['start'][8:10])
    end_data_1 =  str(request.POST['end'][0:4]+"-"+request.POST['end'][5:7]+"-"+request.POST['end'][8:10])

    rebal_month = request.POST['Rebalancing']

    rebal_graph, abcde, pfo_return, pfo_return_month= b.efficient_rebalancing("5_industry_Portfolios",selected,start_data_1,end_data_1,10000,'m',0,0,0, rebal_month)
    #sharpe_eval = pfo.sharpe_ratio(pfo_return_month)[0]
    #mdd_eval = pfo.mdd(pfo_return_month)[0]
    #value_at_risk_eval = pfo.value_at_risk(pfo_return_month)[0]
    
    table_eval, graph_data = pfo.benchmark_function(pfo_return_month, start_data_1, end_data_1, rebal_month)


    context = {
        #'stock' : request.POST['chk_Industry']
        'stock' : selected,
        'eval_index':table_eval['index'],
        'eval_index0':table_eval['index'][0],
        'eval_index1':table_eval['index'][1],
        'eval_index2':table_eval['index'][2],
        'eval_index3':table_eval['index'][3],
        'eval_index4':table_eval['index'][4],

        'eval_textmining_pfo':table_eval['textmining_pfo'],
        'eval_textmining_pfo0':table_eval['textmining_pfo'][0],
        'eval_textmining_pfo1':table_eval['textmining_pfo'][1],
        'eval_textmining_pfo2':table_eval['textmining_pfo'][2],
        'eval_textmining_pfo3':table_eval['textmining_pfo'][3],
        'eval_textmining_pfo4':table_eval['textmining_pfo'][4],

        'eval_Equal_Weighted':table_eval['Equal_Weighted'],
        'eval_Equal_Weighted0':table_eval['Equal_Weighted'][0],
        'eval_Equal_Weighted1':table_eval['Equal_Weighted'][1],
        'eval_Equal_Weighted2':table_eval['Equal_Weighted'][2],
        'eval_Equal_Weighted3':table_eval['Equal_Weighted'][3],
        'eval_Equal_Weighted4':table_eval['Equal_Weighted'][4],


        'eval_SNP':table_eval['SNP'],
        'eval_SNP0':table_eval['SNP'][0],
        'eval_SNP1':table_eval['SNP'][1],
        'eval_SNP2':table_eval['SNP'][2],
        'eval_SNP3':table_eval['SNP'][3],
        'eval_SNP4':table_eval['SNP'][4],

        'eval_Cnsmr':table_eval['Cnsmr'],
        'eval_Cnsmr0':table_eval['Cnsmr'][0],
        'eval_Cnsmr1':table_eval['Cnsmr'][1],
        'eval_Cnsmr2':table_eval['Cnsmr'][2],
        'eval_Cnsmr3':table_eval['Cnsmr'][3],
        'eval_Cnsmr4':table_eval['Cnsmr'][4],

        'eval_Manuf':table_eval['Manuf'],
        'eval_Manuf0':table_eval['Manuf'][0],
        'eval_Manuf1':table_eval['Manuf'][1],
        'eval_Manuf2':table_eval['Manuf'][2],
        'eval_Manuf3':table_eval['Manuf'][3],
        'eval_Manuf4':table_eval['Manuf'][4],

        'eval_HiTec':table_eval['HiTec'],
        'eval_HiTec0':table_eval['HiTec'][0],
        'eval_HiTec1':table_eval['HiTec'][1],
        'eval_HiTec2':table_eval['HiTec'][2],
        'eval_HiTec3':table_eval['HiTec'][3],
        'eval_HiTec4':table_eval['HiTec'][4],

        'eval_Hlth':table_eval['Hlth'],
        'eval_Hlth0':table_eval['Hlth'][0],
        'eval_Hlth1':table_eval['Hlth'][1],
        'eval_Hlth2':table_eval['Hlth'][2],
        'eval_Hlth3':table_eval['Hlth'][3],
        'eval_Hlth4':table_eval['Hlth'][4],

        'eval_Other':table_eval['Other'],
        'eval_Other0':table_eval['Other'][0],
        'eval_Other1':table_eval['Other'][1],
        'eval_Other2':table_eval['Other'][2],
        'eval_Other3':table_eval['Other'][3],
        'eval_Other4':table_eval['Other'][4],

    }
    return render(request, 'polls/text_table.html', context)

