from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager,PermissionsMixin
import datetime

# Create your models here.

class UserManager(BaseUserManager):
  """
  Custom Django User Manager for the Custom User Model Created.
  """
  def create_user(self, email, first_name, last_name, date_of_birth, password=None, **kwargs):
      if not email:
          raise ValueError("Email not provided")

      user = self.model(
          email = self.normalize_email(email),
          first_name = first_name,
          last_name = last_name,
          date_of_birth = date_of_birth,
          **kwargs
      )
      user.set_password(password) #hashing and storing the password
      user.save(using = self._db) #saving the user with the database.
      return user

  def create_superuser(self, email, first_name, last_name, date_of_birth, password=None, **kwargs):
      user = self.create_user(
          email=email,
          password=password,
          first_name = first_name,
          last_name = last_name,
          date_of_birth = date_of_birth,
      )
      user.is_admin = True
      user.is_staff = True
      user.is_superuser = True
      user.save(using=self._db)
      return user


class User(AbstractBaseUser,PermissionsMixin):
  """
  Custom Django User Model without Username.
  """
  id = models.AutoField(primary_key=True)
  email = models.EmailField(null=False, max_length=255,unique=True)
  first_name = models.CharField(null=False, max_length=100)
  last_name = models.CharField(null=False, max_length=100)
  date_of_birth = models.DateField(null=False)
  date_joined = models.DateTimeField(auto_now=True)

  is_admin = models.BooleanField(default = False)
  is_active = models.BooleanField(default = True)
  is_staff = models.BooleanField(default = False)
  is_superuser = models.BooleanField(default = False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name','first_name', 'last_name', 'date_of_birth']

  objects = UserManager()

  def __str__(self):
      return self.first_name + " " + self.last_name

  def age(self):
      return int((datetime.date.today() - self.date_of_birth).days / 365.25)