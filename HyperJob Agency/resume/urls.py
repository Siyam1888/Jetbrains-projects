from django.urls import path
from .views import ResumeListView, CreateResume

urlpatterns = [
    path('', ResumeListView.as_view(), name='resumes'),
    path('/new', CreateResume.as_view(), name='new_resume'),
]