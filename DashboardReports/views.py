from re import S
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from .models import Report

# Create your views here.
def index(request):
    # report = Report()
    dashboard = Report.get_dashboard()
    labels = {'status':[],'stage':[],'service':[],'domain':[]}
    data = {'status':[],'stage':[],'service':[],'domain':[]}

    for status,value in Report.get_dashboard()['status_report'].items():
        labels['status'].append(status)
        data['status'].append(value)
    for stage,value in Report.get_dashboard()['stage_report'].items():
        labels['stage'].append(stage)
        data['stage'].append(value)

    for service,value in Report.get_dashboard()['service_report'].items():
        labels['service'].append(service)
        data['service'].append(value)

    for domain,value in Report.get_dashboard()['domain_report'].items():
        labels['domain'].append(domain)
        data['domain'].append(value)
    return render(request,"index.html",{'dashboard':dashboard,'labels':labels,'data':data})

def load_data(request):
    # report = Report()
    data_status = Report.load_data()
    return render(request,"pie_chart.html",{'data_status':data_status})
