from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.base import View

#
# def recoveryRender(request):
# 	return HttpResponse("Enter email to recover !!!")
#
#
# def homepageRender(request):
# 	return render(request, USER_DASHBOARD_PAGE)
from accounts.forms import UserForm


# from geopy.geocoders import Nominatim
# from accounts.account_links import *
# from accounts.models import *
# from accounts.utils import *
# from .forms import UserForm
# geolocator = Nominatim(user_agent="foodsquare")


class LoginView(TemplateView):
	template_name = 'accounts/Registration.html'

	def get(self, request, *args, **kwargs):
		# if self.request.user.is_authenticated:
		# 	return redirect('/')
		# else:
		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = {'loggedIn': self.request.user.is_authenticated}
		return ctx

	def post(self, request, *args, **kwargs):
		# print(pretty_request(request))
		username = request.POST.get('username', False)
		password = request.POST.get('pass', False)
		if username and password:
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				print('Signing in: ' + str(request.user))
				return redirect('/')
			elif user is None:
				return render(request, 'accounts/message_page.html',
				              {'header': "Error !", 'details': 'Invalid Username or Password',
				               'redirect': reverse('accounts:login')})
		# return JsonResponse({'account': False})
		# elif not user.is_customer:
		# 	return render(request, 'accounts/message_page.html',
		# 	              {'header': "Error !", 'details': 'Not a Customer account',
		# 	               'redirect': reverse('accounts:login')})
		# return JsonResponse({'account': True, 'customer': False})
		else:
			return render(request, 'accounts/message_page.html',
			              {'header': "Error !", 'details': 'Username or password is empty',
			               'redirect': reverse('accounts:login')})


class RegisterView(TemplateView):
	template_name = 'accounts/colorlib-regform-7.html'

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/')
		else:
			return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = super(RegisterView, self).get_context_data(**kwargs)
		# ctx['user_form'] = UserForm(prefix='user')
		# ctx['profile_form'] = ProfileForm(prefix='profile')
		ctx = {'loggedIn': self.request.user.is_authenticated}
		return ctx

	def post(self, request, *args, **kwargs):
		# print(pretty_request(request))

		user_form = UserForm(request.POST)

		if user_form.is_valid():
			user = user_form.save(commit=False)
			user.is_customer = True
			user.save()
			# p = UserProfile.objects.create(user=user)
			# p.save()
			print('Registering : ' + str(request.user))
			login(request, user)
			return redirect('/')
		else:
			# return render(request, 'accounts/message_page.html',
			#               {'header': "Error !", 'details': ' signup'})
			return HttpResponse("Error ! signup")


class LogoutView(View, LoginRequiredMixin):
	def get(self, request):
		print('Signing out: ' + str(request.user))
		logout(request)
		return redirect('/')


class SignupLoginView(TemplateView):
	template_name = 'accounts/Registration.html'

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/')
		else:
			return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = super(SignupLoginView, self).get_context_data(**kwargs)
		# ctx['user_form'] = UserForm(prefix='user')
		# ctx['profile_form'] = ProfileForm(prefix='profile')
		ctx = {'loggedIn': self.request.user.is_authenticated}
		return ctx

	def post(self, request, *args, **kwargs):
		# print(pretty_request(request))
		formName = request.POST.get('formName', False)
		print(formName)

		if formName == 'LOGIN':
			username = request.POST.get('log-username', False)
			password = request.POST.get('log-password', False)
			if username and password:
				user = authenticate(request, username=username, password=password)
				if user is not None:
					login(request, user)
					print('Signing in: ' + str(request.user))
					return redirect('/')
				elif user is None:
					return render(request, 'accounts/message_page.html',
					              {'header': "Error !", 'details': 'Invalid Username or Password',
					               'redirect': reverse('accounts:login')})

			else:
				return render(request, 'accounts/message_page.html',
				              {'header': "Error !", 'details': 'Username or password is empty',
				               'redirect': reverse('accounts:login')})

		else:
			user_form = UserForm(request.POST)

			if user_form.is_valid():
				user = user_form.save(commit=False)
				user.is_customer = True
				user.save()
				# p = UserProfile.objects.create(user=user)
				# p.save()
				print('Registering : ' + str(request.user))
				login(request, user)
				return redirect('/')
			else:
				# return render(request, 'accounts/message_page.html',
				#               {'header': "Error !", 'details': ' signup'})
				return HttpResponse("Error ! signup")
