from django.contrib import admin
from .models import categories_table, budget_target, main_category

# Register your models here.

admin.site.register(categories_table)
admin.site.register(budget_target)
admin.site.register(main_category)