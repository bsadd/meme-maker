from django.contrib import admin

# Register your models here.
from browse.models import *

admin.site.register(Post)
admin.site.register(PostRating)
admin.site.register(PostComment)
admin.site.register(PostCommentReact)
admin.site.register(Genre)
admin.site.register(GenreList)

