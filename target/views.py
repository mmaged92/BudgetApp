from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from .models import years, months
from .models import categories_table, budget_target
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required


years_list = list(range(1990, 2055))

distribution = ['annually','monthly']
category_list = ['housing', 
                 'utilities', 
                 'car payment', 
                 'gas', 
                 'groceries',
                  'proparty tax',
                  'home insurance',
                  'car insurance',
                   'internet',
                   'mobile bills',
                    'car wash',
                    'subscription',
                    'food delivery',
                    'entertainment',
                    'home improvement',
                    'gifts',
                    'donations',
                    'Egypt Expenses',
                    'personal care',
                    'transportation',
                    'miscellaneous',
                    'car maintenance',
                    'home maintenance',
                    'pet care',
                    'loans',
                    'health',
                    'clothes',
                    'sport',
                    'credit card payment',
                    'refund or cashback']

# # file_path_years = 'C:/Users/mahmo/OneDrive/Desktop/Budget/years.csv'
# file_path_months = 'C:/Users/mahmo/OneDrive/Desktop/Budget/months.csv'
# # with open(file_path_years, newline='', encoding='utf-8-sig') as csvfile:
# #     reader = csv.DictReader(csvfile)
# #     for row in reader:
# #         years.objects.create(years=row['year'])

# with open(file_path_months, newline='', encoding='utf-8-sig') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         year =  years.objects.get(id=row['year_id'])
#         months.objects.create(month=row['month'], year_id=year)
# ms= years.objects.all()


# yd = months.objects.select_related("year_id")
# for m in months.objects.all():
#      print(m.month, m.year_id.years)

@login_required(login_url="/users/loginpage/")
def category_add(request):
    user= request.user
    for category in category_list:
        if not categories_table.objects.filter(user_id=user, categories_name=category).exists():
            categories_table.objects.create(user_id=user,categories_name=category)

    if request.method == "POST":
        categories_new = request.POST.get('category')
        if categories_new: 
            if not categories_table.objects.filter(user_id=user, categories_name__iexact=categories_new).exists():
                categories_table.objects.create(user_id=user,categories_name=categories_new)

    categories = categories_table.objects.filter(user_id=user)
    return render(request, 'target/category_edit.html', {"categories":categories})

@login_required(login_url="/users/loginpage/")
def category_get(request):
    user= request.user
    categories = categories_table.objects.filter(user_id=user)
    category_list = []
    for category in categories:
        category_list.append({"Category":category.categories_name, "category_id":category.id})
    return JsonResponse(category_list, safe=False)

@login_required(login_url="/users/loginpage/")
def category_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('new_value')
        category_id = data.get('category_id')
        update = categories_table.objects.get(user_id=user,id=category_id)
        if not categories_table.objects.filter(user_id=user,categories_name__iexact=newValue).exists():
            update.categories_name = newValue
            update.save()
        return JsonResponse({'status': 'updated', 'newValue': newValue})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def category_delete(request):
    user= request.user
    if request.method == 'DELETE':
        data = json.loads(request.body)
        category_id = data.get('category_id')
        try:
            update = categories_table.objects.get(user_id=user,id=category_id)
            update.delete()
        except:
            for id in category_id:
                update = categories_table.objects.get(user_id=user,id=id)
                update.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def target_insert(request):
    user= request.user
    if request.method == "POST":
        freq = request.POST.get('frequency')
        if not freq:
            return

        year = request.POST.get('years')
        if not year:
            return
        else:
            year = years.objects.get(years=year)

        month = request.POST.get('month')
        if not month and freq == "annually":
            month = None
        elif month and freq == "monthly":
            month = months.objects.get(year_id=year, month=month)
        else:
            return

        category = request.POST.get('categories')
        if not category:
            return
        else:
            category = categories_table.objects.get(user_id=user,categories_name=category)

        amount = request.POST.get('amount')
        if not amount:
            return 
        
        if not budget_target.objects.filter(user_id=user,frequency= freq, month_id=month,year_id=year,category_id=category,target=amount).exists():
            budget_target.objects.create(user_id=user,frequency= freq, month_id=month,year_id=year,category_id=category,target=amount)
            return redirect('target_insert')  
        
   
    categories = categories_table.objects.filter(user_id=user)

    return render(request, 'target/targetset.html',{"categories":categories, "years" : years_list})

@login_required(login_url="/users/loginpage/")
def target_delete(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        target_id = data.get('target_id')
        print(target_id)
        try:
            update = budget_target.objects.get(id=target_id)
            update.delete()
        except:
            for id in target_id:
                update = budget_target.objects.get(id=id)
                update.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=405)   

@login_required(login_url="/users/loginpage/")
def target_get(request):
    user= request.user
    targets = budget_target.objects.filter(user_id=user)
    target_list = []
    
    for target in targets:
        try:
            month =  target.month_id.month
            month_id = target.month_id.id
        except:
            month = None
            month_id = None
          
        target_list.append({'year': target.year_id.years, 'month':month, 'category':target.category_id.categories_name
                        ,'target':target.target, 'frequency':target.frequency, 'target_id':target.id, 'year_id':target.year_id.id,
                        'month_id': month_id})            
    return JsonResponse(target_list, safe=False)

@login_required(login_url="/users/loginpage/")
def year_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('newValue')
        target_id = data.get('target_id')
        year_id = data.get('year_id')
        month = data.get('month')

        # print(newValue)
        # print(target_id)
        # print(month)


        yearnew = years.objects.get(years=newValue)
        print(yearnew.years)

        monthnew = months.objects.get(year_id = yearnew, month = month)
        # print(monthnew.year_id.years)

        update = budget_target.objects.get(user_id=user,id=target_id)
        update.year_id = yearnew
        update.save()
        update.month_id = monthnew
        update.save()
        return JsonResponse({'status': 'modified'})
    return JsonResponse({'error':'Invalid method'}, status = 405)

@login_required(login_url="/users/loginpage/")
def month_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('newValue')
        target_id = data.get('target_id')
        year = data.get('year')
        frequency = data.get('frequency')

        # print(newValue)
        # print(target_id)
        # print(year)
        if frequency == 'annually':
            return JsonResponse({'error': 'not allowed'})

        year = years.objects.get(years=year)

        monthnew = months.objects.get(year_id=year, month = newValue)
        # print(monthnew.year_id.years)

        update = budget_target.objects.get(user_id=user,id=target_id)
        update.month_id = monthnew
        update.save()

        return JsonResponse({'status': 'modified'})
    return JsonResponse({'error':'Invalid method'}, status = 405)

@login_required(login_url="/users/loginpage/")
def category_update_target(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('newValue')
        target_id = data.get('target_id')
        newcategory = categories_table.objects.get(user_id=user,categories_name = newValue)
        update = budget_target.objects.get(user_id=user,id=target_id)
        update.category_id = newcategory
        update.save()
        return JsonResponse({'status': 'modified'})
    return JsonResponse({'error':'Invalid method'}, status = 405)

def target_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('newValue')
        target_id = data.get('target_id')
        update = budget_target.objects.get(user_id=user,id=target_id)
        update.target = newValue
        update.save()
        return JsonResponse({'status':'updated'})
    return JsonResponse({'error':'Invalid method'}, status = 405)

@login_required(login_url="/users/loginpage/")
def freq_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('newValue')
        target_id = data.get('target_id')
        year = data.get('year')

        if newValue == 'annually':
            update = budget_target.objects.get(user_id=user,id=target_id)
            update.month_id = None
            update.frequency = 'annually'
            update.save()
        else:
            update = budget_target.objects.get(user_id=user,id=target_id)
            year = years.objects.get(years=year)
            monthnew = months.objects.get(year_id=year, month = 'January')
            update.frequency = 'monthly'
            update.month_id = monthnew
            update.save()
        return JsonResponse({'status':'updated'})
    return JsonResponse({'error':'Invalid method'}, status = 405)

@login_required(login_url="/users/loginpage/")
def monthget(request):
    month = ['January', 'February', 'March', ' April', 'June', 'July', 'August', 'September', 'October'
             , 'November', 'December']
    return JsonResponse(month, safe=False)

@login_required(login_url="/users/loginpage/")
def yearget(request):
    return JsonResponse(years_list, safe=False)

@login_required(login_url="/users/loginpage/")
def freqget(request):
    return JsonResponse(distribution, safe=False)