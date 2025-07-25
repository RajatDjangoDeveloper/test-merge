from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class RoleTable(models.Model):
    name = models.CharField(max_length=225)
    role = models.CharField(max_length=225)
    create_dt = models.DateField(auto_now=True)
    create_by = models.CharField(max_length=225, null=True)
    is_approve = models.BooleanField(default=False)
# Mobile Users


class UserManager(BaseUserManager):
    def create_user(self, email_address, password=None):
        """
            Creates and saves a User with the given email and password.
        """
        if not email_address:
            raise ValueError('Users must have an email address')

        user = self.model(
            email_address=self.normalize_email(email_address),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, password):
        """
            Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email_address,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, null=True)
    email_address = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    create_dt = models.DateTimeField(auto_now_add=True)
    role_fields =models.ForeignKey(RoleTable, on_delete=models.CASCADE, null=True)
    # forigen_created =models.ForeignKey(RoleTable, on_delete=models.CASCADE, null=True)
    
    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = UserManager()

    class Meta:
        db_table = 'user'



class DeviceType(models.Model):
    device_type = models.CharField(max_length=225)
    create_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    create_by = models.CharField(max_length=225, null=True)
    is_approve = models.BooleanField(default=False)

class Location(models.Model):
    location = models.CharField(max_length=225)
    create_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    create_by = models.CharField(max_length=225, null=True)
    is_approve = models.BooleanField(default=False)


class Department(models.Model):
    department_name =models.CharField(max_length=225)
    create_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)

class Designation(models.Model):
    designation_name_www= models.CharField(max_length=225) #field changed to  in UI =>designation job_title
    create_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)
    create_by = models.CharField(max_length=225, null=True)
    is_approve = models.BooleanField(default=False)


class EmployeesData(models.Model):
    Emp_ID = models.CharField(max_length=225,unique=True)
    emp_name = models.CharField(max_length=225)
    emp_email = models.EmailField(max_length=255, unique=True)
    department_fk = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    designation_name = models.CharField(max_length=225)
    manager = models.CharField(max_length=225)
    create_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)
    # group = models.CharField(max_length=225,null=True)
    # emp_type = models.CharField(max_length=225, null=True)
    # location_id = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

class Device(models.Model):
    device_type_name = models.ForeignKey(DeviceType, on_delete=models.CASCADE, null=True)
    service_tag = models.CharField(max_length=225)
    brand = models.CharField(max_length=225)
    model_no = models.CharField(max_length=225)
    model_name = models.CharField(max_length=225)
    ram = models.CharField(max_length=225)
    memory = models.CharField(max_length=225)
    location_name = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    assignee = models.CharField(max_length=225, null=True)
    additional_comment = models.TextField(null=True)
    create_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now=True, null=True)
    create_by = models.CharField(max_length=225, null=True)
    is_approve = models.BooleanField(default=False)
