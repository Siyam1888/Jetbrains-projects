from django.urls import path
from . views import VacancyListView, VacancyCreate

urlpatterns = [
    path('', VacancyListView.as_view(), name='vacancies'),
    path('/new', VacancyCreate.as_view(), name='new_vacancy'),
]