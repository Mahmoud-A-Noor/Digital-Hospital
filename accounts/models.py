from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid


def get_random_code():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return str(code)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, date_of_birth, gender, user_type, phone_number, password, img=None, address=None):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            user_type=user_type,
            phone_number=phone_number,
            img=img,
            address=address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, date_of_birth, gender, user_type, password, phone_number, img=None, address=None):
        user = self.create_user(email, first_name, last_name, date_of_birth, gender, user_type, phone_number, password, img=img, address=address)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('pharmacist', 'Pharmacist'),
        ('manager', 'Manager'),
    )

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=100, unique=True, blank=True)
    date_of_birth = models.DateField()
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True, unique=False)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
    img = models.ImageField(upload_to='images/', blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'gender', 'user_type', 'phone_number']

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.username = self.generate_unique_username(slugify(self.first_name + ' ' + self.last_name))
        super().save(*args, **kwargs)

    def generate_unique_username(self, username):
        existing_user = CustomUser.objects.filter(username=username).exists()
        if not existing_user:
            return username
        
        new_username = username
        while CustomUser.objects.filter(username=new_username).exists():
            new_username = slugify(username + ' ' + get_random_code())
        
        return new_username