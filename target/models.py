from django.db import models

# Create your models here.
class years(models.Model):
    years = models.IntegerField()


class months(models.Model):
    month = models.CharField(max_length=255)
    year_id = models.ForeignKey(years, on_delete=models.CASCADE)

class categories_table(models.Model):
    user_id = models.IntegerField()
    categories_name = models.CharField(max_length=255, null=True)

class budget_target(models.Model):
    user_id = models.IntegerField()
    frequency = models.CharField(max_length=255)
    month_id = models.ForeignKey(months,on_delete=models.CASCADE, null=True, blank=True)
    year_id = models.ForeignKey(years,on_delete=models.CASCADE)
    category_id = models.ForeignKey(categories_table,on_delete=models.CASCADE)
    target = models.FloatField()