import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from accounts.models import *
from browse.forms import PostForm
from browse.models import *


# from browse.utils import *
# from browse.utils_db import *


class Index(TemplateView):
	"""
	Renders Home Page
	"""
	template_name = 'browse/index.html'

	def get_context_data(self, **kwargs):
		# with open("sessionLog.txt", "a") as myfile:
		# 	myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")

		ctx = {'loggedIn': self.request.user.is_authenticated
		       # 'restaurant_list': Restaurant.objects.all(),
		       # 'item_list': pkg_list[:3], 'restaurants': rest_list[0:4]
		       }
		return ctx


#
#
# class OrderView(TemplateView):
# 	"""View to render Cuisines List"""
# 	template_name = 'browse/order.html'
#
# 	def get_context_data(self, **kwargs):
# 		with open("sessionLog.txt", "a") as myfile:
# 			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
# 		entry_name = self.request.GET.get('menu_search')
# 		price_range = self.request.GET.get('range')
# 		pkg_list = Package.objects.all()
# 		if entry_name is not None:
# 			minprice = (float(str(price_range).split('-')[0].strip()[1:]))
# 			maxprice = (float(str(price_range).split('-')[1].strip()[1:]))
# 			queryset2 = [ingobj.package for ingobj in
# 						 IngredientList.objects.filter(ingredient__name__icontains=entry_name)]
# 			# queryset2 = Package.objects.raw(" Select * from browse_package where ")
# 			queryset1 = Package.objects.filter(
# 				Q(pkg_name__icontains=entry_name) & Q(price__range=(minprice, maxprice))
# 			)
# 			result_list = list(dict.fromkeys(list(queryset1) + queryset2))
# 			result_list.sort(key=lambda x: x.pkg_name, reverse=False)
# 			filtered_result = []
# 			for x in result_list:
# 				if minprice <= x.price <= maxprice:
# 					filtered_result.append(x)
# 			pkg_list = filtered_result
# 		page = self.request.GET.get('page')
#
# 		ctx = {'loggedIn': self.request.user.is_authenticated, 'item_list': get_page_objects(pkg_list, page),
# 			   'rating': range(5),
# 			   'categories': [c['category'] for c in Package.objects.all().values('category').distinct()]}
# 		return ctx
#
#
# class PackageDetails(TemplateView):
# 	"""View to render Details Page for a cuisine"""
# 	template_name = 'browse/item.html'
#
# 	def get(self, request, *args, **kwargs):
# 		if kwargs.get('id') is None or not isinstance(kwargs['id'], int):
# 			return redirect('/order/')
# 		return super().get(request, *args, **kwargs)
#
# 	def get_context_data(self, **kwargs):
# 		with open("sessionLog.txt", "a") as myfile:
# 			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
# 		id = kwargs['id']
# 		pkg = Package.objects.get(id=id)
# 		ing_list = [ingobj.ingredient.name for ingobj in IngredientList.objects.filter(package=pkg)]
#
# 		user_id = self.request.user.id if self.request.user.is_authenticated else 0
# 		comments = get_reviews_package(user_id, id)
# 		user_rating = None
# 		if self.request.user.is_authenticated and PackageRating.objects.filter(user=self.request.user,
# 																			   package=pkg).exists():
# 			user_rating = PackageRating.objects.get(user=self.request.user, package=pkg)
# 		print(get_rating_count_package(id))
# 		ctx = {'loggedIn': self.request.user.is_authenticated, 'item': pkg, 'item_img': [pkg.image],
# 			   'ing_list': ing_list, 'comments': comments, 'ratings': get_rating_count_package(id),
# 			   'avg_rating': get_rating_package(id)
# 			, 'user_rating': user_rating}
# 		return ctx
#
#
# class RestaurantList(TemplateView):
# 	"""
# 	View to renders list of branches in 4km radius
# 	If no such branch is in radius then None
# 	Assuming, a restaurant with null key cannot have any branch
# 	"""
# 	template_name = 'browse/restaurants.html'
#
# 	def get_context_data(self, **kwargs):
# 		print(pretty_request(self.request))
# 		with open("sessionLog.txt", "a") as myfile:
# 			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
#
# 		query = self.request.GET.get('searchBy_dish_food')
# 		coord = self.request.GET.get('delivery_area_srch')
# 		show = self.request.GET.get('show')
#
# 		if query is None:
# 			query = ''
#
# 		if coord is None or not coord:
# 			show = 'all'
# 		elif coord is not None and show is None:
# 			show = 'near_me'
# 			print(' @ ' + coord)
#
# 		qset = RestaurantBranch.objects.filter(
# 			Q(branch_name__icontains=query) | Q(restaurant__restaurant_name__icontains=query) | Q(
# 				restaurant__package__category__icontains=query)).distinct()
# 		if show == 'all':
# 			rest_list = frozenset(x.restaurant for x in qset)
# 			rest_list = [RestBranch(x) for x in rest_list]
# 		else:
# 			rest_list = branchesInRadius(coord=coord, queryset=qset)
# 		print(rest_list)
# 		ctx = {'loggedIn': self.request.user.is_authenticated, 'restaurants': rest_list,
# 			   'show_all': (show == 'all'), 'query': query}
# 		return ctx
#
#
#
# class RestaurantDetails(TemplateView):
# 	"""
# 	Renders a Restaurant's Home Page with list of packages it currently has
# 	"""
#
# 	template_name = 'browse/restaurant_home.html'
#
# 	def get_context_data(self, **kwargs):
# 		with open("sessionLog.txt", "a") as myfile:
# 			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
#
# 		rest = Restaurant.objects.get(id=kwargs['id'])
#
# 		pkg_list = Package.objects.filter(restaurant__id=rest.id)
#
# 		categories = set([item.category for item in pkg_list])
# 		# print(pkg_list)
# 		branch_list = RestaurantBranch.objects.filter(restaurant__id=kwargs['id'])
#
# 		ctx = {'loggedIn': self.request.user.is_authenticated, 'item_list': pkg_list, 'categories': categories,
# 			   'restaurant': RestBranch(restaurant=rest, branch=None), 'rating': get_rating_restaurant(kwargs['id']),
# 			   'branch_list': branch_list}
# 		return ctx
#
#
# def reactSubmit(request, id):
# 	"""
# 	updates like/dislike count for user react on any post
# 	:return: updated like,dislike count for that post
# 	"""
# 	print(request)
# 	if not request.user.is_authenticated:
# 		return
# 	pkg_id = request.POST.get('pkg-id')
# 	branch_id = request.POST.get('branch-id')
# 	react = request.POST.get('react')
# 	post_id = request.POST.get('comment-id')
# 	nlike, ndislike = 0, 0
# 	user = request.user
# 	if pkg_id is not None:
# 		nlike, ndislike = post_comment_react_package(user, post_id, react)
#
# 	elif branch_id is not None:
# 		nlike, ndislike = post_comment_react_branch(user, post_id, react)
# 	print(pkg_id, " ", nlike, " ", ndislike)
# 	return JsonResponse({'nlikes': nlike, 'ndislikes': ndislike})
#
#
# def submitReview(request, id):
# 	"""Saves post for branch/package reviews"""
# 	pkg_id = request.POST.get('pkg-id')
# 	branch_id = request.POST.get('branch-id')
# 	comment = request.POST.get('comment')
# 	user = request.user
# 	print(branch_id, " ", comment, " ", user)
#
# 	if pkg_id is not None:
# 		post_comment_package(user, pkg_id, comment)
# 	elif branch_id is not None:
# 		post_comment_branch(user, branch_id, comment)
# 	return JsonResponse({'success': 'success'})
#
#
# def submitPackageRating(request, id):
# 	"""saves user rating for a cuisine"""
# 	pkg_id = request.POST.get('pkg-id')
# 	rating = request.POST.get('rating')
# 	user = request.user
# 	print(pkg_id, " ", rating, " ", user)
#
# 	post_rating_package(user, pkg_id, rating)
# 	return JsonResponse({'success': True})
#
#
# def FilteredProducts(request):
# 	"""
# 	Renders list of cuisines satisfying given filters
# 	:return: list of Package
# 	"""
# 	entry_name = request.GET.get('menu_name')
# 	price_range_min = request.GET.get('min_range')
# 	price_range_max = request.GET.get('max_range')
# 	rating = request.GET.get('rating')
# 	category = request.GET.get('category')
# 	only_offer = request.GET.get('offer_type')  # two value buy_get/ discount
#
# 	if not entry_name:
# 		entry_name = ''
# 	if not price_range_min:
# 		price_range_min = "0"
# 	if not price_range_max:
# 		price_range_max = "10000"
# 	pkg_list = get_named_package(entry_name)
# 	if rating and int(rating) != 0:
# 		pkg_list &= get_rated_package(int(rating))
# 	pkg_list &= get_price_range_package(float(price_range_min), float(price_range_max))
# 	if category is not None:
# 		pkg_list &= get_category_packages(category)
# 	print(pkg_list)
#
# 	page = request.GET.get('page')
# 	print(page, get_page_objects(pkg_list, page))
# 	return render(request, 'browse/product_list.html', {'item_list': get_page_objects(pkg_list, page)})
#
#
# def aboutSection(request):
# 	"""Renders About Page"""
# 	return render(request, 'browse/about.html')
#
#
# def contactSection(request):
# 	"""Renders Contact Page"""
# 	return render(request, 'browse/contact.html')
#


import re

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView


class AddMenuView(TemplateView):
	template_name = 'browse/memeUpload.html'

	def get(self, request, *args, **kwargs):
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(AddMenuView, self).get_context_data()
		# context['ingredient_list'] = Ingredient.objects.all()
		return context

	def post(self, request, *args, **kwargs):
		restaurant = User.objects.get(id=self.request.user.id).author
		print(request.POST)
		menu_form = PostForm(request.POST or None, request.FILES or None)
		ingrd_list = request.POST.getlist('ingrds')[0].split(',')
		print(menu_form)
		if menu_form.is_valid():
			menu = menu_form.save(commit=False)
			menu.author = restaurant
			print(menu)
			menu.save()
			for tmp in ingrd_list:
				tmp = " ".join(re.sub('[^a-zA-Z]+', ',', tmp.lower()).split(','))
				ingrd, created = Genre.objects.get_or_create(name=tmp.strip())
				GenreList.objects.create(package=menu, ingredient=ingrd)
			return render(request, 'manager/message_page.html',
			              {'header': "Done !", 'details': 'Menu added succcessfully'})

		else:
			return render(request, 'manager/message_page.html',
			              {'header': "Sorry !", 'details': 'Couldnot add up menu'})


class ViewMenusView(TemplateView):
	template_name = 'manager/manage_menus.html'

	def get_context_data(self, **kwargs):
		restaurant = User.objects.get(id=self.request.user.id).author
		obj_list = Post.objects.filter(restaurant=restaurant)  # .order_by('status', '-time')
		print(obj_list)
		print('-----')
		return {'menu_list': obj_list}


class ViewBranchMenusView(TemplateView):
	template_name = 'manager/manage_branchMenus.html'

	def get_context_data(self, **kwargs):
		return {'menu_list': get_packages_list_branch(self.request.user)}


def branch_pkg_details(request):
	return render(request, 'manager/branch_pkg_modal.html',
	              {'pkg': get_package_branch(request.user, request.GET.get('id'))})
