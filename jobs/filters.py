import django_filters
from .models import JobPost

class JobPostFilter(django_filters.FilterSet):
    min_wage = django_filters.NumberFilter(field_name="wage", lookup_expr="gte")
    max_wage = django_filters.NumberFilter(field_name="wage", lookup_expr="lte")
    location = django_filters.CharFilter(field_name="location", lookup_expr="icontains")
    job_type = django_filters.CharFilter(field_name="job_type", lookup_expr="iexact")
    is_active = django_filters.BooleanFilter(field_name="is_active")

    class Meta:
        model = JobPost
        fields = ['location', 'job_type', 'is_active', 'min_wage', 'max_wage']
