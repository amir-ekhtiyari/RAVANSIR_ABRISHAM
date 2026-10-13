from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('routes/', views.routes, name='routes'),
    path('about/', views.about, name='about'),
]
