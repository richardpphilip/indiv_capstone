from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
import smtplib

# Create your views here.
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
    for user in users:
        if not user.is_employee:
            print(user.email)
        else:
            pass
    return HttpResponseRedirect(reverse('employees:index'))

    # Customer = apps.get_model('customers.Customer')
    # customers = Customer.objects.all()
    # for customer in customers:
    #     customer.e

    # with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    #     smtp.ehlo()
    #     smtp.starttls()
    #     smtp.ehlo()
    #     smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    #     subject = 'Test'
    #     body = 'Test Test'
    #     msg = f'Subject:{subject}\n\n{body}'
    #     smtp.sendmail(EMAIL_ADDRESS,'richardpphilip1@gmail.com', msg)
