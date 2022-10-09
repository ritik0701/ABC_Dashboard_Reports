from django.db import models
from .utils import read_CSV

path = "C:/Ritik/job search/cybrilla/BusinessDevelopmentReport/data.csv"

# Create your models here.
class Report(models.Model):
    lead = models.CharField(max_length = 200)
    id	= models.IntegerField( primary_key=True)
    services = models.CharField(max_length = 200)
    domain = models.CharField(max_length = 200)	
    channels = models.CharField(max_length = 200)	
    stage = models.CharField(max_length = 200)	
    status = models.CharField(max_length = 200)
    sale_representative = models.CharField(max_length=200,null=True)	
    amount = models.DecimalField(max_digits=10, decimal_places=2)	
    created_at = models.DateField(null=True)	
    signed_at = models.DateTimeField(null=True)	
    closed_at = models.DateField(null=True)	

    def  get_queryset():
        # print(report)
        return Report.objects.all()

    def get_dashboard():
        dashboard = {}
        dashboard['total_leads'] = 0
        dashboard['list_total_leads'] = []
        dashboard['status_report'] = {'Signed':0,'Churned':0,'Active':0}
        dashboard['stage_report']={'Prospect':0,'Discussion':0,'Proposal':0,'Contracting':0,'Payment':0}
        dashboard['forecast_revenue'] = []
        dashboard['potential_loss'] = []
        total_revenue = 0
        total_loss = 0

        for row in Report.objects.all():
            if row.status == "Signed":
                dashboard['total_leads']+=1
                dashboard['list_total_leads'].append(row.lead)

            if row.status in dashboard['status_report'].keys():
                dashboard['status_report'][row.status]+=1

            if row.stage in dashboard['stage_report'].keys():
                dashboard['stage_report'][row.stage]+=1

            if row.status == 'Active' and row.stage in ['Proposal','Contracting']:
                dashboard['forecast_revenue'].append([row.lead,row.stage,row.amount*12])
                total_revenue+=row.amount*12

            if row.status=='Churned':
                dashboard['potential_loss'].append([row.lead,row.amount*12])
                total_loss+=row.amount*12

        total_status_value = sum(dashboard['status_report'].values())
        total_stage_value = sum(dashboard['stage_report'].values())
        dashboard['forecast_revenue'].append(['Total','',total_revenue])
        dashboard['potential_loss'].append(['Total',total_loss])

        for status in dashboard['status_report']:
            dashboard['status_report'][status] = (dashboard['status_report'][status]*100)//total_status_value  

        for stage in dashboard['stage_report']:
            dashboard['stage_report'][stage] = (dashboard['stage_report'][stage]*100)//total_stage_value  


        return dashboard

    def load_data():
        data = read_CSV(path)
        for i in data:
            # print(i)
            Report.objects.update_or_create(
                lead=i[0],
                id=i[1],
                services = i[2], 
                domain = i[3], 
                channels = i[4], 	
                stage = i[5], 
                status = i[6], 
                sale_representative = i[7], 	
                amount = i[8], 	
                created_at = i[9], 
                signed_at = i[10] if i[10]!="" else None, 	
                closed_at = i[11] if i[11]!="" else None )
        # Report.objects.bulk_create(data)
        # self.save()
        return(data)


            



    
