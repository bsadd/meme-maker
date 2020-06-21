import datetime

from allauth.socialaccount.models import SocialAccount
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

    @property
    def moderator_account(self):
        return not self.is_suspended and self.is_superuser or self.is_moderator

    @property
    def avatar(self):
        try:
            return self.socialaccount_set.all()[:1].get().get_avatar_url()
        except SocialAccount.DoesNotExist:
            return 'https://www.netclipart.com/pp/m/232-2329525_person-svg-shadow-default-profile-picture-png.png'

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
