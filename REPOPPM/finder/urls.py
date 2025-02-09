from django.urls import path
from . import views 


urlpatterns = [
    path('', views.finder, name='search'),  # to searchbar.html
    path('result/', views.result, name='result'),  # to result.html
]
