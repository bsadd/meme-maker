from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from accounts.models import User
from browse.consts_db import Reacts, TextPositions


class Keyword(models.Model):
    """Keywords of a post like insulting, depressed etc."""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Keyword"
        verbose_name_plural = "Keywords"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("browse:keyword-details", kwargs={"pk": self.pk})


class Post(models.Model):
    """
    TODO: incorporate collage
    Entity for a post maintained by a user
    Keeping blank template as reference
    """
    caption = models.CharField(max_length=50)
    image = models.ImageField(upload_to='img/', default='img/default.png')
    nviews = models.IntegerField(default=0, verbose_name='Number of views')

    is_adult = models.BooleanField(default=False, verbose_name='Adult Content')
    is_violent = models.BooleanField(default=False, verbose_name='Violent Content')

    template = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    genre_list = models.ManyToManyField(Keyword, through='browse.KeywordList', related_name='post_genres')

    reacts = models.ManyToManyField(User, through='browse.PostReact', related_name='post_react_user')
    comments = models.ManyToManyField(User, through='browse.PostComment', related_name='post_comment_user')

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return "%s %s" % (self.caption, self.author)

    def get_absolute_url(self):
        return reverse("browse:view-meme", kwargs={"id": self.pk})

    def get_absolute_edit_url(self):
        return reverse("browse:edit-meme", kwargs={"id": self.pk})

    def get_absolute_template_edit_url(self):
        return reverse("browse:edit-meme", kwargs={"id": self.get_template_id()})

    def get_template_id(self):
        """Blank Template id for an image. Own id if itself is a template"""
        if self.is_template_post():
            return self.id
        return self.template.id

    def is_template_post(self):
        return self.template is None

    def related_posts(self):
        from browse import utils_db
        return utils_db.get_related_posts(self.id, self)

    def image_shape(self):
        if self.image is None:
            return 0, 0
        from PIL import Image
        return Image.open(self.image).size


class TextBox(models.Model):
    """
    TODO: multi line text
    Textbox of image of a post
    """
    position = models.CharField(max_length=1, verbose_name="Position Type", choices=TextPositions.position_choices(),
                                default=TextPositions.OVER)

    style_text = models.CharField(max_length=100, verbose_name='Style Text', default='')
    background_color = models.CharField(max_length=7, verbose_name='Textbox Background Fill Color', default='#ffffff')
    background_opacity = models.IntegerField(verbose_name='Textbox Background Opacity', default=0)

    pos_x = models.IntegerField(verbose_name='textbox\'s leftmost X coordinate')
    pos_y = models.IntegerField(verbose_name='textbox\'s topmost  Y coordinate')
    pos_z = models.IntegerField(verbose_name='Relative Order Position from Image(0) to Front(inf)')

    len_x = models.IntegerField(verbose_name='Textbox Horizontal Width')
    len_y = models.IntegerField(verbose_name='Textbox Vertical Height')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image_textboxes')

    class Meta:
        verbose_name = "Textbox"
        verbose_name_plural = "Textboxes"

    def get_absolute_url(self):
        return reverse("browse:PostReact", kwargs={"id": self.pk})

    def __str__(self):
        return "%s %s" % (self.position, str(self.post))

    def is_valid_config(self):
        img_w, img_h = self.post.image_shape()
        if img_w is None or img_h is None or TextPositions.is_valid_position(self.position):
            return False
        if self.pos_x < 0 or self.pos_y < 0 or self.pos_z < 0 or \
                self.pos_x + self.len_x > img_w or self.pos_y + self.len_y > img_h:
            return False
        import re
        pattern = re.compile("#[0-9a-f]{6}$")
        if not bool(pattern.match(self.background_color)):
            return False
        return True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_valid_config():
            super().save(force_insert, force_update, using, update_fields)
        else:
            raise ValidationError(message='Invalid Text Box Config')


class KeywordList(models.Model):
    """
    Keeps which post has which genres
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "KeywordList"
        verbose_name_plural = "KeywordLists"
        unique_together = [['post', 'keyword']]

    def get_absolute_url(self):
        return reverse("browse:keywords", kwargs={"pk": self.pk})


class PostReact(models.Model):
    """
    Like, Dislike reacts of viewers on a post
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    react = models.IntegerField(verbose_name="React", choices=Reacts.react_choices(), default=Reacts.NONE)

    class Meta:
        verbose_name = "Post React"
        verbose_name_plural = "Post Reacts"
        unique_together = [['post', 'user']]

    def get_absolute_url(self):
        return reverse("browse:PostReact", kwargs={"id": self.pk})

    def __str__(self):
        return "%s %s %s" % (str(self.user), Reacts.REACT_NAMES[self.react], str(self.post))


class PostComment(models.Model):
    """
    Comments of users for a post
    """
    comment = models.CharField('User Comment', max_length=250, blank=False, null=False)
    time = models.DateTimeField(verbose_name="Post Time", auto_now=True, auto_now_add=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comment_author_user')
    reacts = models.ManyToManyField(User, through='browse.PostCommentReact', related_name='comment_react_user')

    class Meta:
        verbose_name = "Post's Comment"
        verbose_name_plural = "Post's Comments"
        unique_together = [['post', 'user']]

    def get_absolute_url(self):
        return reverse("browse:PostComment", kwargs={"id": self.pk})


class PostCommentReact(models.Model):
    """
    Like, Dislike reacts of viewers for others comment on a post
    """
    post = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    react = models.IntegerField(verbose_name="React", choices=Reacts.react_choices(), default=Reacts.NONE)

    class Meta:
        verbose_name = "Comment's React"
        verbose_name_plural = "Comment's Reacts"
        unique_together = [['post', 'user']]

    def get_absolute_url(self):
        return reverse("browse:PostCommentReact", kwargs={"id": self.pk})
