from django.db import models
from django.conf import settings

class JobPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    wage = models.DecimalField(max_digits=10, decimal_places=2)
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'employer'},
        related_name='job_posts',
        null=True,
        blank=True
    )
    availability_start = models.DateTimeField(null=True, blank=True)
    availability_end = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    job_type = models.CharField(max_length=50) 
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
class JobApplication(models.Model):
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    job = models.ForeignKey(
        JobPost,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )

    class Meta:
        unique_together = ('applicant', 'job')

    def __str__(self):
        return f"{self.applicant} → {self.job.title}"

