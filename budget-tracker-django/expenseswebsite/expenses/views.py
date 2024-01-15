from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.contrib import messages

@login_required(login_url='/authentication/login/') # not working properly??
def index(request):
  categories = Category.objects.all()
  return render(request, 'expenses/index.html')


def add_expense(request):
  categories = Category.objects.all()
  context= {
    'categories': categories,
    'values': request.POST,
  }

  if request.method == 'GET':
    return render(request, 'expenses/add_expense.html', context)

  if request.method == 'POST':
    amount = request.POST['amount']
    description = request.POST['description']
    date = request.POST['date']
    category = request.POST['category']

    if not amount:
      messages.error(request, 'Please enter the amount!')
      return render(request, 'expenses/add_expense.html', context)

    if not description:
      messages.error(request, 'Please enter the description!')
      return render(request, 'expenses/add_expense.html', context)

    Expense.objects.create(owner=request.user, amount=amount, date=date,
                           description=description, category= category)
    messages.success(request, 'Expense saved successfully!')
    return redirect('expenses')

