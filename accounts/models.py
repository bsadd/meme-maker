import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User's login credential entity for any system user"""

    backend = 'django.contrib.auth.backends.ModelBackend'

    is_moderator = models.BooleanField('Moderator Account', default=False)
    is_suspended = models.BooleanField('Suspended Account', default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_rating(self):
        rating = 0
        return round(rating, 2)

    def get_image(self):
        return self.socialaccount_set.all[0].get_avatar_url  # 'default.png'

    def send_mail(self, subject, message, from_email='admin@mememaker'):
        print('sending mail to', self)
        import django.core.mail
        django.core.mail.send_mail(
            subject=subject,
            message='Username:' + self.username + '\n ' + 'Email:' + self.email + '\n ' + message,
            from_email=from_email,
            recipient_list=[self.email],
            fail_silently=False,
        )
