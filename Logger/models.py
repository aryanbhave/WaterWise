from django.db import models

# Create your models here.

class loggerDB(models.Model):
    username=models.CharField(max_length=150)
    bottleID=models.CharField(max_length=150)
    timeStamp=models.TimeField(auto_now=True, auto_now_add=False)
    measurement=models.CharField(max_length=150)

    class Meta:
        db_table='loggerDB'