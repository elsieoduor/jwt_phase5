from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Admin(AbstractUser):
  name= models.CharField(max_length=20)
  email = models.EmailField(unique=True)
  password= models.CharField(max_length=20)
  username= None

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []
