from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from coreapp.decorators import ajax_login_required, moderator_login_required
from memesbd import utils_db
from memesbd.models import *

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.urls import reverse_lazy


@ajax_login_required
def upload_meme_image(request):
    """
    :param request: request with edited image over a template
    :return: Json with id: uploaded-post-id, loggedIn:True/False && id is -1 for failure
    """
    keyword_list = request.POST.getlist('keywords')[0].split(',')
    caption = request.POST.get('caption')
    template_id = request.POST.get('template-id')
    image = request.POST.get('memeImg')
    if not request.user.is_authenticated or template_id is None or caption is None or image is None:
        return JsonResponse({'id': -1, 'loggedIn': request.user.is_authenticated})

    post = utils_db.insert_meme_post(user_id=request.user.id, image_base64=image, caption=caption,
                                     keyword_list=keyword_list, is_adult=False, template_id=template_id)
    return JsonResponse({'id': post.id, 'loggedIn': request.user.is_authenticated})


@ajax_login_required
def upload_template_image(request):
    """
    :param request: request a new template image
    :return: Json with id: uploaded-post-id, loggedIn:True/False && id is -1 for failure
    """
    keyword_list = request.POST.getlist('keywords')[0].split(',')
    caption = request.POST.get('caption')
    template = request.POST.get('template')
    if not request.user.is_authenticated or template is None or caption is None:
        return JsonResponse({'id': -1, 'loggedIn': request.user.is_authenticated})

    post = utils_db.insert_template_post(user_id=request.user.id, image_base64=template, caption=caption,
                                         keyword_list=keyword_list, is_adult=False)
    return JsonResponse({'id': post.id, 'loggedIn': request.user.is_authenticated})


class Index(TemplateView):
    """
    Renders Home Page
    """
    template_name = 'memesbd/meme_gallery.html'

    def get_context_data(self, **kwargs):
        # with open("sessionLog.txt", "a") as myfile:
        # 	myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")

        ctx = {'item_list': Post.objects.filter(template__isnull=True)}
        return ctx


class AddMemeView(TemplateView):
    """
    View for uploading template
    """
    template_name = 'memesbd/template_upload.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(self.__class__, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # print(pretty_request(self.request))
        print(request.POST)
        return upload_template_image(request)


class ViewMenusView(TemplateView):
    template_name = 'memesbd/index.html'

    def get_context_data(self, **kwargs):
        obj_list = Post.objects.filter(author=self.request.user)  # .order_by('status', '-time')
        print(obj_list)
        print('-----')
        return {'menu_list': obj_list}


@login_required
def editView(request, id):
    """Renders Edit Page for the given meme id"""

    print(request.POST)
    st = render(request, 'memesbd/meme_edit.html',
                context={'loggedIn': request.user.is_authenticated, 'fullLoad': request.POST.get('fromAjax') is None,
                         'post': Post.objects.get(id=id)})
    print(st)
    return st


def memeDetails(request, id):
    post = Post.objects.get(id=id)
    post.nviews += 1
    post.save()
    return render(request, 'memesbd/meme_details.html',
                  context={'loggedIn': request.user.is_authenticated, 'post': post})


def view_meme_gallery(request, *args, **kwargs):
    posts = Post.objects.filter(approval_status=ApprovalStatus.APPROVED)
    from django.core.paginator import Paginator
    paginator = Paginator(posts, 3)
    page = request.GET.get("page")
    posts = paginator.get_page(page)

    return render(request, 'memesbd/meme_gallery.html',
                  context={'fullLoad': request.POST.get('fromAjax') is None, 'posts': posts})


@ajax_login_required
def update_react(request, id):
    react_name = str(request.POST.get('react')).upper()
    print(str(request.user) + ' ' + react_name + ' on ' + str(id))
    if Reacts.is_valid_react(Reacts.REACT_VALUE[react_name]):
        from utils_db import update_react_post
        post_react = update_react_post(user=request.user, post_id=id, react=Reacts.REACT_VALUE[react_name])
        if post_react is not None:
            return JsonResponse(
                {'success': True, 'id': id, 'react': Reacts.REACT_NAMES[post_react.react],
                 'loggedIn': request.user.is_authenticated})
    return JsonResponse({'success': False, 'loggedIn': request.user.is_authenticated})


@login_required
def approved_posts(request):
    return render(request, 'memesbd/user_posts.html',
                  context={'posts': Post.objects.filter(author=request.user, approval_status=ApprovalStatus.APPROVED)})


@login_required
def pending_posts(request):
    return render(request, 'memesbd/user_posts.html',
                  context={'posts': Post.objects.filter(author=request.user, approval_status=ApprovalStatus.PENDING)})


@login_required
@moderator_login_required
def pending_posts_moderator(request):
    return render(request, 'memesbd/pending_posts.html',
                  context={'posts': Post.objects.filter(approval_status=ApprovalStatus.PENDING)})


@login_required
@moderator_login_required
def approve_post_moderator(request, id):
    post = Post.objects.get(id=id)
    if post.approval_status == ApprovalStatus.PENDING:
        post.moderator = request.user
        post.approval_status = ApprovalStatus.APPROVED
        post.save()
    return redirect(reverse('memesbd:pending-posts-moderator'))


@login_required
@moderator_login_required
def delete_post_moderator(request, id):
    post = Post.objects.get(id=id)
    if post.approval_status == ApprovalStatus.PENDING:
        post.moderator = request.user
        post.approval_status = ApprovalStatus.REJECTED
        post.save()
    return redirect(reverse('memesbd:pending-posts-moderator'))
