from django.db import models
from django.contrib.auth.models import User
from family.models import family
# Create your models here.
class Bank(models.Model):
    Bank = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    family_id = models.ForeignKey(family, on_delete=models.CASCADE, null=True, blank=True)


class Accounts(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=255, null=True, blank=True)   # Debit/credit/saving
    account_name = models.CharField(max_length=255, null=True, blank=True)   
    account_number = models.IntegerField() 
    family_id = models.ForeignKey(family, on_delete=models.CASCADE, null=True, blank=True)
