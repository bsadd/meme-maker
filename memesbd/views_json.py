from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view

from coreapp.decorators import ajax_login_required, moderator_login_required
from memesbd import utils_db
from memesbd.models import *


@api_view(http_method_names=['GET'])
def meme_list(request):
    page = 1 if request.GET.get("page") is None else request.GET.get("page")
    type = 'all' if request.GET.get("type") not in ['all', 'popular', 'mymeme'] else request.GET.get("type")
    query = '' if request.GET.get("query") is None else request.GET.get("query")
    posts = Post.objects.filter(approval_status=ApprovalStatus.APPROVED)
    if type == 'all':
        posts = Post.approved.all()
    elif type == 'mymeme':
        posts = Post.objects.filter(author=request.user)
    posts = posts.filter(caption__icontains=query)
    from django.core.paginator import Paginator
    paginator = Paginator(posts, 3)
    posts = paginator.get_page(page)
    from memesbd.serializers import PostSerializer
    from rest_framework.response import Response
    from rest_framework import status
    return Response(PostSerializer(posts, many=True).data, status.HTTP_200_OK)


@ajax_login_required
def meme_create(request):
    """
    requires image in base64 encoded format
    """
    keyword_list = request.POST.getlist('keywords')
    if keyword_list is not None:
        keyword_list = keyword_list[0].split(',')
    caption = request.POST.get('caption')
    is_adult = False if request.POST.get('is_adult') is None else request.POST.get('is_adult')
    template_id = request.POST.get('template-id')
    image = request.POST.get('image')
    if caption is None or image is None:
        return JsonResponse({'url': None, 'caption': caption, 'image': image})

    post = utils_db.insert_meme_post(user_id=request.user.id, image_base64=image, caption=caption,
                                     keyword_list=keyword_list, is_adult=is_adult,
                                     template_id=template_id) if template_id is not None else utils_db.insert_template_post(
        user_id=request.user.id, image_base64=image, caption=caption,
        keyword_list=keyword_list, is_adult=is_adult)

    return JsonResponse({'url': post.get_absolute_url(), 'is_template': post.is_template_post()})


@moderator_login_required
def moderation_action(request):
    try:
        post = Post.objects.get(id=request.POST.get('post_id'))
        action_type = request.POST.get('action_type')
        if action_type and post.approval_status == ApprovalStatus.PENDING:
            if action_type.upper() == ApprovalStatus.STATUS_NAMES[ApprovalStatus.APPROVED]:
                post.moderator = request.user
                post.approval_status = ApprovalStatus.APPROVED
                post.save()
            elif action_type.upper() == ApprovalStatus.STATUS_NAMES[ApprovalStatus.REJECTED]:
                post.moderator = request.user
                post.approval_status = ApprovalStatus.REJECTED
                post.save()
            return JsonResponse({'approval_status': post.approval_status, 'url': post.get_absolute_url()})
        else:
            return JsonResponse({'result': 'not a valid action_type', 'url': None})
    except Post.DoesNotExist:
        return JsonResponse({'result': 'post does not exists', 'url': None})
    except KeyError:
        return JsonResponse({'result': 'need post_id & action_type', 'url': None})


@ajax_login_required
def react_submit(request):
    react_name = str(request.POST.get('reaction_type')).upper()
    id = int(request.POST.get('post_id'))
    print(str(request.user) + ' ' + react_name + ' on ' + str(id))
    if Reacts.is_valid_react(Reacts.REACT_VALUE[react_name]):
        post_react = utils_db.update_react_post(user=request.user, post_id=id, react=Reacts.REACT_VALUE[react_name])
        if post_react is not None:
            return JsonResponse(
                {'success': True, 'id': id, 'react': Reacts.REACT_NAMES[post_react.react]})
    return JsonResponse({'success': False})


@ajax_login_required
def comment_submit(request):
    comment = str(request.POST.get('comment')).upper()
    id = int(request.POST.get('post_id'))
    print(str(request.user) + ' ' + comment + ' on ' + str(id))
    try:
        post = utils_db.update_comment_post(user=request.user, post_id=id, comment=comment)
        return JsonResponse(
            {'success': True, 'comment': post.comment, 'url': post.post.get_absolute_url()})
    except Post.DoesNotExist:
        return JsonResponse({'success': False, 'comment': None, 'details': 'Post not found'})
    except KeyError:
        return JsonResponse({'success': False, 'comment': None, 'details': 'comment & post_id not passed properly'})
