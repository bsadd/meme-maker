import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class User(AbstractUser):
	"""User's login credential entity for any system user"""

	backend = 'django.contrib.auth.backends.ModelBackend'

	is_suspended = models.BooleanField('Suspended Account', default=False)

	class Meta:
		verbose_name = "User"
		verbose_name_plural = "Users"

	def get_rating(self):
		rating = 0
		# if self.is_customer:
		# 	from customer.utils_db import get_avg_customer_rating
		# 	rating = get_avg_customer_rating(self.id)
		# elif self.is_delivery_man:
		# 	from delivery.utils_db import get_avg_deliveryman_rating
		# 	rating = get_avg_deliveryman_rating(self.id)
		# elif self.is_manager:
		# 	rating = self.restaurant.get_avg_rating()
		# elif self.is_branch_manager:
		# 	rating = self.restaurantbranch.get_avg_rating()
		# if rating is None:
		# 	rating = 0
		return round(rating, 2)

	def get_image(self):
		# if self.is_customer:
		# 	return self.userprofile.avatar
		# if self.is_manager:
		# 	return self.restaurant.get_image()
		# if self.is_branch_manager:
		# 	return self.restaurantbranch.get_image()
		return 'default.png'

	def send_mail(self, subject, message, from_email='admin@foodsquare'):
		print('sending mail to', self)
		import django.core.mail
		django.core.mail.send_mail(
			subject=subject,
			message='Username:' + self.username + '\n ' + 'Email:' + self.email + '\n ' + message,
			from_email=from_email,
			recipient_list=[self.email],
			fail_silently=False,
		)

#
# class UserProfile(models.Model):
# 	"""Customer profile entity"""
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	first_name = models.CharField(max_length=20, null=True)
# 	last_name = models.CharField(max_length=20, null=True)
# 	address = models.TextField(max_length=150, null=True)
# 	avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
#
# 	def __str__(self):
# 		return str(self.first_name or None) + str(self.last_name or None) + self.user.username + " " + str(
# 			self.address or None) + str(self.avatar.url)
#
