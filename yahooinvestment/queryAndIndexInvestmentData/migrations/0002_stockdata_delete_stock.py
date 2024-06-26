# Generated by Django 5.0.4 on 2024-05-21 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queryAndIndexInvestmentData', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('open_price', models.FloatField()),
                ('high_price', models.FloatField()),
                ('low_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('volume', models.BigIntegerField()),
                ('adj_close_price', models.FloatField()),
            ],
            options={
                'unique_together': {('ticker', 'date')},
            },
        ),
        migrations.DeleteModel(
            name='Stock',
        ),
    ]
