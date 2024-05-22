from django.db import models

# Create your models here.
class StockData(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.BigIntegerField()
    adj_close_price = models.FloatField()

    class Meta:
        db_table  = 'stock_data'
        unique_together = ('ticker', 'date')


class DividendData(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    dividend = models.FloatField()

    class Meta:
        unique_together = ('ticker', 'date')
        db_table = 'dividend_data'
