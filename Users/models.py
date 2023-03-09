from django.db import models

# Create your models here.

class bottlesDB(models.Model):
    username=models.CharField(max_length=150)
    bottleID=models.CharField(max_length=150)

    class Meta:
        db_table='bottlesDB' 

class authDB(models.Model):
    username=models.CharField(max_length=150)
    isVerified = models.BooleanField(default=False)

    class Meta:
        db_table='authDB' 
