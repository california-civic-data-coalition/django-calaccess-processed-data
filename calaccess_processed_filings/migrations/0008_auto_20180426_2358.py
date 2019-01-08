# Generated by Django 2.0.4 on 2018-04-26 23:58

from django.db import migrations, models
from datetime import date


class Migration(migrations.Migration):

    dependencies = [
        ('calaccess_processed_filings', '0007_auto_20180426_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='form461filing',
            name='from_date',
            field=models.DateField(db_index=True, default=date.today(), help_text='The first date of the filing period covered by the statement (from CVR_CAMPAIGN_DISCLOSURE.FROM_DATE)', verbose_name='from date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='form461filing',
            name='statement_type',
            field=models.CharField(default='', help_text='Type of statement, e.g., "Quarterly", "Semi-Annual", Pre-Election (from CVR_CAMPAIGN_DISCLOSURE.STMT_TYPE)', max_length=50, verbose_name='statement type'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='form461filing',
            name='thru_date',
            field=models.DateField(db_index=True, default=date.today(), help_text='The last date of the filing period covered by the statement (from CVR_CAMPAIGN_DISCLOSURE.THRU_DATE)', verbose_name='thru date'),
            preserve_default=False,
        ),
    ]