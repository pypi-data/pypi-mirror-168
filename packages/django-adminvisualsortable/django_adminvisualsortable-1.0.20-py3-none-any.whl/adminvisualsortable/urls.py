#-*- coding: utf-8 -*-
from django.urls import path, include, re_path
from adminvisualsortable import views

app_name = 'adminvisualsortable'

urlpatterns_base = [
    path('<slug:app>/<slug:modelname>/', views.sort_models, name='sort models'), # Ordina i Models
    
    path('<slug:app>/<slug:modelparentname>/<int:model_id>/sortinlines/', views.sortable_inlines, name='sortable inlines'), # Lista inlines ordinabili
    path('<slug:app>/<slug:modelparentname>/<int:model_id>/sortinlines/<slug:modelname>/<slug:fkfield>/', views.sortable_inlines_detail, name='sortable inlines detail'), # Ordina gli Inlines
    path('<slug:app>/<slug:modelparentname>/<int:model_id>/sortinlines/<slug:modelname>/', views.sortable_inlines_detail, name='sortable inlines detail'), # Ordina gli Inlines


    
]

urlpatterns_api = [
    path('api/sort-model/', views.api_sort_models, name='api sort models'), # salva le modifiche ordinamento Models
]

urlpatterns = urlpatterns_api + urlpatterns_base
