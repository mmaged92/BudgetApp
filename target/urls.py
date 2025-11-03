from django.urls import path
from . import views


urlpatterns = [

    path('',views.category_add, name="category_add"),
    path('category_get/',views.category_get, name="category_get"),
    path('category_update/',views.category_update, name="category_update"),
    path('delete/',views.category_delete, name="category_delete"),
    path('targetinsert/',views.target_insert, name="target_insert"),
    path('targetinsert/delete',views.target_delete, name="target_delete"),
    path('targetinsert/all',views.target_get, name="target_get"),
    path('targetinsert/category_update_target',views.category_update_target, name="category_update_target"),
    path('targetinsert/target_update',views.target_update, name="target_update"),
    path('targetinsert/freq_update',views.freq_update, name="freq_update"),
    path('targetinsert/date_update',views.date_update, name="date_update"),
    path('targetinsert/freqget',views.freqget, name="yearget"),
    path('fixed_fees_update/',views.fixed_fees_update, name="fixed_fees_update"),

]
