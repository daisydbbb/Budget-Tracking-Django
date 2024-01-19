from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Income, Category
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference

def search_income(request):
  if request.method=="POST":
    search_str = json.loads(request.body).get('searchText')

    incomes = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            category__icontains=search_str, owner=request.user)
    data = incomes.values()
    return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login/') # not working properly??
def index(request):
  categories = Category.objects.all()
  incomes = Income.objects.filter(owner=request.user)
  # add pagination
  paginator = Paginator(incomes, 5)
  page_number = request.GET.get('page')
  page_obj = Paginator.get_page(paginator, page_number)
  currency = UserPreference.objects.get(user=request.user).currency
  currency_abbre = currency.split('-')[0]

  context = {
    'incomes': incomes,
    'page_obj': page_obj,
    'currency': currency_abbre,
  }
  return render(request, 'incomes/index.html', context)


def add_income(request):
  categories = Category.objects.all()
  context= {
    'categories': categories,
    'values': request.POST,
  }

  if request.method == 'GET':
    return render(request, 'incomes/add_income.html', context)

  if request.method == 'POST':
    amount = request.POST['amount']
    description = request.POST['description']
    date = request.POST['date']
    category = request.POST['category']

    if not amount:
      messages.error(request, 'Please enter the amount!')
      return render(request, 'incomes/add_income.html', context)

    if not description:
      messages.error(request, 'Please enter the description!')
      return render(request, 'incomes/add_income.html', context)

    # create a new expense, use create
    Income.objects.create(owner=request.user, amount=amount, date=date,
                           description=description, category= category)
    messages.success(request, 'Income saved successfully!')
    return redirect('incomes')

def edit_income(request, id):
  income = Income.objects.get(pk=id)
  categories = Category.objects.all()
  context = {
    'income': income,
    'values': income,
    'categories': categories,
  }
  if request.method == 'GET':
    return render(request, 'incomes/edit_income.html', context)

  if request.method == 'POST':
    amount = request.POST['amount']
    description = request.POST['description']
    date = request.POST['date']
    category = request.POST['category']

    if not amount:
      messages.error(request, 'Please enter the amount!')
      return render(request, 'incomes/edit_income.html', context)

    if not description:
      messages.error(request, 'Please enter the description!')
      return render(request, 'incomes/edit_income.html', context)

    # update the income info, use save
    income.owner = request.user
    income.amount = amount
    income.date = date
    income.category = category
    income.description = description

    income.save()

    messages.success(request, 'Income updated successfully!')
    return redirect('incomes')

def delete_income(request, id):
  income = Income.objects.get(pk=id)
  income.delete()
  messages.success(request, 'Income deleted successfully!')
  return redirect('incomes')