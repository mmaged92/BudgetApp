from django.db import models

# Create your models here.
class Bank(models.Model):
    Bank = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.IntegerField()

class Accounts(models.Model):
    user_id = models.IntegerField()
    Bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=255, null=True, blank=True)   # Debit/credit/saving
    account_name = models.CharField(max_length=255, null=True, blank=True)   
    account_number = models.IntegerField() 
