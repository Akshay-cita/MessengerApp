from django.db import models

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class MyAccountManager(BaseUserManager):
	def create_user(self,email,username,password=None):
		if not email:
			raise ValueError("User Must have a email address")
		if not username:
			raise ValueError("User must have Username")
		user=self.model(
				email=self.normalize_email(email),
				username=username,

			)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,email,username,password):
		user=self.create_user(
				email=self.normalize_email(email),
				username=username
				password=password
			)
		user.is_admin=True
		user.is_staff=True
		user.is_superuser=True
		user.save(using=self._db)
		return user

		

class Account(AbstractBaseUser):

	email=models.EmailField(verbose_name="email",max_length=60,unique=True)
	username=models.CharField(max_length=30,unique=True)
	date_joined=models.DateTimeField(verbose_name="date_joined",auto_now=True)
	last_login=models.DateTimeField(verbose_name="last_login",auto_now=True)
	is_admin=models.BooleanField(default=False)
	is_active=models.BooleanField(default=False)
	is_staff=models.BooleanField(default=False)
	is_superuser=models.BooleanField(default=False)

	profile_image=models.ImageField(max_length=255,upload_to='profile_pic/',null=True,blank=True,default='profile_pic/default.png')
	hide_email=models.BooleanField(default=True)
	USERNAME_FIELD='email'
	REQUIRED_FIELDS=['username']

	def __str__(self):
		return self.username

	def has_perms(self,perm,obj=None):
		return self.is_admin

	def has_module_perms(self,app_label):
		return True

