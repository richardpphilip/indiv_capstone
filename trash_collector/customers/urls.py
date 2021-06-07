from django.urls import path

from . import views

app_name = "customers"
urlpatterns = [
    path('', views.index, name="index"),
    path('stocks/', views.apicall, name="stock"),
    path('add', views.apicall, name='add'),
    path('stock_details/<int:position_id>/', views.stock_details, name='stock_details'),
]
