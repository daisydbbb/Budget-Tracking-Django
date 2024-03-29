from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference

def search_expense(request):
  if request.method=="POST":
    search_str = json.loads(request.body).get('searchText')

    expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
    data = expenses.values()
    return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login/') # not working properly??
def index(request):
  categories = Category.objects.all()
  expenses = Expense.objects.filter(owner=request.user)
  # add pagination
  paginator = Paginator(expenses, 5)
  page_number = request.GET.get('page')
  page_obj = Paginator.get_page(paginator, page_number)
  currency = UserPreference.objects.get(user=request.user).currency
  currency_abbre = currency.split('-')[0]

  context = {
    'expenses': expenses,
    'page_obj': page_obj,
    'currency': currency_abbre,
  }
  return render(request, 'expenses/index.html', context)


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

    # create a new expense, use create
    Expense.objects.create(owner=request.user, amount=amount, date=date,
                           description=description, category= category)
    messages.success(request, 'Expense saved successfully!')
    return redirect('expenses')

def edit_expense(request, id):
  expense = Expense.objects.get(pk=id)
  categories = Category.objects.all()
  context = {
    'expense': expense,
    'values': expense,
    'categories': categories,
  }
  if request.method == 'GET':
    return render(request, 'expenses/edit_expense.html', context)

  if request.method == 'POST':
    amount = request.POST['amount']
    description = request.POST['description']
    date = request.POST['date']
    category = request.POST['category']

    if not amount:
      messages.error(request, 'Please enter the amount!')
      return render(request, 'expenses/edit_expense.html', context)

    if not description:
      messages.error(request, 'Please enter the description!')
      return render(request, 'expenses/edit_expense.html', context)

    # update the expense info, use save
    expense.owner = request.user
    expense.amount = amount
    expense.date = date
    expense.category = category
    expense.description = description

    expense.save()

    messages.success(request, 'Expense updated successfully!')
    return redirect('expenses')

def delete_expense(request, id):
  expense = Expense.objects.get(pk=id)
  expense.delete()
  messages.success(request, 'Expense deleted successfully!')
  return redirect('expenses')