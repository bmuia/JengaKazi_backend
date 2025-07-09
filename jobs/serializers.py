from rest_framework import serializers
from .models import JobPost,JobApplication



class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model =JobPost
        fields = ['id','title','description','location','wage','employer','availability_start','availability_end','created_at']
        read_only_fields = ['id','created_at']


class JobApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.get_full_name', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'job_title', 'applicant_name', 'applied_at', 'status']
        read_only_fields = ['id', 'job_title', 'applicant_name', 'applied_at', 'status']


