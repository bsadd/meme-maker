from collections import namedtuple

from django.db import connection

# ------------------ util functions --------------------------
from accounts.models import User
from browse.models import PostRating


def namedtuplefetchall(query, param_list):
	"""Return all rows from a cursor as a namedtuple"""
	with connection.cursor() as cursor:
		cursor.execute(query, param_list)
		desc = cursor.description
		nt_result = namedtuple('Result', [col[0] for col in desc])
		return [nt_result(*row) for row in cursor.fetchall()]


# ------------------- Review Ratings -------------------------


def get_rating_count_post(post_id):
	""":returns an array with index as rating-value and value as count"""
	results = namedtuplefetchall(
		'select rating, count(distinct user_id)\
		from browse_packagerating\
		where package_id = %s\
		group by rating', [post_id])
	ratings = [0, 0, 0, 0, 0, 0]
	for i in results:
		ratings[i.rating] = i.count
	return ratings


def get_rating_post(post_id):
	""":returns average rating of a post"""
	from django.db.models import Avg
	return float(PostRating.objects.filter(post__id=post_id).aggregate(Avg('rating'))['avg_rating'])


def get_reviews_post(user_id, post_id):
	"""returns list of comments as tuple (package_id, comment_id, user_name, user_id, rating, comment, time, nlikes, ndislikes)
	with current user @ top """
	results = namedtuplefetchall(
		'select comment.package_id,\
			comment.id                       as comment_id,\
			account.username                 as user_name,\
			account.id                       as user_id,\
			rate.rating,\
			comment.comment,\
			comment.time,\
			(select count(liked.user_id)\
			from browse_packagecommentreact liked\
			where liked.post_id = comment.id\
				and liked.liked = true)		 as nlikes,\
			(select count(disliked.user_id)\
			from browse_packagecommentreact disliked\
			where disliked.post_id = comment.id\
				and disliked.disliked = true) as ndislikes\
		from browse_packagecomment comment\
				left join browse_packagerating rate on rate.package_id = comment.package_id and\
													rate.user_id = comment.user_id\
				join accounts_user account on comment.user_id = account.id\
		where comment.user_id = %s and comment.package_id = %s\
		UNION\
		DISTINCT\
		select *\
		from (\
			select comment.package_id,\
				comment.id                       as comment_id,\
				account.username                 as user_name,\
				account.id                       as user_id,\
				rate.rating,\
				comment.comment,\
				comment.time,\
				(select count(liked.user_id)\
				from browse_packagecommentreact liked\
				where liked.post_id = comment.id\
					and liked.liked = true)		 as nlikes,\
				(select count(disliked.user_id)\
				from browse_packagecommentreact disliked\
				where disliked.post_id = comment.id\
					and disliked.disliked = true) as ndislikes\
			from browse_packagecomment comment\
					left join browse_packagerating rate on rate.package_id = comment.package_id and\
														rate.user_id = comment.user_id\
					join accounts_user account on comment.user_id = account.id\
			where comment.user_id != %s and comment.package_id = %s\
			order by time desc\
		) other_comments', [user_id, post_id, user_id, post_id])
	return results


def get_react_count_post(post):
	""":returns (likes_count, dislikes_count) of post in package"""
	from browse.models import PostCommentReact
	nliked = PostCommentReact.objects.filter(post=post, liked=True).count()
	ndisliked = PostCommentReact.objects.filter(post=post, disliked=True).count()
	return nliked, ndisliked


def get_rating_author(user_id):
	""":returns avg rating over all users from all branches"""
	results = namedtuplefetchall(
		'select avg(rating) as avg_rating\
		from browse_branchrating join accounts_restaurantbranch\
									on browse_branchrating.branch_id = accounts_restaurantbranch.id\
		where accounts_restaurantbranch.restaurant_id = %s', [user_id])
	return results[0].avg_rating


def update_rating_post(user, pkg_id, rating):
	""" create or update user rating on package """
	from browse.models import PostRating
	from browse.models import Post
	package = Post.objects.get(id=pkg_id)
	post, _ = PostRating.objects.get_or_create(package=package, user=user)
	post.rating = rating
	post.save()


def update_comment_post(user, pkg_id, comment):
	""" create or update user comment on package """
	from browse.models import PostComment
	from browse.models import Post
	package = Post.objects.get(id=pkg_id)
	post, _ = PostComment.objects.get_or_create(package=package, user=user)
	post.comment = comment
	post.save()


def update_comment_react_post(user, comment_id, react_val):
	"""
	create or update react on existing post of any user on package
	:returns updated (likes_count, dislikes_count) of that post
	"""
	from browse.models import PostComment, PostCommentReact
	post = PostComment.objects.get(id=comment_id)
	if react_val in ['like', 'dislike']:
		react, _ = PostCommentReact.objects.get_or_create(post=post, user=user)
		print(react)

		react.liked = (react_val == 'like')
		react.disliked = (react_val == 'dislike')
		react.save()
	return get_react_count_post(post)


# ------------ Posts -----------------------------

def get_named_post(name):
	"""
	:param name: package-name / restaurant-name / category-name / ingredient-name
	:return: set of packages satisfying above criteria
	"""
	from browse.models import Post
	return (Post.objects.filter(
		pkg_name__icontains=name) | Post.objects.filter(
		# restaurant__restaurant_name__icontains=name) | Package.objects.filter(
		ingr_list__name__icontains=name) | Post.objects.filter(
		category__icontains=name)).distinct()


def get_rated_post(rating=0):
	from browse.models import PostRating
	from django.db.models import Avg
	pkg_ids = PostRating.objects.values('post').annotate(avg=Avg('rating')).filter(
		avg__gte=rating).values('post').distinct()
	from browse.models import Post
	return Post.objects.filter(id__in=pkg_ids).distinct()


def get_nviews_range_post(low=0.0, high=90000.0):
	from browse.models import Post
	from django.db.models import Q
	return Post.objects.filter(Q(price__gte=low) & Q(price__lte=high)).distinct()


def get_category_post(categoty_name):
	"""
	:param categoty_name: category-name
	:return: set of packages satisfying above criteria
	"""
	from browse.models import Post
	return Post.objects.filter(category__iexact=categoty_name).distinct()


#  ----------------------- Insert utils -------------------------
def insert_post(post_name, genre_list, category, user_id):
	from browse.models import Post
	user = User.objects.get(id=user_id)
	package, _ = Post.objects.get_or_create(pkg_name=post_name, category=category, author=user)
	for gen in genre_list:
		from browse.models import Genre
		from browse.models import GenreList
		gen = str(gen).strip().lower()
		genre, _ = Genre.objects.get_or_create(name=gen)
		GenreList.objects.get_or_create(post=package, genre=genre)
