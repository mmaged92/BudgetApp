from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from trans.models import trans
from target.models import budget_target, categories_table, months, years
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
import json

year_list = list(range(2023,2055))

month_list =['January', 'February', 'March','April','May','June','July','August','September','October','November','December']
month_dict = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
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
    # print(month_no,type(month_no), month, year)
    date_start = datetime(year,month_no,1)
    date_end = date_start + relativedelta(months=1)
    year_id = years.objects.get(years = year)
    month_id = months.objects.get(year_id=year_id, month=month)
    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
    
    days_month = date_end - timedelta(days=1)
    days_month = int(days_month.strftime("%d"))
    
    for category in categories:
        
        category_spent_total = category_spent_sum(user,category,date_start,date_end)
            
        category_target_total = category_target_sum(user,category,month_id,year_id)
        if category.categories_name == 'unassigned':
            Remianing = 0
        else:
            Remianing = category_target_total - category_spent_total
        
        status = budget_status(user,category,date_start,date_end, category_target_total,month_id,year_id, days_month)

        monthly_view.append({'category': category.categories_name,'Total_spent': category_spent_total , "Total_Target": category_target_total, "Remianing": round(Remianing,2), "Status": status})

    Total_month_spent = category_spent_sum(user,None,date_start,date_end)
    
    Total_month_target = category_target_sum(user,None,month_id,year_id)
    
    month_status = budget_status(user,None,date_start,date_end, category_target_total,month_id,year_id, days_month)
    

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

def category_target_sum(user,category,month_id,year_id):
    category_target_total = 0
    if category == None:
        category_target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user,month_id=month_id,year_id=year_id)))['total']
    else:    
        category_target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user, category_id=category,month_id=month_id,year_id=year_id)))['total']
        
    if category_target_total == None:
        category_target_total = 0
         
    return round(category_target_total,2)


def budget_status(user,category,date_start,date_end, category_target_total,month_id,year_id, days_month):
    if category == None:
        category = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
        spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense',category_id__in=category, category_id__Fixed_fees=False ,date__range=(date_start, date_end))))['total']
        target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user, category_id__Fixed_fees=False, month_id=month_id,year_id=year_id)))['total']
    else:
        spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense', category_id=category, category_id__Fixed_fees=False ,date__range=(date_start, date_end))))['total']
        target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user, category_id=category, category_id__Fixed_fees=False, month_id=month_id,year_id=year_id)))['total']
      
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
    return render(request, 'expense/annually.html', {'years': year_list,'months':month_list})


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


