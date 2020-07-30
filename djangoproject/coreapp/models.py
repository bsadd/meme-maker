from django.urls import reverse

from accounts.models import User
from coreapp.consts_db import Reaction, ApprovalStatus
from coreapp.managers import *
from coreapp import validators


class Keyword(models.Model):
    """Keywords of a post like insulting, depressed etc."""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Keyword"
        verbose_name_plural = "Keywords"

    def __str__(self):
        return self.name


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
    modified_at = models.DateTimeField(auto_now=True)

    approval_status = models.CharField(max_length=8, verbose_name="Approval Status",
                                       choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    approval_details = models.CharField(max_length=200, verbose_name="Approval Verdict Reason", default='')
    approval_at = models.DateTimeField(null=True, blank=True)

    moderator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='moderator')

    template = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')

    keywords = models.ManyToManyField(Keyword, through='coreapp.KeywordList', related_name='post_keywords')

    reactions = models.ManyToManyField(User, through='coreapp.PostReaction', related_name='post_reaction_user')
    comments = models.ManyToManyField(User, through='coreapp.PostComment', related_name='post_comment_user')

    objects = PostManager()
    approved = PostManager(approval_status=ApprovalStatus.APPROVED)
    pending = PostManager(approval_status=ApprovalStatus.PENDING)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return "%s %s" % (self.caption, self.author)

    def get_template_id(self):
        """Blank Template id for an image. Own id if itself is a template"""
        if self.is_template_post():
            return self.id
        return self.template_id

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


def factory_manager_for_postreaction(post_id):
    return PostReactionManager.factory(model=PostReaction, post_id=post_id)


class PostReaction(models.Model):
    """
    Like, Dislike reactions of viewers on a post
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # , validators=[__is_approved_post]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # , validators=[__is_allowed_user]

    reaction = models.IntegerField(verbose_name="Reaction", choices=Reaction.choices, default=Reaction.NONE)
    modified_at = models.DateTimeField(auto_now=True)

    objects = PostReactionManager()
    of_post = factory_manager_for_postreaction

    class Meta:
        verbose_name = "Post Reaction"
        verbose_name_plural = "Post Reactions"
        unique_together = [['post', 'user']]

    def reaction_name(self):
        return Reaction(self.reaction).label

    def __str__(self):
        return "%s %s %s" % (str(self.user), self.reaction_name(), str(self.post))


class PostComment(models.Model):
    """
    Comments of users for a post
    """
    comment = models.CharField('User Comment', max_length=250, blank=False, null=False)
    time = models.DateTimeField(verbose_name="Post Time", auto_now=True, auto_now_add=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comment_author_user')
    reacts = models.ManyToManyField(User, through='coreapp.PostCommentReact', related_name='comment_react_user')

    class Meta:
        verbose_name = "Post's Comment"
        verbose_name_plural = "Post's Comments"
        unique_together = [['post', 'user']]


class PostCommentReact(models.Model):
    """
    Like, Dislike reactions of viewers for others comment on a post
    """
    post = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    react = models.IntegerField(verbose_name="React", choices=Reaction.choices, default=Reaction.NONE)

    class Meta:
        verbose_name = "Comment's React"
        verbose_name_plural = "Comment's Reaction"
        unique_together = [['post', 'user']]
