from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('piechart', views.pie_chart, name='pie_chart'),
]