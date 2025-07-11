from rest_framework import serializers
from .models import JobPost,JobApplication
from django.contrib.auth import get_user_model

User = get_user_model()


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model =JobPost
        fields = ['id','title','description','location','wage','employer','availability_start','availability_end','created_at']
        read_only_fields = ['id','created_at','employer']
class ApplicantSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return obj.get_full_name()


class JobApplicationSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer(read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'job_title', 'applicant', 'applied_at', 'status']
        read_only_fields = ['id', 'job_title', 'applicant_name', 'applied_at', 'status']


