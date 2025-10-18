from django.shortcuts import render, redirect
from .models import trans, categorization
import csv
from django.http import JsonResponse
from target.models import categories_table
from accounts.models import Bank, Accounts
from datetime import datetime, timedelta
from django.core import serializers
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages


# file_path = 'C:/Users/mahmo/OneDrive/Desktop/Budget/keyword.csv'
# with open(file_path, newline='', encoding='utf-8-sig' ) as csvfile:
#     reader = csv.DictReader(csvfile) 
#     for row in reader:
#         print(row['keyword'], row['category'])
#         keyword = row['keyword']
#         category_id = categories_table.objects.get(id=row['category'])  
#         categorization.objects.create(user_id=1, keyword=keyword, category_id = category_id)

ios = ['income', 'expense', 'credit card payment', 'refund or cashback']
card_types = ['Credit' , 'Debit']
accounts = ['Chequing', ' Saving', 'Credit']

@login_required(login_url="/users/loginpage/")
def trans_add(request):
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=15)
    transactions = trans.objects.filter(date__range=(start_date, end_date)).order_by('-date')
    
    if request.method == "POST":
        input_type = request.POST.get('input_type')

        if input_type =='file_upload':
            card_type = request.POST.get('card_type')
            account_name = request.POST.get('account_name')
            
            account_id = Accounts.objects.get(user_id = 1, account_name=account_name)
            
            file_path = request.FILES['file_path']
                  
            decoded_file = file_path.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            #print(file_path)
        # file_path = 'C:/Users/mahmo/OneDrive/Desktop/Budget/Scotia_Momentum_VISA_card_4023_092825.csv'
            try:
                # with open(file_path, newline='') as csvfile:
                #     reader = csv.DictReader(csvfile)
                for row in reader:
                    # print(row['Description'], row['Date'], row['Amount'])

                    # if not trans.objects.filter(user_id=1, description=row['Description'],date=row['Date'],amount=row['Amount']).exists():
                        amount = row['Amount']

                        try:
                            category = categorization.objects.get(keyword__contains=row['Description'])
                            category = category.category_id
                            # print(category)
                        except Exception:
                            print("doesn't exist need attention") # message here
                            category = None      

                        try:
                            amount =float(amount)
                        except Exception:
                            amount = amount.replace("$", "").replace(",", "")
                            print(amount)
                            amount =float(amount)

                        if card_type == 'Credit' and amount < 0 and ('thank you' in row['Description'].lower() or 'payment' in row['Description'].lower()):
                            category = 'credit card payment'
                            category = categories_table.objects.get(categories_name=category)
                            IO = 'credit card payment'
                        elif card_type == 'Credit' and amount < 0:
                            category = 'refund or cashback'
                            category = categories_table.objects.get(categories_name=category)
                            IO = 'income'
                        elif card_type == 'Credit' and amount > 0:
                            IO = 'expense'
                        elif card_type == 'Debit' and ('visa' in row['Description'].lower() or 'mastercard' in row['Description'].lower()):
                            IO = 'expense'
                            category = 'credit card payment'
                            category = categories_table.objects.get(categories_name=category)
                        elif card_type == 'Debit' and amount < 0:
                            IO = 'expense'
                        else:
                            IO = 'income'

                      
                        if not trans.objects.filter(user_id=1,description=row['Description'],date=row['Date'],amount=abs(amount), category_id = category, IO = IO, Accounts_id= account_id).exists():
                            trans.objects.create(user_id=1,description=row['Description'],date=row['Date'],amount=abs(amount), category_id = category, IO = IO, Accounts_id= account_id)

            except FileNotFoundError:
                print("file not found")
            
            
        if input_type =='single_entry':  
            description = request.POST.get('description')
            date = request.POST.get('date')
            amount = request.POST.get('amount')
            category = request.POST.get('category')

            account_name = request.POST.get('account_name')

            account_id = Accounts.objects.get(account_name=account_name)
            IO = request.POST.get('IO')
            try:
                category = categories_table.objects.get(categories_name=category)
                # print(category)
            except Exception:
                print("doesn't exist need attention") # message here
                category = None
            if not trans.objects.filter(user_id=1, description=description,date=date,amount=amount, category_id = category, IO = IO, Accounts_id=account_id).exists():
                trans.objects.create(user_id=1,description=description,date=date,amount=amount, category_id = category, IO = IO, Accounts_id=account_id)

            
    categories = categories_table.objects.all()
    account_names = Accounts.objects.filter(user_id=1)

    return render(request, 'trans/trans.html', {'transactions': transactions, 'card_types': card_types, 'categories':categories, 'ios':ios, 'account_names':account_names})

@login_required(login_url="/users/loginpage/")
def trans_edit(request):
    print(request)
    return JsonResponse({}, status=405)

@login_required(login_url="/users/loginpage/")
def trans_all(request):
    transactions = trans.objects.all()
    transactions_list = []
    for transaction in transactions:
        if transaction.category_id == None:
            transactions_list.append({'Description': transaction.description, "Date": transaction.date, "Amount":transaction.amount, "IO":transaction.IO
                                  , "Bank":transaction.Accounts_id.account_name,"Category":'***********',
                                  "Account Name":transaction.Accounts_id.account_name, "Account Number": transaction.Accounts_id.account_number,"Account Type":transaction.Accounts_id.account_type,
                                  "Bank":transaction.Accounts_id.Bank.Bank,"category_id":"", "transaction_id":transaction.id, "Account_id":transaction.Accounts_id.id})
        else:
            transactions_list.append({'Description': transaction.description, "Date": transaction.date, "Amount":transaction.amount, "IO":transaction.IO
                                  , "Bank":transaction.Accounts_id.account_name,"Category":transaction.category_id.categories_name,
                                  "Account Name":transaction.Accounts_id.account_name,"Account Number":transaction.Accounts_id.account_number, "Account Type":transaction.Accounts_id.account_type,
                                  "Bank":transaction.Accounts_id.Bank.Bank,"category_id":transaction.category_id.id, "transaction_id":transaction.id, "Account_id":transaction.Accounts_id.id})
    return JsonResponse(transactions_list, safe=False)

@login_required(login_url="/users/loginpage/")

def trans_view(request):
    return render(request, 'trans/view.html')

@login_required(login_url="/users/loginpage/")
def Account_get(request):
    accounts = Accounts.objects.all()
    account_list = []
    for account in accounts:
        account_list.append(account.account_name)
    return JsonResponse(account_list, safe=False)


@login_required(login_url="/users/loginpage/")
def IO_get(request):
    return JsonResponse(ios, safe=False)

@login_required(login_url="/users/loginpage/")
def description_update(request):
    if request.method =='PUT':
        data = json.loads(request.body)
        new_value = data.get('new_value')
        transaction_id = data.get('transaction_id')
        update_value = trans.objects.get(id=transaction_id)
        update_value.description = new_value
        update_value.save()
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def date_update(request):
    if request.method =='PUT':
        data = json.loads(request.body)
        new_value = data.get('new_value')
        transaction_id = data.get('transaction_id')
        update_value = trans.objects.get(id=transaction_id)
        update_value.date = new_value
        update_value.save()
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def amount_update(request):
    if request.method =='PUT':
        data = json.loads(request.body)
        new_value = data.get('new_value')
        transaction_id = data.get('transaction_id')
        update_value = trans.objects.get(id=transaction_id)
        update_value.amount = new_value
        update_value.save()
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def category_update(request):
    if request.method =='PUT':
        data = json.loads(request.body)
        category_id = data.get('category_id')
        new_value = data.get('new_value')
        transaction_id = data.get('transaction_id')

        update_value = trans.objects.get(id=transaction_id)
        new_category_id = categories_table.objects.get(categories_name=new_value)
        update_value.category_id = new_category_id
        update_value.save()
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def IO_update(request):
    if request.method =='PUT':
        data = json.loads(request.body)
        new_value = data.get('new_value')
        transaction_id = data.get('transaction_id')
        update_value = trans.objects.get(id=transaction_id)
        update_value.IO = new_value
        update_value.save()

        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def account_update(request):
    if request.method =='PUT':
        data = json.loads(request.body)
        Account_id = data.get('Account_id')
        new_value = data.get('new_value')
        transaction_id = data.get('transaction_id')

        update_value = trans.objects.get(id=transaction_id)
        new_account_id = Accounts.objects.get(account_name=new_value)
        update_value.Accounts_id = new_account_id
        update_value.save()
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def transaction_delete(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        # print(data)
        transaction_id = data.get('transaction_id')

        try:
            trans_delete = trans.objects.get(id=transaction_id)
            trans_delete.delete()
        except:
            for id in transaction_id:
                trans_delete = trans.objects.get(id=id)
                trans_delete.delete()

        return JsonResponse({'status': 'deleted', 'keyword_id': transaction_id})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def keyword_insert(request):

    if request.method == "POST":
        keyword = request.POST.get('new_keyword')
        category_id = request.POST.get('category_id')
        if keyword and category_id:
            category_id = categories_table.objects.get(id=category_id)
            if not categorization.objects.filter(user_id=1,keyword=keyword, category_id = category_id):    
                categorization.objects.create(user_id=1,keyword=keyword, category_id = category_id)
        else:
            print("error") # insert message error


    category_list = categories_table.objects.all()

    return render(request, 'trans/keyword.html', { 'category_list' : category_list})

@login_required(login_url="/users/loginpage/")
def keyword_all(request):
    keywords = categorization.objects.all()
    keywords_dic =[]
    for keyword in keywords:
        keywords_dic.append({"keyword_id":keyword.id,"keyword":keyword.keyword, "category_id":keyword.category_id.id, "category":keyword.category_id.categories_name})

    return JsonResponse(keywords_dic, safe=False)

@login_required(login_url="/users/loginpage/")
def keyword_delete(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        keyword_id = data.get('keyword_id')
        print(type(keyword_id))
        try:
            category_delete = categorization.objects.get(id=keyword_id)
            category_delete.delete()
        except:
            for id in keyword_id:
                category_delete = categorization.objects.get(id=id)
                category_delete.delete()

        return JsonResponse({'status': 'deleted', 'keyword_id': keyword_id})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def keyword_update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        print(data)
        keyword_id = data.get('keyword_id')
        new_value = data.get('new_value')
        print(keyword_id)
        print(new_value)

        category_update = categorization.objects.get(id=keyword_id)
        category_update.keyword = new_value
        category_update.save()

        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def keyword_category_get(request):
    category_list = categories_table.objects.all()
    category_options = []
    for category in category_list:
        category_options.append(category.categories_name)

    return JsonResponse(category_options, safe=False)

@login_required(login_url="/users/loginpage/")
def keyword_category_update(request):
    if request.method =='PUT':
        data = json.loads(request.body)
        category_id = data.get('category_id')
        new_value = data.get('new_value')
        keyword_id = data.get('keyword_id')
        category_update = categorization.objects.get(id=keyword_id)
        new_category_id = categories_table.objects.get(categories_name=new_value)
        category_update.category_id = new_category_id
        category_update.save()
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)