from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from trans.models import trans
from target.models import budget_target, categories_table
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
import json
from saving.models import SavingTarget

year_list = list(range(2023,2055))

month_list =['January', 'February', 'March','April','May','June','July','August','September','October','November','December']
month_dict = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}
month_dict_add = {
    1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN",
    7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"
}
year = date.today().year
month_no = date.today().month
month = month_dict[month_no]
date_start = datetime(year,month_no,1)
date_end = date_start + relativedelta(months=1) 
category_view ='Overall'

def getMonthlyView(user):
    monthly_view=[]   
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    date_start = datetime(year,month_no,1)
    date_end = date_start + relativedelta(months=1)

    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
    
    days_month = date_end - timedelta(days=1)
    days_month = days_month.day
    for category in categories:
        
        category_spent_total = category_spent_sum(user,category,date_start,date_end)
            
        category_target_total = category_target_sum(user,category,month,year)
        if category.categories_name == 'unassigned':
            Remianing = 0
        else:
            Remianing = category_target_total - category_spent_total
        
        status = budget_status(user,category,date_start,date_end, category_target_total,month,year, days_month)

        monthly_view.append({'category': category.categories_name,'Total_spent': category_spent_total , "Total_Target": category_target_total, "Remianing": round(Remianing,2), "Status": status})

    Total_month_spent = category_spent_sum(user,None,date_start,date_end)
    
    Total_month_target = category_target_sum(user,None,month,year)
    
    month_status = budget_status(user,None,date_start,date_end, category_target_total,month,year, days_month)
    

    Total_ramaining = Total_month_target-Total_month_spent
    
    monthly_view.append({'category': "Monthly Total",'Total_spent': Total_month_spent , "Total_Target": Total_month_target, "Remianing": round(Total_ramaining,2), "Status": month_status})
    return monthly_view

def category_spent_sum(user,category,date_start,date_end):
    if category == None:
        category = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
        category_spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense', date__range=(date_start, date_end),category_id__in=category)))['total']    
    else:
        category_spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense', category_id=category, date__range=(date_start, date_end))))['total']    
    if category_spent_total == None:
        category_spent_total = 0
    else:
        category_spent_total = round(category_spent_total,2)
    
    return round(category_spent_total,2)

def spent_day_sum(user,category,date):
    if category == 'Overall':
        category = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
        category_spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense', date=date, category_id__in=category)))['total']    
    else:
        category = categories_table.objects.get(user_id=user,categories_name=category)
        category_spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense', category_id=category, date=date)))['total']    
    if category_spent_total == None:
        category_spent_total = 0
    else:
        category_spent_total = round(category_spent_total,2)
    
    return round(category_spent_total,2)    

def category_target_sum(user,category,month,year):
    category_target_total = 0
    if category == None:
        category_target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user,month=month,year=year)))['total']
    else:    
        category_target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user, category_id=category,month=month,year=year)))['total']
        
    if category_target_total == None:
        category_target_total = 0
         
    return round(category_target_total,2)


def budget_status(user,category,date_start,date_end, category_target_total,month,year, days_month):
    if category == None:
        category = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
        spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense',category_id__in=category, category_id__Fixed_fees=False ,date__range=(date_start, date_end))))['total']
        target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user, category_id__Fixed_fees=False, month=month,year=year)))['total']
    else:
        spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense', category_id=category, category_id__Fixed_fees=False ,date__range=(date_start, date_end))))['total']
        target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user, category_id=category, category_id__Fixed_fees=False, month=month,year=year)))['total']
      
    if spent_total == None:
        spent_total = 0
    if target_total == None:
        target_total = 0
                
    if spent_total > category_target_total:
        status = 'Over Budget'
    elif (spent_total/int(datetime.today().strftime("%d")))  > (target_total/days_month) :
        status = 'Over Spending'
    else:
        status = 'On Budget' 
    return status

def category_spent_pichart(user):
    category_spent=[]   
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    date_start = datetime(year,month_no,1)
    date_end = date_start + relativedelta(months=1)
    
    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
    Total_month_spent = category_spent_sum(user,None,date_start,date_end)
    
    if Total_month_spent == 0:
        return category_spent.append({'y': 100, 'name': "categories_name"})
    
    for category in categories:   
        category_month_spent_total = round(category_spent_sum(user,category,date_start,date_end)*100/Total_month_spent,2)
        category_spent.append({'y': category_month_spent_total, 'name': category.categories_name})
    return category_spent

def category_pent_bar(user):
    category_spent=[]   
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    date_start = datetime(year,month_no,1)
    date_end = date_start + relativedelta(months=1)
    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','trasnfer','income'])
    Total_month_spent = category_spent_sum(user,None,date_start,date_end)
    
    if Total_month_spent == 0:
        return category_spent.append({'label': "categories_name",'y': 100 })
    for category in categories:   
        category_month_spent_total = round(category_spent_sum(user,category,date_start,date_end),2)
        category_spent.append({'label': category.categories_name,'y': category_month_spent_total })
    return category_spent 
    
def category_spent_bar_daily(user):
    category_spent=[]   
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    date_start = datetime(year,month_no,1)
    date = date_start
    date_end = date_start + relativedelta(months=1)

    while(date < date_end):    
        Total_daily_spent = round(spent_day_sum(user,category_view,date),2)
        datedisplay = date.strftime("%b/%d")
        category_spent.append({'y': Total_daily_spent, 'label': datedisplay})
        date = date + timedelta(days=1)

    return category_spent     


def income_calc(user,date_start,date_end):
    return trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='income' ,date__range=(date_start, date_end))))['total']

def target_saving_calc(user,date_start,date_end):
    return SavingTarget.objects.aggregate(total=Sum('Saving_target',filter=Q(user_id=user, date__range=(date_start, date_end))))['total']

def spentVstargetCalc(user):
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    date_start = datetime(year,month_no,1)
    date_end = date_start + relativedelta(months=1)
    print(date_start, date_start)
    target = category_target_sum(user,None,month,year)
    actual_spent = category_spent_sum(user,None,date_start,date_end)
    
    return [{"y": target, "label":"Target"} , {"y": actual_spent, "label":"Actual Spent" }]


def incomeVsspentCalc(user):
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    date_start = datetime(year,month_no,1)
    date_end = date_start + relativedelta(months=1)
    income = income_calc(user,date_start,date_end)
    actual_spent = category_spent_sum(user,None,date_start,date_end)
    return [{"y": income, "label":"Income"} , {"y": actual_spent, "label":"Actual Spent" }]


def savingVstargetCalc(user):
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    date_start = datetime(year,month_no,1)
    date_end = date_start + relativedelta(months=1)
    income = income_calc(user,date_start,date_end)
    actual_spent = category_spent_sum(user,None,date_start,date_end)
    actual_saving = income - actual_spent
    if actual_saving <0:
        actual_saving = 0
    target_saving = target_saving_calc(user,date_start,date_end)
    return [{"y": target_saving, "label":"Target"} , {"y": actual_saving, "label":"Actual Saving" }]

def get_target_calc(user):
    
    target_list = []

    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])        
    
    for category in categories:
        category_dict = {"category": category.categories_name}
        
        for month_no in range(1,13):
            month = month_dict[month_no]
            month_title = month_dict_add[month_no]        
            try:
                target = budget_target.objects.get(user_id=user,category_id = category.id, year=year , month = month)
                target = target.target
            except Exception:
                target = 0
            category_dict[month_title] = target
        
        
        try:
            Category_target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user,category_id = category.id, year=year)))['total'] or 0
            
        except Exception:
            Category_target_total = 0
        category_dict['Total_Target'] = Category_target_total
        target_list.append(category_dict)   
    
    
    
    category_dict = {"category": "Total"}    
    for month_no in range(1,13):
        month = month_dict[month_no]
        month_title = month_dict_add[month_no]
        try:
            target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user, month=month, year=year)))['total']
        except Exception:
            target_total = 0
        category_dict[month_title] = target_total
        
        
    try:
        target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user, year=year)))['total'] or 0
            
    except Exception:
        target_total = 0
    category_dict['Total_Target'] = target_total
    target_list.append(category_dict)  
    
    
    return target_list


# Create your views here.
@login_required(login_url="/users/loginpage/")
def monthly_view(request):
    user = request.user
    global year
    global month
    global month_no
    global date_start
    global date_end
    year = date.today().year
    month_no = date.today().month
    month = month_dict[month_no]
    date_start = datetime(year,month_no,1)
    date_end = date_start + relativedelta(months=1)   
    if request.method == 'POST':
        year = request.POST.get('year')
        year = int(year)
        month = request.POST.get('month')
        request.session["selected_year"] = year
        request.session["selected_month"] = month
    else:
        year = request.session.get("selected_year", year)
        month = request.session.get("selected_month", month)
    
    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
    category_list = ["Overall"]
    for category in categories:
        category_list.append(category.categories_name)
    selected_category = request.session.get("selected_category", "Overall")
    context = {
        'years': year_list,
        'months':month_list,
        "selected_year": year,
        "selected_month": month,
        "categories":category_list,
        "selected_category":selected_category
    }  
    
    return render(request, 'expense/monthly.html',  context)

@login_required(login_url="/users/loginpage/")
def monthly_get(request):    
    return JsonResponse(getMonthlyView(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def category_spent(request):    
    return JsonResponse(category_spent_pichart(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def category_spent_amounts(request):    
    return JsonResponse(category_pent_bar(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def category_spent_daily(request):    
    return JsonResponse(category_spent_bar_daily(request.user), safe=False)
      
@login_required(login_url="/users/loginpage/")
def annual_view(request):
    user = request.user
    global year
    global date_start
    global date_end
    year = date.today().year
    if request.method == 'POST':
        year = request.POST.get('year')
        year = int(year)
        month = request.POST.get('month')
        request.session["selected_year"] = year
    else:
        year = request.session.get("selected_year", year)
    
    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
    category_list = ["Overall"]
    for category in categories:
        category_list.append(category.categories_name)
    selected_category = request.session.get("selected_category", "Overall")
    context = {
        'years': year_list,
        "selected_year": year,
        "categories":category_list,
        "selected_category":selected_category
    }  
    return render(request, 'expense/annually.html', context)

@login_required(login_url="/users/loginpage/")
def annual_get_target(request):
    return JsonResponse(get_target_calc(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def category_get_view(request):
    global category_view
    category_view ='Overall'
    if request.method=="POST":
        data = json.loads(request.body)
        category_view = data.get('category_view')
        request.session["selected_category"] = category_view
        return JsonResponse({'status': 'success'})
    else:
        category_view =  request.session.get("selected_category","Overall")
        return JsonResponse({'selected_category': category_view})
    return JsonResponse({"invalid method":"invalid method"})

@login_required(login_url="/users/loginpage/")
def spentvstarget(request):
    return JsonResponse(spentVstargetCalc(request.user), safe=False)
    
    
@login_required(login_url="/users/loginpage/")
def incomevsspent(request):
    return JsonResponse(incomeVsspentCalc(request.user), safe=False)
    
    
@login_required(login_url="/users/loginpage/")
def savingvstarget(request):
    return JsonResponse(savingVstargetCalc(request.user), safe=False)




