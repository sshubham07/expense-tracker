from django.shortcuts import render,redirect
from django.contrib import messages
from tracker.models import Transaction
from django.db.models import Sum

# Create your views here.

def index(request):
    if request.method == "POST":
        print("Inside post method")
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        print(f"{description}, {amount} HERE")
        if description is None or description == "":
            print("Description IS NONE")
            messages.info(request, "Description can not be None")
            return redirect('/')
        try: 
            amount = float(amount)
        except:
            messages.info(request, "Description can not be None")
            return redirect('/')
        Transaction.objects.create(description=description,amount=amount)
    context = {'transactions' : Transaction.objects.all(),
                'balance': Transaction.objects.all().aggregate(total_balance = Sum('amount'))['total_balance'] or 0,
                'income': Transaction.objects.filter(amount__gte=0).aggregate(income = Sum('amount'))['income'] or 0,
                'expense': Transaction.objects.filter(amount__lte=0).aggregate(expense = Sum('amount'))['expense'] or 0,
                }
    return render(request, 'index.html',context)

def deleteTransaction(request, uid):
    Transaction.objects.get(uuid =uid).delete()
    return redirect('/')
