from re import S
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from .models import Report

# Create your views here.
def index(request):
    # report = Report()
    dashboard = Report.get_dashboard()
    labels = {'status':[],'stage':[]}
    data = {'status':[],'stage':[]}

    for status,value in Report.get_dashboard()['status_report'].items():
        labels['status'].append(status)
        data['status'].append(value)
    for stage,value in Report.get_dashboard()['stage_report'].items():
        labels['stage'].append(stage)
        data['stage'].append(value)
    return render(request,"index.html",{'dashboard':dashboard,'labels':labels,'data':data})
