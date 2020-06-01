"""
Contains utility functions for database query maintenance i.e. Insert/Update
"""

from collections import namedtuple

from django.db import connection

# ------------------ util functions --------------------------
from accounts.models import User
from memesbd.models import Post, PostReact
from memesbd.consts_db import ApprovalStatus


def namedtuplefetchall(query, param_list):
    """Return all rows from a cursor as a namedtuple"""
    with connection.cursor() as cursor:
        cursor.execute(query, param_list)
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]


# ------------------- Review Ratings -------------------------


def get_react_count_post(post_id):
    """
    :param post_id: id of the post
    :returns an array with index as status-value and value as count
    i.e. ret_val[Reacts.UPVOTE] is number of times this post had been up-voted
    """
    from django.db.models import Count
    qset = PostReact.objects.filter(post_id=post_id).annotate(count=Count('user')).values('react', 'count')
    from memesbd.consts_db import Reacts
    react_counts = [0] * (Reacts.__MAX + 1)
    for q in qset:
        react_counts[q['status']] = q['count']
    return react_counts


def update_react_post(user, post_id, react):
    """ create or update user status on post """
    from memesbd.consts_db import Reacts
    if not Reacts.is_valid_react(react):
        return
    from memesbd.models import PostReact
    from memesbd.models import Post
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return None
    post_react, _ = PostReact.objects.get_or_create(post=post, user=user)
    post_react.react = react
    post_react.save()
    return post_react


def update_comment_post(user, pkg_id, comment):
    """ create or update user comment on package """
    from memesbd.models import PostComment
    from memesbd.models import Post
    package = Post.objects.get(id=pkg_id)
    post, _ = PostComment.objects.get_or_create(package=package, user=user)
    post.comment = comment
    post.save()


def update_comment_react_post(user, comment_id, react_val):
    """
    create or update status on existing post of any user on package
    :returns updated (likes_count, dislikes_count) of that post
    """
    from memesbd.models import PostComment, PostCommentReact
    post = PostComment.objects.get(id=comment_id)
    if react_val in ['like', 'dislike']:
        react, _ = PostCommentReact.objects.get_or_create(post=post, user=user)
        print(react)

        react.liked = (react_val == 'like')
        react.disliked = (react_val == 'dislike')
        react.save()
    return get_react_count_post(post)


# ------------ User Profile -----------------------------

def get_pending_posts(user_id):
    return Post.objects.filter(author_id=user_id, approval_status=ApprovalStatus.PENDING)


def get_approved_posts(user_id):
    return Post.objects.filter(author_id=user_id, approval_status=ApprovalStatus.APPROVED)


def get_rejected_posts(user_id):
    return Post.objects.filter(author_id=user_id, approval_status=ApprovalStatus.REJECTED)


# ------------ Posts -----------------------------

def get_posts(key=''):
    """
    :param key: search key to look for posts
    :return: set of posts satisfying above criteria
    """
    caption = key.strip().lower()
    keywords = [k.lower() for k in key.split()]
    from memesbd.models import Post
    return (Post.objects.filter(
        caption__icontains=caption) | Post.objects.filter(
        keywords__keyword__name__in=keywords)).distinct()


def get_nviews_range_post(low=0.0, high=90000.0):
    from memesbd.models import Post
    from django.db.models import Q
    return Post.objects.filter(Q(nviews__gte=low) & Q(nviews__lte=high)).distinct()


def get_related_posts(post_id, post=None):
    """
    :param post_id: id of the post to look for memes made on its template
    :param post: the post to look for memes made on its template. pass to deter double hit on db
    :return: qset of memes excluding itself & blank template
    """
    if post is None:
        post = Post.objects.get(id=post_id)
    if post.is_template_post():
        return Post.objects.filter(template=post)
    else:
        return Post.objects.exclude(id=post.id).filter(template=post.template)


#  ----------------------- Insert utils -------------------------
def insert_template_post(caption, keyword_list, image_base64, is_adult, user_id):
    """
    :param text_boxes: a list of TextBox objects
    :param caption: caption
    :param keyword_list: list of keywords
    :param image_base64: js image data
    :param is_adult: is adult content
    :param user_id: author id
    """
    from memesbd.models import Post
    from memesbd.utils import trim_replace_wsp
    post = Post.objects.create(caption=trim_replace_wsp(caption), author_id=user_id)
    post.is_adult = is_adult
    for gen in keyword_list:
        from memesbd.models import Keyword, KeywordList
        gen = str(gen).strip().lower()
        keyword, _ = Keyword.objects.get_or_create(name=gen)
        KeywordList.objects.get_or_create(post=post, keyword=keyword)
    from memesbd.utils import image_to_file
    img_filename, img_data = image_to_file(img_base64=image_base64, file_id=post.id)
    post.image.save(img_filename, img_data, save=True)
    post.save()
    return post


def insert_template_post_path(caption, keyword_list, image_path, is_adult, user_id):
    """
    :param text_boxes: a list of TextBox objects
    :param caption: caption
    :param keyword_list: list of keywords
    :param image_path: image path on server
    :param is_adult: is adult content
    :param user_id: author id
    """
    from memesbd.models import Post
    from memesbd.utils import trim_replace_wsp
    post = Post.objects.create(caption=trim_replace_wsp(caption), author_id=user_id)
    post.is_adult = is_adult
    for gen in keyword_list:
        from memesbd.models import Keyword, KeywordList
        gen = str(gen).strip().lower()
        keyword, _ = Keyword.objects.get_or_create(name=gen)
        KeywordList.objects.get_or_create(post=post, keyword=keyword)
    post.image = image_path
    post.save()
    return post


def insert_meme_post(caption, keyword_list, image_base64, is_adult, user_id, template_id):
    """
    :param text_boxes: a list of TextBox objects
    :param caption: caption
    :param keyword_list: list of keywords
    :param image_base64: js image data
    :param is_adult: is adult content
    :param user_id: author id
    :param template_id: id of the meme on which it had been edited on
    """
    from memesbd.models import Post
    template_id = Post.objects.get(id=template_id).get_template_id()
    from memesbd.utils import trim_replace_wsp
    post = Post.objects.create(caption=trim_replace_wsp(caption), author_id=user_id, template_id=template_id)
    post.is_adult = is_adult
    for gen in keyword_list:
        from memesbd.models import Keyword, KeywordList
        gen = str(gen).strip().lower()
        keyword, _ = Keyword.objects.get_or_create(name=gen)
        KeywordList.objects.get_or_create(post=post, keyword=keyword)
    from memesbd.utils import image_to_file
    img_filename, img_data = image_to_file(img_base64=image_base64, file_id=post.id)
    post.image.save(img_filename, img_data, save=True)
    return post
