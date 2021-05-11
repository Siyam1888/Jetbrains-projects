from django.shortcuts import render, redirect
from django.views import View
from .models import Vacancy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class VacancyListView(View):
    def get(self, request, *args, **kwargs):
        vacancy_list = Vacancy.objects.all()
        context = {'vacancies': vacancy_list}
        print(context)
        return render(request, 'vacancy/vacancy_list.html', context=context)


class VacancyCreate(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'vacancy/vacancy_create.html')

    def post(self, request, *args, **kwargs):
        user = request.user
        description = request.POST.get('description')
        vacancy = Vacancy.objects.create(description=description, author=user)
        return redirect('/')

    def test_func(self):
        return self.request.user.is_staff
