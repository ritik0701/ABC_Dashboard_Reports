# Generated by Django 4.1.2 on 2022-10-12 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardReports', '0002_report_sale_representative'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='channels',
            field=models.CharField(choices=[('AMC', 'AMC'), ('FP Fintech Distribution', 'FP Fintech Distribution'), ('Enterprise Distribution', 'Enterprise Distribution')], default='AMC', max_length=200),
        ),
        migrations.AlterField(
            model_name='report',
            name='domain',
            field=models.CharField(choices=[('AMC', 'AMC'), ('Fintech', 'Fintech'), ('Enterprise', 'Enterprise')], default='AMC', max_length=200),
        ),
        migrations.AlterField(
            model_name='report',
            name='lead',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='services',
            field=models.CharField(choices=[('MFLite', 'MFLite'), ('MFPro', 'MFPro'), ('AMC', 'AMC')], default='MFlite', max_length=200),
        ),
        migrations.AlterField(
            model_name='report',
            name='stage',
            field=models.CharField(choices=[('Proposal', 'Proposal'), ('Contracting', 'Contracting'), ('Discussion', 'Discussion'), ('Prospect', 'Prospect'), ('Payment', 'Payment')], default='Proposal', max_length=200),
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Churned', 'Churned'), ('Signed', 'Signed')], default='Active', max_length=200),
        ),
    ]
