from django.urls import path

from myapp import views

urlpatterns = [
    path('index/', views.index, name=''),
    path('', views.new, name='index'),
    path('confirm/', views.confirm, name='confirm'),
    path('delete/', views.delete, name='delete'),
    path('news/', views.news, name='news')
]