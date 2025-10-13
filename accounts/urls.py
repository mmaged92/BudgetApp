from . import views
from django.urls import path

urlpatterns = [
    path('',views.add_account,name="add_account"),
    path('getaccounts/',views.get_accounts,name="get_accounts"),
    path('accountname_update/',views.accountname_update,name="accountname_update"),
    path('accounttype_update/',views.accounttype_update,name="accounttype_update"),
    path('accountnumber_update/',views.accountnumber_update,name="accountnumber_update"),
    path('bank_update/',views.bank_update,name="bank_update"),
    path('bank_get/',views.bank_get,name="bank_get"),
    path('accounttype_get/',views.accounttype_get,name="accounttype_get"),
    path('delete/',views.delete_accounts,name="delete"),
]
