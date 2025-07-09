from django.shortcuts import render
from .serializers import JobSerializer
from users.permisssions import IsEmployer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import JobPost

class JobListCreateView(generics.ListCreateAPIView):
    """
    GET: Public - List all job posts
    POST: Employer-only - Create a new job post
    """
    queryset = JobPost.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsEmployer()]
        return [AllowAny()]


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Public - View a job post
    PUT/PATCH/DELETE: Employer-only - Update or delete their own job post
    """
    queryset = JobPost.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsEmployer()]
