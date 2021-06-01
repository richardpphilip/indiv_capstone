from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
from django.apps import apps
from .models import Position


# Create your views here.


def index(request):
    return render(request, 'positions/index.html')


def create(request):
    if request.method == 'POST':
        user = request.user
        selected_ticker = request.POST.get('selected_ticker')
        selected_value = request.POST.get('selected_value')
        new_position = Position(selected_ticker=selected_ticker, selected_value=selected_value, user_id=user.id)
        new_position.save()
        return HttpResponseRedirect(reverse('positions:index'))
    else:
        print('error')
        return HttpResponseRedirect(reverse('positions:index'))
