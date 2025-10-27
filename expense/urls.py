from django.urls import path
from . import views


urlpatterns = [

    path('monthly_view',views.monthly_view, name="monthly_view"),
    path('monthly_view/monthly_get/',views.monthly_get, name="monthly_get"),
    path('monthly_view/category_spent/',views.category_spent, name="category_spent"),
    path('',views.annual_view, name="annual_view"),

]
