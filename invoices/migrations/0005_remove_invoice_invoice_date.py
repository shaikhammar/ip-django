# Generated by Django 5.0 on 2024-04-30 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_invoice_invoice_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='invoice_date',
        ),
    ]
