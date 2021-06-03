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
        for position in positions:
            if user.id == position.user_id and user.is_employee == False:
                # stock_news = requests.get(f'https://api.tiingo.com/tiingo/news?tickers=aapl',
                #                           headers=headers)
                # stock_news_json = stock_news.json()
                price_json = requests.get(f'https://api.tiingo.com/tiingo/daily/{position}/prices',
                                          headers=headers)
                stock_info = price_json.json()
                close_value = stock_info[0]['close']
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    subject = f'{position} Stock Update'
                    body = f' The closing value for {position} was ${close_value} yesterday.'
                    msg = f'Subject:{subject}\n\n{body}'
                    smtp.sendmail(EMAIL_ADDRESS, f'{user.email}', msg)
            else:
                print(user.first_name)
    return HttpResponseRedirect(reverse('employees:index'))

    # Customer = apps.get_model('customers.Customer')
    # customers = Customer.objects.all()
    # for customer in customers:
    #     customer.e
