# FinBERT-Model-Portfolio-Optimization-
FinBERT는 금융 텍스트의 감정을 분석하기 위해 사전 훈련된 NLP 모델이다. 금융 영역에서 BERT 언어 모델을 추가로 교육하여 대규모 금융 코퍼스를 사용하여 금융감성 분류를 위해 이를 미세 조정함으로써 구축된다. 이러한 FinBERT 모델을 활용하여 포트폴리오를 구성하는 개별종목(미국의 섹터별 대표 3개의 종목)의 월별 asset allocation을 조정하여 최적화 및 리밸런싱을 진행하였다. 또한 구성된 포트폴리오의 결과를 벤치마크와 비교하고 백테스트를 실행한다.

링크 : https://github.com/ProsusAI/finBERT

<!-- Output copied to clipboard! -->

<!-----
NEW: Check the "Suppress top comment" option to remove this info from the output.

Conversion time: 0.686 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β29
* Tue Jun 08 2021 09:12:03 GMT-0700 (PDT)
* Source doc: READ ME_코드 정리
* Tables are currently converted to HTML tables.
----->


1.  크롤링



1. Google News
*   google email, password, 검색어, 크롤링 기간을 입력한 후 실행 가능
2. Seeking Alpha

2. 감성분석 : open source를 사용하여 진행하였습니다. 



1. NLTK

    [https://github.com/NemesLaszlo](https://github.com/NemesLaszlo)

2. FIN BERT 

    [https://github.com/ProsusAI/finBERT](https://github.com/ProsusAI/finBERT)


3. feature selection



*   random forest
*   adaboost

4. 회귀분석

5. Django 기능



*   python 코드
*   기본 M-V 모델

<table>
  <tr>
   <td>
py 파일 명
   </td>
   <td>기능 설명
   </td>
  </tr>
  <tr>
   <td>mv_return_graph.py  
   </td>
   <td>기본 m-v 모델에서 return graph를 그리기 위한 데이터를 생성하는  기능. 5개 industry를 선택할 수 있다. 
   </td>
  </tr>
  <tr>
   <td>mv_eff.py 
   </td>
   <td>기본 m-v 모델에서 efficient frontier를 그리기 위한 데이터를 생성하는 기능.
   </td>
  </tr>
  <tr>
   <td>mv_rebal.py
   </td>
   <td>기본 m-v 모델에서 rebalancing graph를 그리기 위한 데이터를 생성하는 기능. industry 선택 기능은 추가하지 않았고, 5개 산업군을 모두 포함한 결과만 확인 가능.
   </td>
  </tr>
</table>




*   텍스트마이닝 모델

<table>
  <tr>
   <td>
py 파일 명
   </td>
   <td>기능 설명
   </td>
  </tr>
  <tr>
   <td>text_rebal.py
   </td>
   <td>text mining 모델에서 rebalancing 그래프를 그리기위한 데이터를 생성하는 기능. 15개 stock을 (복수)선택 및 전체 선택할 수 있고, rebalancing 주기 및 기간을 선택할 수 있다. 
<p>
기간의 경우 2015.09~2020.09 이내에서 원하는 기간을 설정할 수 있다. 
   </td>
  </tr>
  <tr>
   <td>text_visual.py
   </td>
   <td>text mining 모델에서 text mining 결과를 그리기 위한 데이터를 생성하는 기능. 원하는 산업군에 대한 그래프를 보고 싶다면, 해당 산업군에 대한 stock을 모두 선택해야한다. 예를 들면 Cnsmr에 대한 결과를 보고 싶다면 AMZN,WMT,NVDA를 모두 선택한다. 
   </td>
  </tr>
  <tr>
   <td>text_eval.py
   </td>
   <td>text mining 모델에서 text mining 결과 그래프와 결과 테이블을 그리기 위한 데이터를 생성하는 기능. 테이블에서 사용한 지표들(MDD, Sharpe ratio, VaR 등등)을 이곳에서 생성하였고, 벤치마크와 함께 그래프를 그리기 위한 기능도 존재한다. (def benchmark_function)
   </td>
  </tr>
</table>




*   csv 파일
*   따로 DB를 사용하지는 않았고, 필요한 데이터의 경우 직접 yahoo에서 가져오거나, csv 파일 형태로 저장한 후 불러와서 사용하는 방식으로 진행하였다. 
*   csv 파일의 경우 benchmark, text mining 결과, text mining 지수 생성 결과 등을 포함시켰다. 
*   html 파일

<table>
  <tr>
   <td>
html 파일 명
   </td>
   <td>기능 설명
   </td>
  </tr>
  <tr>
   <td>startpage.html
   </td>
   <td>기본 M-V 모델과 텍스트마이닝 기능 선택 화면
   </td>
  </tr>
  <tr>
   <td>mv_input.html
   </td>
   <td>기본 M-V 모델 INPUT 입력받는 화면
   </td>
  </tr>
  <tr>
   <td>mv_return.html
   </td>
   <td>기본 M-V 모델 return graph 그리는 화면
   </td>
  </tr>
  <tr>
   <td>mv_efficient.html
   </td>
   <td>기본 M-V 모델 efficient frontier 그리는 화면
   </td>
  </tr>
  <tr>
   <td>mv_rebalancing.html
   </td>
   <td>기본 M-V 모델 rebalancing 그래프 그리는 화면
   </td>
  </tr>
  <tr>
   <td>text_input.html
   </td>
   <td>텍스트마이닝 모델 INPUT 입력받는 화면
   </td>
  </tr>
  <tr>
   <td>text_JourneyMap.html
   </td>
   <td>텍스트마이닝 모델 rebalancing 그래프 그리는 화면
   </td>
  </tr>
  <tr>
   <td>text_result.visual.html
   </td>
   <td>텍스트마이닝 결과 그래프 그리는 화면
   </td>
  </tr>
  <tr>
   <td>text_result_graph.html
   </td>
   <td>텍스트마이닝 모델 결과 return graph 그리는 화면
<p>
(벤치마크와 수익률 비교하는 그래프)
   </td>
  </tr>
  <tr>
   <td>text_table.html
   </td>
   <td>텍스트마이닝 결과 테이블 보여주는 화면
   </td>
  </tr>
</table>


********* 장고 실행법 ********



1. 장고 파일(finalproject)를 원하는 위치에 놓는다. 
2. Anaconda Prompt에서 가상환경을 만든후 activate 한다.
3. 패키지를 설치한다. (아래 패키지 목록 첨부)
4. finalproject 위치로 들어가서 명령어 **py manage.py runserver** 입력
5. visual code에서 장고 작업을 실행했습니다. 

    visual code에서 finalproject 폴더를 열면 코드를 보실 수 있습니다. 

*   패키지 설치 명령어

-> conda install -c conda-forge cvxpy

-> conda install scipy

-> conda install  Django

-> conda install  pandas

-> conda install  numpy

-> pip install  DateTime

-> conda install  matplotlib

-> conda install -c anaconda pandas-datareader



