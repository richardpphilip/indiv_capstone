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
    historical_data = requests.get(f'https://api.tiingo.com/tiingo/daily/{position}/prices?startDate={early_day}&endDate={today}&format=json&resampleFreq=daily',
                 headers=headers)
    historical_data_json= historical_data.json()

    five = historical_data_json[0]['close']
    four = historical_data_json[1]['close']
    three = historical_data_json[2]['close']
    two = historical_data_json[3]['close']
    one = historical_data_json[4]['close']

    return render(request, 'customers/stock_details.html',{'position': position, 'historical_data_json': historical_data_json, 'five': five, 'four': four, 'three': three, 'two': two, 'one': one})

def update_all(request):

    return render(request, 'customers/index.html')
