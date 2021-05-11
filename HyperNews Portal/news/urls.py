from django.urls import path
from .views import hello, news, index, create

urlpatterns = [
    path('', hello, name='hello'),
    path('news/', index, name='home'),
    path('news/<int:link>/', news, name='news-detail'),
    path('news/create/', create, name='create'),
]