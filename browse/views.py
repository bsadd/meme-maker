from django.views.generic import TemplateView

from browse import utils_db
from browse.models import *

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


def upload_meme_image(request):
    genre_list = request.POST.getlist('keywords')[0].split(',')
    caption = request.POST.get('caption')
    template_id = request.POST.get('template-id')
    image = request.POST.get('memeImg')
    if template_id is None or caption is None or image is None:
        return HttpResponse('Invalid')

    post = utils_db.insert_meme_post(user_id=request.user.id, image_base64=image, post_name=caption,
                                     genre_list=genre_list, is_adult=False)
    return HttpResponse(post.id)


def upload_template_image(request):
    genre_list = request.POST.getlist('keywords')[0].split(',')
    # category = request.POST.get('category')
    caption = request.POST.get('caption')
    # image = request.POST.get('memeImg')
    template = request.POST.get('template')
    if template is None or caption is None:
        return HttpResponse('Invalid data')

    post = utils_db.insert_template_post(user_id=request.user.id, image_base64=template, post_name=caption,
                                         genre_list=genre_list, is_adult=False)
    return HttpResponse(post.id)


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
    template_name = 'browse/memeUpload.html'

    def get(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        # 	return redirect('accounts:login')
        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(AddMemeView, self).get_context_data()
        context['loggedIn'] = self.request.user.is_authenticated
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse('Not logged in')

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
    """Renders Contact Page"""

    print(request.POST)
    st = render(request, 'browse/memeEdit.html',
                context={'fullLoad': False, 'post': Post.objects.get(id=id)})
    print(st)
    return st
