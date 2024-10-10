from django.shortcuts import render,redirect
from django.contrib import messages
from tracker.models import Transaction

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
        context = {'transactions' : Transaction.objects.all()}
    return render(request, 'index.html',context)
