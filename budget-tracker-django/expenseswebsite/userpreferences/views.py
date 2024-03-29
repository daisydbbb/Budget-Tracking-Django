from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages

def index(request):
  currency_data = []
  file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
  with open(file_path, 'r') as file:
      data =json.load(file)
      for k, v in data.items():
        currency_data.append({"name": k, "value": v})

  exist_preference = UserPreference.objects.filter(user=request.user).exists()
  user_preferences = None

  if exist_preference:
    user_preferences = UserPreference.objects.get(user=request.user)
  if request.method == "GET":
    return render(request, 'userpreferences/index.html', {'currencies':currency_data,
                                                          'user_preferences': user_preferences})
  else:
    currency = request.POST['currency']
    if exist_preference:
      user_preferences.currency = currency
      user_preferences.save()
    else:
      UserPreference.objects.create(user=request.user, currency = currency)
    messages.success(request, "Changes saved")
    return render(request, 'userpreferences/index.html', {'currencies': currency_data,
                                                          'user_preferences': user_preferences})