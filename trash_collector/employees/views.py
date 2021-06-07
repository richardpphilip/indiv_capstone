from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
from django.apps import apps
import smtplib
from email.message import EmailMessage
import datetime


# Create your views here.
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token faadb088abbd151884296572be6b19d0321922b3'
}
from django.urls import reverse




def index(request):
    Customer = apps.get_model('customers.Customer')

    return render(request, 'employees/index.html')


def send_email(request):
    Account = apps.get_model('accounts.User')
    users = Account.objects.all()
    Position = apps.get_model('positions.Position')
    positions = Position.objects.all()
    today = datetime.date.today()

    for user in users:
        position_list = []
        stock_news_list = []
        stock_email_list_string = ''
        stock_email_price_string = ''
        stock_news_url = []
        close_value_list = []
        stock_name_list = []

        for position in positions:
            if position.user_id == user.id:
                position_list.append(position)
                stock_news = requests.get(f'https://api.tiingo.com/tiingo/news?tickers={position}',
                                          headers=headers)
                stock_news_json = stock_news.json()

                price_json = requests.get(f'https://api.tiingo.com/tiingo/daily/{position}/prices',
                                          headers=headers)
                stock_info = price_json.json()
                meta_json = requests.get(f'https://api.tiingo.com/tiingo/daily/{position}',
                                         headers=headers)
                stock_meta = meta_json.json()
                stock_email_list_string += "Update for Stock:"
                stock_email_list_string += stock_meta['name']
                stock_email_list_string += "-"
                stock_email_list_string += f"The price of the Stock as of {today} is:  $"
                stock_email_price_string = str(stock_info[0]['close'])
                stock_email_list_string += stock_email_price_string
                stock_email_list_string += "-"
                stock_email_list_string += "A snippet of news I think you might find helpful is:"
                stock_email_list_string += stock_news_json[0]['description']
                stock_email_list_string += "-"
                stock_email_list_string += "If you want to read more this is the link:"
                stock_email_list_string += stock_news_json[0]['url'] + " "
                stock_email_list_string += f"---------END OF {position} -------------"
        EMAIL_ADDRESS = 'stock.tracker.philip@gmail.com'
        EMAIL_PASSWORD = 'NickMangold74!'
        print(stock_email_list_string)
        msg = EmailMessage()

        msg['Subject'] = f'Stock Update {user.username} for {today}'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = f'{user.email}'
        msg.set_content(stock_email_list_string)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    return HttpResponseRedirect(reverse('employees:index'))

