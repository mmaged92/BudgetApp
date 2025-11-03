from django.contrib import admin
from .models import categories_table, budget_target

# Register your models here.

admin.site.register(categories_table)
admin.site.register(budget_target)