from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, password2=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#custome user
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(unique=True, max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

class Project_db(models.Model):
    emp = models.ManyToManyField(User)
    id = models.IntegerField(primary_key = True, auto_created=True)
    project_name =  models.CharField(max_length=200,default=False)
    project_pricing =  models.CharField(max_length=200,default=False)
    inventory =  models.CharField(max_length=200,default=False)
    working_status =  models.CharField(max_length=200,default=False)
    project_description  = models.CharField(max_length=200,default=False)


class Parts_db(models.Model):
    id = models.IntegerField(primary_key = True)
    part_name = models.CharField(max_length=200,default=False)
    projet_id = models.ForeignKey(Project_db, on_delete=models.CASCADE)


class Task_db(models.Model):
    id = models.IntegerField(primary_key = True)
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    projet_id = models.ForeignKey(Project_db, on_delete=models.CASCADE)
    parts_id =  models.ForeignKey(Parts_db, on_delete=models.CASCADE)
    parts_quantity = models.IntegerField(max_length=200,default=False)
    opretions = models.CharField(max_length=200,default=False)

 
class Timesheet_db(models.Model):
    # id = models.IntegerField(primary_key = True)
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    projet_id = models.ForeignKey(Project_db, on_delete=models.CASCADE)
    parts_id =  models.ForeignKey(Parts_db, on_delete=models.CASCADE)
    task_id =  models.ForeignKey(Task_db, on_delete=models.CASCADE)
    hours_for_the_day =  models.CharField(max_length=200,default=False)
    check_in =models.BooleanField(default=False)
    check_in_time = models.DateTimeField(blank=True, null=True)
    check_out = models.BooleanField(default=False)
    check_out_time = models.DateTimeField(blank=True, null=True)
