# Generated by Django 5.0 on 2024-04-29 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_remove_invoice_invoice_total_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='invoice_date',
            field=models.DateField(default='2024-01-01', verbose_name='invoice date'),
        ),
    ]
