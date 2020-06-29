"""
Contains utility functions for database query maintenance i.e. Insert/Update
"""

# ------------------ util functions --------------------------
from memesbd.models import Post, PostReact
from memesbd.consts_db import ApprovalStatus, Reacts


# ------------------- Review -------------------------


def get_react_count_post(post_id):
    return PostReact.objects.reacts_count_map(post_id)


def update_react_post(user, post_id, react):
    """ create or update user status on post """
    from memesbd.consts_db import Reacts
    if not Reacts.is_valid_react(react):
        from django.core.exceptions import ValidationError
        raise ValidationError
    from memesbd.models import PostReact
    from memesbd.models import Post
    post = Post.objects.get(id=post_id)
    if post.approval_status != ApprovalStatus.APPROVED:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    return PostReact.objects.all().of_approved_posts().create(post=post, user=user, react=react)


# ------------ Posts -----------------------------

def get_posts(key=''):
    """
    :param key: search key to look for posts
    :return: set of posts satisfying above criteria
    """
    caption = key.strip().lower()
    keywords = [k.lower() for k in key.split()]
    from memesbd.models import Post
    return (Post.approved.filter(caption__icontains=caption) | Post.objects.filter(
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
        return Post.approved.filter(template=post)
    else:
        return Post.approved.exclude(id=post.id).filter(template_id=post.template_id)


#  ----------------------- Insert utils -------------------------
def insert_post_path(caption, keyword_list, image_path, is_adult, user_id):
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


def insert_post(caption, user_id, image_base64, keyword_list=None, is_adult=False, is_violent=False, template_id=None):
    """
    :param text_boxes: a list of TextBox objects
    :param caption: caption
    :param keyword_list: list of keywords
    :param image_base64: js image data
    :param is_adult: is adult content
    :param is_violent: is violent content
    :param user_id: author id
    :param template_id: id of the meme on which it had been edited on
    """
    if keyword_list is None:
        keyword_list = []
    from memesbd.models import Post
    from memesbd.utils import trim_replace_wsp
    if template_id:
        template_id = Post.objects.get(id=template_id).get_template_id()
    post = Post.objects.create(caption=trim_replace_wsp(caption), author_id=user_id, template_id=template_id)
    post.is_adult = is_adult
    post.is_violent = is_violent
    for key in keyword_list:
        from memesbd.models import Keyword, KeywordList
        keyword, _ = Keyword.objects.get_or_create(name=str(key).strip().lower())
        KeywordList.objects.get_or_create(post=post, keyword=keyword)
    from memesbd.utils import image_to_file
    img_filename, img_data = image_to_file(img_base64=image_base64, file_id=post.id)
    post.image.save(img_filename, img_data, save=True)
    return post
