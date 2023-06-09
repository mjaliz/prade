# Generated by Django 4.2.2 on 2023-06-06 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0002_currency_created_at_currency_deleted_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currency',
            old_name='company',
            new_name='name',
        ),
        migrations.CreateModel(
            name='CurrencyPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currencies.currency')),
            ],
        ),
    ]
