from django.views.generic import TemplateView

from browse import utils_db
from browse.models import *


class Index(TemplateView):
	"""
	Renders Home Page
	"""
	template_name = 'browse/index.html'

	def get_context_data(self, **kwargs):
		# with open("sessionLog.txt", "a") as myfile:
		# 	myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")

		ctx = {'loggedIn': self.request.user.is_authenticated,
		       # 'restaurant_list': Restaurant.objects.all(),
		       # 'item_list': pkg_list[:3], 'restaurants': rest_list[0:4]
		       'item_list': Post.objects.all()
		       }
		return ctx


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
# 	return render(request, 'browse/meme_list.html', {'item_list': get_page_objects(pkg_list, page)})
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


from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class AddMemeView(TemplateView):
	template_name = 'browse/memeUpload.html'

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('accounts:login')
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(AddMemeView, self).get_context_data()
		context['loggedIn'] = self.request.user.is_authenticated
		return context

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponse('Not logged in')

		print(pretty_request(self.request))
		# print(request.POST)
		genre_list = request.POST.getlist('keywords')[0].split(',')
		category = request.POST.get('category')
		caption = request.POST.get('caption')
		image = request.POST.get('image')
		if image is None or caption is None:
			return HttpResponse('Invalid data')

		utils_db.insert_post(user_id=self.request.user.id, image_base64=image, post_name=caption, category=category,
		                     genre_list=genre_list)
		return HttpResponse('Ok')




class ViewMenusView(TemplateView):
	template_name = 'manager/manage_menus.html'

	def get_context_data(self, **kwargs):
		obj_list = Post.objects.filter(author=self.request.user)  # .order_by('status', '-time')
		print(obj_list)
		print('-----')
		return {'loggedIn': self.request.user.is_authenticated, 'menu_list': obj_list}


def branch_pkg_details(request):
	return render(request, 'manager/branch_pkg_modal.html',
	              {'pkg': get_package_branch(request.user, request.GET.get('id'))})
