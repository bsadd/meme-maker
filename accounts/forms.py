from django import forms
from django.forms.models import ModelForm

from accounts.models import User
# from .models import UserProfile


# class ProfileForm(ModelForm):
# 	class Meta:
# 		model = UserProfile
# 		fields = ('first_name', 'last_name', 'avatar', 'address')


class UserForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'password', 'email')

	def save(self, commit=True):
		new_user = User.objects.create_user(username=self.cleaned_data['username'],
		                                    email=self.cleaned_data['email'],
		                                    password=self.cleaned_data['password'])
		try:
			new_user.first_name = self.cleaned_data['first_name']
			new_user.last_name = self.cleaned_data['last_name']
		except Exception:
			pass
		if commit:
			new_user.save()
		return new_user
