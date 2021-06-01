from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the customer user stories, add a path for each in urlpatterns

app_name = "customers"
urlpatterns = [
    path('', views.index, name="index"),
    path('stocks/', views.apicall, name="stock"),
    path('add', views.apicall, name='add'),
    path('stock_details/<int:position_id>/', views.stock_details, name='stock_details')
]
