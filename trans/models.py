from django.db import models
from target.models import categories_table
from accounts.models import Accounts, Bank
from django.contrib.auth.models import User
from family.models import family
# Create your models here.

class categorization(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    category_id = models.ForeignKey(categories_table, on_delete=models.CASCADE, null=True)
    family_id = models.ForeignKey(family, on_delete=models.CASCADE, null=True, blank=True)

class trans(models.Model):
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    date = models.DateField()
    amount = models.FloatField()
    category_id = models.ForeignKey(categories_table, on_delete=models.CASCADE, null=True)
    IO = models.CharField(max_length=255)
    Accounts_id = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
    family_id = models.ForeignKey(family, on_delete=models.CASCADE, null=True, blank=True)


    