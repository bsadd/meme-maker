from django.urls import reverse

from accounts.models import User
from memesbd.consts_db import Reacts, ApprovalStatus
from memesbd.managers import *
from memesbd import validators


class Keyword(models.Model):
    """Keywords of a post like insulting, depressed etc."""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Keyword"
        verbose_name_plural = "Keywords"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("memesbd:keyword-details", kwargs={"pk": self.pk})


class Post(models.Model):
    """
    Entity for a post maintained by a user
    Keeping blank template as reference
    """
    caption = models.CharField(max_length=50)
    image = models.ImageField(upload_to='img/', default='img/default.png')
    nviews = models.IntegerField(default=0, verbose_name='Number of views')

    is_adult = models.BooleanField(default=False, verbose_name='Adult Content')
    is_violent = models.BooleanField(default=False, verbose_name='Violent Content')

    configuration_head = models.CharField(max_length=100, default='', verbose_name='Text-Boxes top of image')
    configuration_over = models.CharField(max_length=1000, default='', verbose_name='Text-Boxes on image')
    configuration_tail = models.CharField(max_length=100, default='', verbose_name='Text-Boxes below of image')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    approval_status = models.CharField(max_length=2, verbose_name="Approval Status",
                                       choices=ApprovalStatus.approval_status(), default=ApprovalStatus.PENDING)
    approval_details = models.CharField(max_length=200, verbose_name="Approval Verdict Reason", default='')
    approval_at = models.DateTimeField(null=True, blank=True)

    moderator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='moderator')

    template = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')

    keywords = models.ManyToManyField(Keyword, through='memesbd.KeywordList', related_name='post_keywords')

    reacts = models.ManyToManyField(User, through='memesbd.PostReact', related_name='post_react_user')
    comments = models.ManyToManyField(User, through='memesbd.PostComment', related_name='post_comment_user')

    objects = models.Manager()
    approved = ApprovedPostManager()
    pending = PendingPostManager()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        # default_manager_name = models.Manager()
        # base_manager_name = models.Manager()

    def __str__(self):
        return "%s %s" % (self.caption, self.author)

    def get_absolute_url(self):
        return reverse("memesbd:view-meme", kwargs={"id": self.pk})

    def get_absolute_edit_url(self):
        return reverse("memesbd:edit-meme", kwargs={"id": self.pk})

    def get_absolute_template_edit_url(self):
        return reverse("memesbd:edit-meme", kwargs={"id": self.get_template_id()})

    def get_template_id(self):
        """Blank Template id for an image. Own id if itself is a template"""
        if self.is_template_post():
            return self.id
        return self.template.id

    def is_template_post(self):
        return self.template is None

    def image_shape(self):
        if self.image is None:
            return 0, 0
        from PIL import Image
        return Image.open(self.image).size

    def is_active(self):
        return self.approval_status == ApprovalStatus.APPROVED


class KeywordList(models.Model):
    """
    Keeps which post has which keywords
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "KeywordList"
        verbose_name_plural = "KeywordLists"
        unique_together = [['post', 'keyword']]

    def get_absolute_url(self):
        return reverse("memesbd:keywords", kwargs={"pk": self.pk})


class PostReact(models.Model):
    """
    Like, Dislike reacts of viewers on a post
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # , validators=[__is_approved_post]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # , validators=[__is_allowed_user]

    react = models.IntegerField(verbose_name="React", choices=Reacts.react_choices(), default=Reacts.NONE,
                                validators=[validators.is_valid_react])

    class Meta:
        verbose_name = "Post React"
        verbose_name_plural = "Post Reacts"
        unique_together = [['post', 'user']]

    def react_name(self):
        return Reacts.REACT_NAMES[self.react]

    def get_absolute_url(self):
        return reverse("memesbd:PostReact", kwargs={"id": self.pk})

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
    reacts = models.ManyToManyField(User, through='memesbd.PostCommentReact', related_name='comment_react_user')

    class Meta:
        verbose_name = "Post's Comment"
        verbose_name_plural = "Post's Comments"
        unique_together = [['post', 'user']]

    def get_absolute_url(self):
        return reverse("memesbd:PostComment", kwargs={"id": self.pk})


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
        return reverse("memesbd:PostCommentReact", kwargs={"id": self.pk})
