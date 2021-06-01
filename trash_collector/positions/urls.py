from django.urls import path

from . import views

app_name = 'positions'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.create, name='add_stock')
]
