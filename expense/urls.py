from django.urls import path
from . import views


urlpatterns = [

    path('monthly_view',views.monthly_view, name="monthly_view"),
    path('monthly_view/category_get_view/',views.category_get_view, name="category_get_view"),
    path('monthly_view/monthly_get/',views.monthly_get, name="monthly_get"),
    path('monthly_view/category_spent/',views.category_spent, name="category_spent"),
    path('monthly_view/category_spent_amounts/',views.category_spent_amounts, name="category_spent_amounts"),
    path('monthly_view/category_spent_daily/',views.category_spent_daily, name="category_spent_daily"),
    path('monthly_view/spentvstarget/',views.spentvstarget, name="spentvstarget"),
    path('monthly_view/incomevsspent/',views.incomevsspent, name="incomevsspent"),
    path('monthly_view/savingvstarget/',views.savingvstarget, name="savingvstarget"),
    path('annual_view',views.annual_view, name="annual_view"),
    path('annual_view/annual_get_target/',views.annual_get_target, name="annual_get_target"),

]
