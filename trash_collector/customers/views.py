from django.http import HttpResponse
from django.shortcuts import render
from .models import Customer
import requests
import json


# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token faadb088abbd151884296572be6b19d0321922b3'
}


def index(request):
    # get the logged in user within any view function
    user = request.user
    # This will be useful while creating a customer to assign the logged in user as the user foreign key
    # Will also be useful in any function that needs
    print(user)
    return render(request, 'customers/index.html')


def stock(request):
    return render(request, 'customers/stock.html')


def apicall(request):
    ticker = request.GET['ticker']
    price_json = requests.get(f'https://api.tiingo.com/tiingo/daily/{ticker}/prices',
                                   headers=headers)
    stock_info = price_json.json()

    meta_json = requests.get(f'https://api.tiingo.com/tiingo/daily/{ticker}',
                             headers=headers)
    stock_meta = meta_json.json()
    stock_name = stock_meta['name']
    stock_description = stock_meta['description']
    close_value = stock_info[0]['close']
    high_value = stock_info[0]['high']
    low_value = stock_info[0]['low']
    volume = stock_info[0]['volume']

    return render(request, 'customers/stock.html', {'stock_info': stock_info, 'ticker': ticker, 'close_value': close_value, 'high_value': high_value, 'low_value' : low_value, 'volume': volume,'stock_name': stock_name, 'stock_description': stock_description})
