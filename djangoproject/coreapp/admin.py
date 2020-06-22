from django.contrib import admin

# Register your models here.
from coreapp.models import *

admin.site.register(Post)
admin.site.register(PostReact)
admin.site.register(PostComment)
admin.site.register(PostCommentReact)
admin.site.register(Keyword)
admin.site.register(KeywordList)
