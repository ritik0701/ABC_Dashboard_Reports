from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('piechart', views.load_data, name='load_data'),
]