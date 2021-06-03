from os.path import join

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Customer
import requests
from django.apps import apps
import datetime

import json

# Create your views here.


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token faadb088abbd151884296572be6b19d0321922b3'
}


def index(request):
    user = request.user
    Position = apps.get_model('positions.Position')
    positions = Position.objects.all()
    selected_positions = []
    portfolio_balance = 0
    for position in positions:
        if user.id == position.user_id:
            portfolio_balance += position.position_value
            selected_positions.append(position)

    return render(request, 'customers/index.html',
                  {'selected_positions': selected_positions, 'portfolio_balance': portfolio_balance})


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


def stock_details(request, position_id):
    Position = apps.get_model('positions.Position')
    position = Position.objects.get(pk=position_id)
    today = datetime.date.today()
    five_delta = datetime.timedelta(-10)
    early_day = today + five_delta
    price_json = requests.get(f'https://api.tiingo.com/tiingo/daily/{position}/prices',
                              headers=headers)
    stock_info = price_json.json()

    meta_json = requests.get(f'https://api.tiingo.com/tiingo/daily/{position}',
                             headers=headers)
    stock_meta = meta_json.json()
    stock_name = stock_meta['name']
    stock_description = stock_meta['description']
    close_value = stock_info[0]['close']
    high_value = stock_info[0]['high']
    low_value = stock_info[0]['low']
    volume = stock_info[0]['volume']
    historical_data = requests.get(
        f'https://api.tiingo.com/tiingo/daily/{position}/prices?startDate={early_day}&endDate={today}&format=json&resampleFreq=daily',
        headers=headers)
    historical_data_json = historical_data.json()
    active_dates = []

    for i in range(len(historical_data_json)):
        date_time = datetime.datetime.strptime(historical_data_json[i]['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
        date_time_list = date_time.strftime("%B %d")
        active_dates.append(date_time_list)
    i = 0

    historical_prices = []
    historical_dates = []
    for i in range(len(historical_data_json)):
        historical_prices.append(historical_data_json[i]['close'])
        historical_dates.append(historical_data_json[i]['date'])

    return render(request, 'customers/stock_details.html',
                  {'position': position, 'historical_data_json': historical_data_json,
                   'historical_prices': historical_prices, 'historical_dates': historical_dates, 'active_dates': active_dates, 'close_value': close_value, 'high_value': high_value,
                   'low_value': low_value, 'volume': volume, 'stock_name': stock_name,
                   'stock_description': stock_description})

