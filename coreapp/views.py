from django.shortcuts import render


# Create your views here.
def view_navbar(request, *args, **kwargs):
    return render(request, 'coreapp/base.html', {})
