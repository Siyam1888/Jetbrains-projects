from django.shortcuts import render, redirect
from django.views import View
from .models import Resume
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class ResumeListView(View):
    def get(self, request, *args, **kwargs):
        resume_list = Resume.objects.all()
        context = {'resumes': resume_list}
        return render(request, 'resume/resume_list.html', context=context)


class CreateResume(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'resume/resume_create.html')

    def post(self, request):
        user = request.user
        description = request.POST.get("description")
        resume = Resume(author=user, description=description)
        resume.save()
        return redirect("/")













