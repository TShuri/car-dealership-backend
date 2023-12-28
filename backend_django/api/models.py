# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Car(models.Model):
    id_car = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=30, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    model = models.CharField(max_length=30, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    color = models.CharField(max_length=20, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    engine = models.CharField(max_length=6, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)
    gearbox = models.CharField(max_length=4, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Car'


class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    phone = models.CharField(max_length=11, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    passport = models.CharField(max_length=10, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    email = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Client'


class Deal(models.Model):
    id_deal = models.AutoField(primary_key=True)
    id_car = models.ForeignKey(Car, models.DO_NOTHING, db_column='id_car', blank=True, null=True)
    id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='id_client', blank=True, null=True)
    id_employee = models.ForeignKey('Employee', models.DO_NOTHING, db_column='id_employee', blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Deal'


class Employee(models.Model):
    id_employee = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    post = models.CharField(max_length=20, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    salary = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    email = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Employee'


class Service(models.Model):
    id_service = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    id_car = models.ForeignKey(Car, models.DO_NOTHING, db_column='id_car', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Service'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS')
    name = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Names(models.Model):
    id = models.IntegerField(primary_key=True)
    man_first = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    man_second = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    man_third = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    woman_first = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    woman_second = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    woman_third = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')

    class Meta:
        managed = False
        db_table = 'names'

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
