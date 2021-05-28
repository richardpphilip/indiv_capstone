from django.http import HttpResponse
from django.shortcuts import render
from .models import Customer
import requests
from django.apps import apps
import json

# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token faadb088abbd151884296572be6b19d0321922b3'
}


def index(request):
    user = request.user
    Position = apps.get_model('positions.Position')
    positions = Position.objects.all()
    selected_positions = []
    for position in positions:
        if user.id == position.user_id:
            selected_positions.append(position)
    selected_tickers = []
    selected_values = []
    i = 0

    for i in range(len(selected_positions)):
        selected_tickers += selected_positions[i].selected_ticker
        selected_values += str(selected_positions[i].selected_value)
        print(selected_positions[i].selected_ticker)
        print(str(selected_positions[i].selected_value))
        i += 1
    return render(request, 'customers/index.html', {'selected_positions': selected_positions, 'selected_tickers': selected_tickers, 'selected_values': selected_values})


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

    return render(request, 'customers/stock.html',
                  {'stock_info': stock_info, 'ticker': ticker, 'close_value': close_value, 'high_value': high_value,
                   'low_value': low_value, 'volume': volume, 'stock_name': stock_name,
                   'stock_description': stock_description})
