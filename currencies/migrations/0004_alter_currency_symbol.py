# Generated by Django 4.2.2 on 2023-06-08 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0003_rename_company_currency_name_currencyprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='symbol',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
