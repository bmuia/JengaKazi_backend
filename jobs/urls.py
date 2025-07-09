from django.urls import path
from .views import (
    JobListCreateView,
    JobDetailView,
    JobListView,
    JobApplicationCreateView,
    JobApplicantListView,
)

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('feed/jobs/', JobListView.as_view(), name='job-feed'),
    path('jobs/<int:job_id>/apply/', JobApplicationCreateView.as_view(), name='apply-to-job'),
    path('jobs/<int:job_id>/applicants/', JobApplicantListView.as_view(), name='job-applicants'),
]
