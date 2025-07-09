from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class PhoneOtp(models.Model):
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number}"


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, otp=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(otp)
        user.save(using=self._db)
        return user

    def create_employer(self, phone_number=None, otp=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'employer')

        if phone_number and otp:
            user = self.model(phone_number=phone_number, **extra_fields)
            user.set_password(otp)
        elif email and password:
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
        else:
            raise ValueError("Provide either (phone_number and otp) OR (email and password) to create an employer.")

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        superuser = self.model(email=email, **extra_fields)
        superuser.set_password(password)
        superuser.save(using=self._db)
        return superuser


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
        ('admin', 'Admin'),
    ]

    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    bio = models.TextField()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []  # You can add 'email' if needed

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.phone_number or self.email} - {self.role}"
