from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
from django.apps import apps
from .models import Position


# Create your views here.
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token faadb088abbd151884296572be6b19d0321922b3'
}


def index(request):
    return render(request, 'positions/index.html')


def create(request):
    if request.method == 'POST':
        user = request.user
        selected_ticker = request.POST.get('selected_ticker')
        selected_value = request.POST.get('selected_value')
        price_json = requests.get(f'https://api.tiingo.com/tiingo/daily/{selected_ticker}/prices',
                                  headers=headers)
        stock_info = price_json.json()
        close_value = stock_info[0]['close']
        stock_close_value = close_value
        selected_value_int= int(selected_value)
        position_value = stock_close_value * selected_value_int
        print(position_value)
        new_position = Position(selected_ticker=selected_ticker, selected_value=selected_value,stock_close_value=stock_close_value, user_id=user.id, position_value=position_value)
        new_position.save()
        return HttpResponseRedirect(reverse('positions:index'))
    else:
        print('error')
        return HttpResponseRedirect(reverse('positions:index'))

def update_all(request):
    print("this works")
    return render(request, 'positions/update_all.html')




