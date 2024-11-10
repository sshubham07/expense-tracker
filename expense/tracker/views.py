from django.shortcuts import render,redirect
from django.contrib import messages
from tracker.models import Transaction
from django.db.models import Sum,Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def registration(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(Q(email = email) | Q(username = username)):
            messages.error(request, "email or username already taken")
            return redirect('/registration')
        user_obj = User.objects.create(
            first_name  = first_name,
            last_name = last_name,
            username = username,
            email = email,
        )
        user_obj.set_password(password)
        messages.error(request, "Account Created")
        return redirect('/registration')
    return render(request, 'register.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username)
        if not user_obj.exists():
            messages.error(request, 'username doesnot exists')
            return redirect('/login')
        user_obj = authenticate(username = username, password=password)
        if not user_obj:
            messages.error(request, 'Invalid credentials')
            return redirect('/login')
        login(request, user_obj)
        return redirect('/')
    return render(request, 'login.html')
def logout_page(request):
    logout(request)
    messages.error(request, 'User Logged out')
    return redirect('/registration')
@login_required(login_url='/login')
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
        Transaction.objects.create(created_by = request.user, description=description,amount=amount)
    context = {'transactions' : Transaction.objects.filter(created_by = request.user),
                'balance': Transaction.objects.filter(created_by = request.user).aggregate(total_balance = Sum('amount'))['total_balance'] or 0,
                'income': Transaction.objects.filter(created_by = request.user, amount__gte=0).aggregate(income = Sum('amount'))['income'] or 0,
                'expense': Transaction.objects.filter(created_by = request.user, amount__lte=0).aggregate(expense = Sum('amount'))['expense'] or 0,
                }
    return render(request, 'index.html',context)
@login_required(login_url='/login')
def deleteTransaction(request, uid):
    Transaction.objects.get(uuid =uid).delete()
    return redirect('/')
