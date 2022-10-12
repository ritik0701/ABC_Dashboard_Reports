import datetime
from django.db import models
from .utils import read_CSV,validate_date

path = "C:/Users/ritik/Downloads/datatest.csv"

# Create your models here.
class Report(models.Model):

    lead = models.CharField(max_length = 200,unique=True)
    id	= models.IntegerField( primary_key=True)

    SERVICES_CHOICES = (('MFLite','MFLite'), ('MFPro','MFPro'),('AMC','AMC'))
    services = models.CharField(max_length = 200,choices=SERVICES_CHOICES,default='MFlite')

    DOMAIN_CHOICES = (('AMC','AMC'),('Fintech','Fintech'),('Enterprise','Enterprise')) 
    domain = models.CharField(max_length = 200,choices=DOMAIN_CHOICES,default='AMC')

    CHANNELS_CHOICES = (('AMC','AMC'), ('FP Fintech Distribution','FP Fintech Distribution'),('Enterprise Distribution','Enterprise Distribution'))
    channels = models.CharField(max_length = 200,choices=CHANNELS_CHOICES,default='AMC')	

    STAGE_CHOICES = (('Proposal','Proposal'),('Contracting','Contracting'),('Discussion','Discussion'),('Prospect','Prospect'),('Payment','Payment'))
    stage = models.CharField(max_length = 200,choices=STAGE_CHOICES,default='Proposal')	

    STATUS_CHOICES = (('Active','Active'),('Churned','Churned'),('Signed','Signed'))
    status = models.CharField(max_length = 200,choices=STATUS_CHOICES,default='Active')


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
        dashboard['sales_rep_of_month'] = ''
        dashboard['service_report'] = {'MFLite':0, 'MFPro':0,'AMC':0}
        dashboard['domain_report'] = {'AMC':0,'Fintech':0,'Enterprise':0}

        total_revenue = 0
        total_loss = 0

        # Used to get Sales rep of month
        sales_rep_count = {}
        now = datetime.datetime.now()
        last_month = now.month-1 if now.month > 1 else 12

        query_set = Report.get_queryset()

        for row in query_set:
            # 
            if row.status == "Signed":
                dashboard['total_leads']+=1
                dashboard['list_total_leads'].append(row.lead)

            # 
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

            if row.services in dashboard['service_report'].keys():
                dashboard['service_report'][row.services]+=1

            if row.domain in dashboard['domain_report'].keys():
                dashboard['domain_report'][row.domain]+=1

            if row.signed_at:
                if row.signed_at.month == last_month and row.sale_representative in sales_rep_count.keys():
                    sales_rep_count[row.sale_representative]+=row.amount
                else:
                    sales_rep_count[row.sale_representative]=row.amount

        total_status_value = sum(dashboard['status_report'].values())
        total_stage_value = sum(dashboard['stage_report'].values())
        total_service_value = sum(dashboard['service_report'].values())
        total_domain_value = sum(dashboard['domain_report'].values())

        dashboard['forecast_revenue'].append(['Total','',total_revenue])
        dashboard['potential_loss'].append(['Total',total_loss])

        # Get Status Report Data
        for status in dashboard['status_report']:
            dashboard['status_report'][status] = (dashboard['status_report'][status]*100)//total_status_value  

        # get Stage Report Data
        for stage in dashboard['stage_report']:
            dashboard['stage_report'][stage] = (dashboard['stage_report'][stage]*100)//total_stage_value  

        # Get Services Report Data
        for service in dashboard['service_report']:
            dashboard['service_report'][service] = (dashboard['service_report'][service]*100)//total_service_value  

        # get Domain Report Data
        for domain in dashboard['domain_report']:
            dashboard['domain_report'][domain] = (dashboard['domain_report'][domain]*100)//total_domain_value  


        # Get Sales Rep Of Last Month
        max_amount = max(sales_rep_count.values())

        for sales_rep,amount in sales_rep_count.items():
            if max_amount == amount:
                dashboard['sales_rep_of_month'] = sales_rep
                break

        return dashboard

    def load_data():
        data = read_CSV(path)
        data_status = {}
        data_status['success']=[]
        data_status['failed']=[]
        for i in data:
            try:
                if i[2] not in Report.SERVICES_CHOICES:
                    raise Exception("Invalid Service")

                if i[3] not in Report.DOMAIN_CHOICES:
                    raise Exception("Invalid Domain")

                if i[4] not in Report.CHANNELS_CHOICES:
                    raise Exception("Invalid Channel")

                if i[5] not in Report.STAGE_CHOICES:
                    raise Exception("Invalid Stage")

                if i[6] not in Report.STATUS_CHOICES:
                    raise Exception("Invalid Status")

                created_date = validate_date(i[9]).date()
                signed_date = validate_date(i[10]) if i[10]!="" else None
                closed_date = validate_date(i[11]) if i[11]!='' else None

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
                    created_at = created_date, 
                    signed_at = signed_date, 	
                    closed_at = closed_date )

                data_status['success'].append(i[1])
            except Exception:
                data_status['failed'].append(i[1])
        return(data_status)


            



    
