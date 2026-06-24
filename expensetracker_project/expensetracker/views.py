from django.shortcuts import render, redirect
from .models import Expense
from django.db.models import Sum
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDay, TruncMonth, TruncYear, ExtractWeek

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'expensetracker/login.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        else:
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            messages.success(request, "Account created successfully")
            return redirect('login')
    return render(request, 'expensetracker/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    return render(request, 'expensetracker/index.html')

@login_required(login_url='login')
def add_expense(request):
    if request.method == 'POST':
        categories = request.POST.getlist('category[]')
        amounts = request.POST.getlist('amount[]')
        dates = request.POST.getlist('date[]')
        descriptions = request.POST.getlist('description[]')

        for i in range(len(categories)):
            if categories[i] and amounts[i] and dates[i]:
                Expense.objects.create(
                    user=request.user,
                    date=dates[i],
                    category=categories[i],
                    amount=float(amounts[i]),
                    description=descriptions[i]
                )

        return redirect('add_expense')

    return render(request, 'expensetracker/addexpense.html')

@login_required(login_url='login')
def recent_expenses(request):
    recent = Expense.objects.filter(user=request.user).order_by('-id')[:10]
    return render(request, 'expensetracker/recentexpense.html', {'expenses': recent})

@login_required(login_url='login')
def total_expenses(request, period='overall', total_period='overall'):
    today = date.today()

    if period == 'daily':
        table_expenses = Expense.objects.filter(user=request.user, date=today)
    elif period == 'weekly':
        week_start = today - timedelta(days=today.weekday())
        table_expenses = Expense.objects.filter(user=request.user, date__gte=week_start, date__lte=today)
    elif period == 'monthly':
        table_expenses = Expense.objects.filter(user=request.user, date__year=today.year, date__month=today.month)
    else:
        table_expenses = Expense.objects.filter(user=request.user)

    if total_period == 'daily':
        total_grouped = (
            Expense.objects.filter(user=request.user)
            .annotate(day=TruncDay("date"))
            .values("day")
            .annotate(total=Sum("amount"))
            .order_by("day")
        )

    elif total_period == 'weekly':
        qs = Expense.objects.filter(user=request.user)
        grouped = {}
        for e in qs:
            week_start = e.date - timedelta(days=e.date.weekday())
            if week_start not in grouped:
                grouped[week_start] = 0
            grouped[week_start] += e.amount
        total_grouped = [{"week": wk, "total": amt} for wk, amt in sorted(grouped.items())]

    elif total_period == 'monthly':
        total_grouped = (
            Expense.objects.filter(user=request.user)
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )

    elif total_period == 'yearly':
        total_grouped = (
            Expense.objects.filter(user=request.user)
            .annotate(year=TruncYear("date"))
            .values("year")
            .annotate(total=Sum("amount"))
            .order_by("year")
        )

    else:
        total_overall = Expense.objects.filter(user=request.user).aggregate(total=Sum("amount"))['total'] or 0
        return render(request, "expensetracker/totalexpense.html", {
            "expenses": table_expenses,
            "total_overall": total_overall,
            "period": period,
            "total_period": total_period
        })

    return render(request, "expensetracker/totalexpense.html", {
        "expenses": table_expenses,
        "total_grouped": total_grouped,
        "period": period,
        "total_period": total_period
    })
