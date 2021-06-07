from django.urls import path

from . import views

app_name = 'positions'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.create, name='add_stock'),
    path('update_all/', views.update_all, name='update_all'),
    path('edit/<int:position_id>/', views.edit, name='edit')

]
