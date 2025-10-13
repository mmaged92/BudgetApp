from django.shortcuts import render

# Create your views here.
def expense_view(request):
    return render(request, 'expense/expense.html')


