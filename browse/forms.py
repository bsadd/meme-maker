from django.forms import ModelForm

from browse.models import Post


class PostForm(ModelForm):
	class Meta:
		model = Post
		fields = ('name', 'for_n_persons', 'image', 'details', 'price', 'category')