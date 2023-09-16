from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator

class AppUserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		user = self.model(email=email)
		user.set_password(password)
		user.save()
		return user
	def create_superuser(self, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.create_user(email, password)
		user.is_superuser = True
		user.save()
		return user


class AppUser(AbstractBaseUser, PermissionsMixin):
	user_id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=50, unique=True)
	username = models.CharField(max_length=50)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	objects = AppUserManager()
	def __str__(self):
		return self.username
	
class building(models.Model):
		title = models.CharField(max_length=255)
		description = models.CharField(max_length=255)
		state = models.CharField(max_length=255, default= 'state')
		city = models.CharField(max_length=255 , default='city')
		price = models.DecimalField(max_digits=12, decimal_places=2)
		image = models.CharField(max_length=255)
		stars = models.IntegerField(
			validators=[MinValueValidator(0), MaxValueValidator(5)],
			default=5
		)
		bedrooms = models.IntegerField(
			default=1,
			validators=[MinValueValidator(1), MaxValueValidator(10)])
		bathrooms = models.IntegerField(
			default=1,
			validators=[MinValueValidator(1), MaxValueValidator(10)],)
		guests = models.IntegerField(
			default=1,
			validators=[MinValueValidator(1), MaxValueValidator(10)],)
		beds = models.IntegerField(
			default=1,
			validators=[MinValueValidator(1), MaxValueValidator(40)],)
		seller_name = models.CharField(max_length=255,default= 'john doe')
		seller_phone_number = models.IntegerField(default=12345678)
		seller_email = models.CharField(max_length=255, default='johndoe@email.com')
