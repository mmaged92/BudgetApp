from . import views
from django.urls import path

urlpatterns = [
    path('',views.add_account,name="add_account"),
    path('add_bank/',views.add_bank,name="add_bank"),
    path('add_bank/get_banks/',views.get_banks,name="get_banks"),
    path('add_bank/update_banks/',views.update_banks,name="update_banks"),
    path('add_bank/delete_banks/',views.delete_banks,name="delete_banks"),
    path('getaccounts/',views.get_accounts,name="get_accounts"),
    path('accountname_update/',views.accountname_update,name="accountname_update"),
    path('accounttype_update/',views.accounttype_update,name="accounttype_update"),
    path('accountnumber_update/',views.accountnumber_update,name="accountnumber_update"),
    path('accountbalancestart_update/',views.accountbalancestart_update,name="accountbalancestart_update"),
    path('accountbalance_update/',views.accountbalance_update,name="accountbalance_update"),
    path('bank_update/',views.bank_update,name="bank_update"),
    path('account_date_update/',views.account_date_update,name="account_date_update"),
    path('bank_get/',views.bank_get,name="bank_get"),
    path('accounttype_get/',views.accounttype_get,name="accounttype_get"),
    path('delete/',views.delete_accounts,name="delete"),
]
