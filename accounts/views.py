from django.shortcuts import render, redirect
from .models import Accounts, Bank
from django.http import JsonResponse
import json

# Create your views here.
accounts = ['Chequing', ' Saving', 'Credit']
banks_in_canada = [
    "Royal Bank of Canada (RBC)",
    "Toronto-Dominion Bank (TD)",
    "Bank of Nova Scotia (Scotiabank)",
    "Bank of Montreal (BMO)",
    "Canadian Imperial Bank of Commerce (CIBC)",
    "National Bank of Canada",
    "Laurentian Bank of Canada",
    "HSBC Bank Canada (now part of RBC, 2024)",
    "Canadian Western Bank",
    "EQ Bank",
    "Tangerine Bank",
    "Simplii Financial",
    "Desjardins Group",
    "ATB Financial",
    "Manulife Bank of Canada",
    "PC Financial",
    "Wealth One Bank of Canada",
    "First Nations Bank of Canada",
    "Home Trust Company",
    "Bridgewater Bank",
    "Cash"
]


for bank in banks_in_canada:
    if not Bank.objects.filter(Bank=bank).exists():
        Bank.objects.create(Bank=bank)

def add_account(request):

    if request.method == "POST":
        input_type = request.POST.get('input_type')
        if input_type == 'insert_new_account':
            Bank_name = request.POST.get('Bank_name')
            account_type = request.POST.get('account_type')
            account_name = request.POST.get('account_name')
            account_number = request.POST.get('account_number')

            Bank_id = Bank.objects.get(Bank=Bank_name)
            if not Accounts.objects.filter(user_id=1,Bank=Bank_id,account_type=account_type,account_name=account_name,account_number=account_number):
                Accounts.objects.create(user_id=1,Bank=Bank_id,account_type=account_type,account_name=account_name,account_number=account_number)
        if input_type == 'insert_new_bank':
            Bank_new = request.POST.get('Bank_new')
            if not Bank.objects.filter(Bank=Bank_new):
                Bank.objects.create(Bank=Bank_new)
        return redirect('add_account')  

    Banks = Bank.objects.all()
    return render(request, 'account/account.html',{'Banks':Banks, 'accounts':accounts})


def get_accounts(request):
    accounts = Accounts.objects.all()
    accounts_list = []
    for account in accounts:
        accounts_list.append({'Bank':account.Bank.Bank ,'account_type':account.account_type,'account_name':account.account_name,
                              'account_number':account.account_number, 'account_id':account.id})
        print()
    return JsonResponse(accounts_list, safe=False)

def bank_get(request):
    Banks = Bank.objects.all()
    bank_list = []
    for bank in Banks:
        bank_list.append(bank.Bank)
    return JsonResponse(bank_list, safe=False)

def accounttype_get(request):
    return JsonResponse(accounts, safe=False)

def accountname_update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        newvalue = data.get('newValue')
        account_id = data.get('account_id')
        print(newvalue)
        print(account_id)
        update = Accounts.objects.get(id=account_id)
        update.account_name = newvalue
        update.save()
        return JsonResponse({'status': 'updated'})
    return JsonResponse({"error":"invalid method"})

def accounttype_update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        newvalue = data.get('newValue')
        account_id = data.get('account_id')
        print(newvalue)
        print(account_id)
        update = Accounts.objects.get(id=account_id)
        update.account_type = newvalue
        update.save()
        return JsonResponse({'status': 'updated'})
    return JsonResponse({"error":"invalid method"})

def accountnumber_update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        newvalue = data.get('newValue')
        account_id = data.get('account_id')
        print(newvalue)
        print(account_id)
        update = Accounts.objects.get(id=account_id)
        update.account_number = newvalue
        update.save()
        return JsonResponse({'status': 'updated'})
    return JsonResponse({"error":"invalid method"})

def bank_update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        newvalue = data.get('newValue')
        account_id = data.get('account_id')
        print(newvalue)
        print(account_id)
        bankNew = Bank.objects.get(Bank=newvalue)
        update = Accounts.objects.get(id=account_id)
        update.Bank = bankNew
        update.save()
        return JsonResponse({'status': 'updated'})
    return JsonResponse({"error":"invalid method"})

def delete_accounts(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        target_id = data.get('account_id')
        try:
            update = Accounts.objects.get(id=target_id)
            update.delete()
        except:
            for id in target_id:
                update = Accounts.objects.get(id=id)
                update.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=405)   