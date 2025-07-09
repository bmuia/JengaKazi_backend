from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import JobSerializer,JobApplicationSerializer
from users.permisssions import IsEmployer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import JobPost,JobApplication
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobPostFilter

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
    
class JobListView(generics.ListAPIView):
    """
    Public job feed with filtering (location, wage, job type, etc.)
    """
    queryset = JobPost.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobPostFilter

class JobApplicationCreateView(generics.CreateAPIView):
    """
    Authenticated users (job seekers) can apply to a job
    """
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        job_id = kwargs.get('job_id')
        job = JobPost.objects.filter(id=job_id, is_active=True).first()

        if not job:
            return Response({"error": "Job not found or inactive."}, status=status.HTTP_404_NOT_FOUND)

        already_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
        if already_applied:
            return Response({"message": "You have already applied to this job."}, status=status.HTTP_400_BAD_REQUEST)

        application = JobApplication.objects.create(job=job, applicant=request.user)
        serializer = self.get_serializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class JobApplicantListView(generics.ListAPIView):
    """
    Employers can view all applicants who applied to their job
    """
    permission_classes = [IsEmployer]
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        job_id = self.kwargs.get('job_id')
        return JobApplication.objects.filter(
            job__id=job_id,
            job__employer=self.request.user
        ).order_by('-applied_at')

