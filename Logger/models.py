from django.db import models

# Create your models here.

class loggerDB(models.Model):
    bottleID=models.CharField(max_length=150)
    timeStamp=models.DateTimeField(auto_now=True, auto_now_add=False)
    measurement=models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table='loggerDB'