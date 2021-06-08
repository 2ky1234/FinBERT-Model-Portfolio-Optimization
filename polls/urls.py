from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('text_input/', views.text_input, name = 'text_input'),
    path('mv_input/', views.mv_input, name = 'mv_input'),

    # mv 모델
    path('mv_return/', views.mv_return, name = 'mv_return'),
    path('mv_efficient/', views.mv_efficient, name = 'mv_efficient'),
    path('mv_rebalancing/', views.mv_rebalancing, name = 'mv_rebalancing'),


    # textmining 모델
    path('text_rebalancing/', views.text_rebalancing, name = 'text_rebalancing'),
    path('text_result_visual/', views.text_result_visual, name = 'text_result_visual'),
    path('text_result_graph/', views.text_result_graph, name = 'text_result_graph'),
    path('text_table/', views.text_table, name = 'text_table'),

]