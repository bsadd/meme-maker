from django.db import models

# Create your models here.

from django.db import models
from django.urls import reverse

from accounts.models import User


class Genre(models.Model):
    """Genres of a post like insulting, depressed etc."""
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Ingredient_detail", kwargs={"pk": self.pk})


class Post(models.Model):
    """
    Entity for a post maintained by a user
    """
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='img/', default='img/default.png')
    nviews = models.IntegerField(default=0, verbose_name='Number of views')
    ndownloads = models.IntegerField(default=0, verbose_name='Number of downloads')
    is_adult = models.BooleanField(default=False, verbose_name='Adult Content')
    # details = models.CharField(max_length=250, blank=True)

    is_template = models.BooleanField(default=False, verbose_name='Template Image')

    template = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    genre_list = models.ManyToManyField(Genre, through='browse.GenreList', related_name='post_genres')

    ratings = models.ManyToManyField(User, through='browse.PostRating', related_name='post_rating_user')
    comments = models.ManyToManyField(User, through='browse.PostComment', related_name='post_comment_user')

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("browse:view-meme", kwargs={"id": self.pk})

    def get_absolute_edit_url(self):
        return reverse("browse:edit-meme", kwargs={"id": self.pk})

    def get_template_id(self):
        """Blank Template id for an image. Own id if itself is a template"""
        if self.template is None:
            return self.id
        return self.template.id

    def is_editable(self, user):
        return user.is_authenticated and user.author.id == self.author.id

    def get_avg_rating(self):
        from browse.utils_db import get_rating_post
        return get_rating_post(self.id)


class GenreList(models.Model):
    """
    Keeps which post has which genres
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "GenreList"
        verbose_name_plural = "GenreLists"

    def get_absolute_url(self):
        return reverse("IngredientList_detail", kwargs={"pk": self.pk})


class PostRating(models.Model):
    """
    Ratings for a post rated by a user
    """
    rating = models.IntegerField('Rating', default=5, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Post Rating"
        verbose_name_plural = "Post Ratings"
        unique_together = [['post', 'user']]

    def get_absolute_url(self):
        return reverse("browse:PackageRating", kwargs={"id": self.pk})

    def __str__(self):
        return self.post.__str__() + " " + str(self.rating) + " from " + self.user.__str__()


class PostComment(models.Model):
    """
    Comments of customers for a post
    """
    comment = models.CharField('User Comment', max_length=250, blank=False, null=False)
    time = models.DateTimeField(verbose_name="Post Time", auto_now=True, auto_now_add=False)
    package = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comment_author_user')
    reacts = models.ManyToManyField(User, through='browse.PostCommentReact', related_name='post_react_user')

    class Meta:
        verbose_name = "Package Comment"
        verbose_name_plural = "Package Comments"
        unique_together = [['package', 'user']]

    def get_absolute_url(self):
        return reverse("browse:PackageComment", kwargs={"id": self.pk})


class PostCommentReact(models.Model):
    """
    Like, Dislike reacts of viewers for others comment on a post
    """
    post = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    liked = models.BooleanField(verbose_name='Liked', default=False)
    disliked = models.BooleanField(verbose_name='Disliked', default=False)

    class Meta:
        verbose_name = "Post Comment React"
        verbose_name_plural = "Post Comment Reacts"
        unique_together = [['post', 'user']]

    def get_absolute_url(self):
        return reverse("browse:PackageCommentReact", kwargs={"id": self.pk})
