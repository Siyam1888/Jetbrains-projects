from django.urls import path
from .views import (WelcomeView, MenuView,
                    GetTicketView, ProcessingView,
                    NextView)

urlpatterns = [
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('processing', ProcessingView.as_view(), name='processing'),
    path('next', NextView.as_view(), name='next'),
    path('get_ticket/<str:service>/', GetTicketView.as_view(), name='get_ticket')
]