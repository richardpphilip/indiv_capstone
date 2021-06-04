from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
from django.apps import apps
import smtplib

# Create your views here.
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token faadb088abbd151884296572be6b19d0321922b3'
}
from django.urls import reverse

EMAIL_ADDRESS = 'stock.tracker.philip@gmail.com'
EMAIL_PASSWORD = 'NickMangold74!'


def index(request):
    # Get the Customer model from the other app, it can now be used to query the db
    Customer = apps.get_model('customers.Customer')

    return render(request, 'employees/index.html')


def send_email(request):
    Account = apps.get_model('accounts.User')
    users = Account.objects.all()
    Position = apps.get_model('positions.Position')
    positions = Position.objects.all()

    for user in users:
        position_list = []
        stock_news_list = []
        stock_news_url = []
        close_value_list = []
        stock_name_list = []


        for position in positions:
            if position.user_id == user.id:
                position_list.append(position)
                stock_news = requests.get(f'https://api.tiingo.com/tiingo/news?tickers={position}',
                                          headers=headers)
                stock_news_json = stock_news.json()
                stock_news_list.append(stock_news_json[0]['description'])
                stock_news_url.append(stock_news_json[0]['url'])
                price_json = requests.get(f'https://api.tiingo.com/tiingo/daily/{position}/prices',
                                          headers=headers)
                stock_info = price_json.json()
                close_value_list.append(stock_info[0]['close'])
                meta_json = requests.get(f'https://api.tiingo.com/tiingo/daily/{position}',
                                         headers=headers)
                stock_meta = meta_json.json()
                stock_name_list.append(stock_meta['name'])
        print(user.username)
        print(stock_name_list)
        print(position_list)
        print(stock_news_list)
        print(close_value_list)



            # with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            #     smtp.ehlo()
            #     smtp.starttls()
            #     smtp.ehlo()
            #     smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            #     subject = f'{stock_name} Stock Update'
            #     body = f' The closing value for {position} was ${close_value} yesterday.'
            #     msg = f'Subject:{subject}\n\n{body}'
            #     smtp.sendmail(EMAIL_ADDRESS, f'{user.email}', msg)
    return HttpResponseRedirect(reverse('employees:index'))

    # Customer = apps.get_model('customers.Customer')
    # customers = Customer.objects.all()
    # for customer in customers:
    #     customer.e
