from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from memesbd.models import Post


def view_navbar(request, *args, **kwargs):
    return render(request, 'coreapp/base.html', {})


def view_meme_gallery(request, *args, **kwargs):

    posts = Post.objects.get_queryset().order_by('id')
    paginator = Paginator(posts, 3)
    page = request.GET.get("page")
    posts = paginator.get_page(page)


    st = render(request, 'coreapp/meme_gallery.html',
                context={'loggedIn': request.user.is_authenticated, 'fullLoad': request.POST.get('fromAjax') is None,
                         'post': posts})
    return st
