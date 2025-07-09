from rest_framework import serializers
from .models import JobPost


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model =JobPost
        fields = ['id','title','description','location','wage','employer','availability_start','availability_end','created_at']
        read_only_fields = ['id','created_at']