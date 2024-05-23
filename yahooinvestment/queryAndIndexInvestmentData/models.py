from django.db import models

# StockData and DividendData are the models that will be used to store the data
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
        # This will ensure that the combination of ticker and date is unique
        unique_together = ('ticker', 'date')


class DividendData(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    dividend = models.FloatField()
    class Meta:
        db_table = 'dividend_data'
        # This will ensure that the combination of ticker and date is unique
        unique_together = ('ticker', 'date')
