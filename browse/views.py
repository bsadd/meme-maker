from django.views.generic import TemplateView

from browse import utils_db
from browse.models import *

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


def upload_meme_image(request):
    """
    :param request: request with edited image over a template
    :return: Json with id: uploaded-post-id, loggedIn:True/False && id is -1 for failure
    """
    genre_list = request.POST.getlist('keywords')[0].split(',')
    caption = request.POST.get('caption')
    template_id = request.POST.get('template-id')
    image = request.POST.get('memeImg')
    if not request.user.is_authenticated or template_id is None or caption is None or image is None:
        return JsonResponse({'id': -1, 'loggedIn': request.user.is_authenticated})

    post = utils_db.insert_meme_post(user_id=request.user.id, image_base64=image, post_name=caption,
                                     genre_list=genre_list, is_adult=False, template_id=template_id)
    return JsonResponse({'id': post.id, 'loggedIn': request.user.is_authenticated})


def upload_template_image(request):
    """
    :param request: request a new template image
    :return: Json with id: uploaded-post-id, loggedIn:True/False && id is -1 for failure
    """
    genre_list = request.POST.getlist('keywords')[0].split(',')
    caption = request.POST.get('caption')
    template = request.POST.get('template')
    if not request.user.is_authenticated or template is None or caption is None:
        return JsonResponse({'id': -1, 'loggedIn': request.user.is_authenticated})

    post = utils_db.insert_template_post(user_id=request.user.id, image_base64=template, post_name=caption,
                                         genre_list=genre_list, is_adult=False)
    return JsonResponse({'id': post.id, 'loggedIn': request.user.is_authenticated})


class Index(TemplateView):
    """
    Renders Home Page
    """
    template_name = 'browse/index.html'

    def get_context_data(self, **kwargs):
        # with open("sessionLog.txt", "a") as myfile:
        # 	myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")

        ctx = {'loggedIn': self.request.user.is_authenticated,
               'item_list': Post.objects.all()
               }
        return ctx


class AddMemeView(TemplateView):
    """
    View for uploading template
    """
    template_name = 'browse/templateUpload.html'

    def get(self, request, *args, **kwargs):


        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(AddMemeView, self).get_context_data()
        context['loggedIn'] = self.request.user.is_authenticated
        return context

    def post(self, request, *args, **kwargs):
        # print(pretty_request(self.request))
        print(request.POST)
        return upload_template_image(request)


class ViewMenusView(TemplateView):
    template_name = 'browse/index.html'

    def get_context_data(self, **kwargs):
        obj_list = Post.objects.filter(author=self.request.user)  # .order_by('status', '-time')
        print(obj_list)
        print('-----')
        return {'loggedIn': self.request.user.is_authenticated, 'menu_list': obj_list}


def editView(request, id):
    """Renders Edit Page for the given meme id"""

    print(request.POST)
    st = render(request, 'browse/memeEdit.html',
                context={'loggedIn': request.user.is_authenticated, 'fullLoad': request.POST.get('fromAjax') is None,
                         'post': Post.objects.get(id=id)})
    print(st)
    return st


def memeDetails(request, id):
    post = Post.objects.get(id=id)
    post.nviews += 1
    post.save()
    return render(request, 'browse/memeDetails.html',
                  context={'loggedIn': request.user.is_authenticated, 'post': post})
