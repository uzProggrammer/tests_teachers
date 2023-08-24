from datetime import datetime

from django.db import models
from users.models import MyUser
from ckeditor.fields import RichTextField
from django.contrib.humanize.templatetags.humanize import naturaltime
import bs4

class Post(models.Model):
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='user_post'
    )
    title = models.CharField(max_length=555)
    content = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(MyUser, related_name='post_likes', null=True, blank=True)

    def get_date(self):
        return str(naturaltime(self.date_created))

    def get_custom_body(self):
        return bs4.BeautifulSoup(self.content, 'html.parser').get_text()

    def __str__(self):
        return self.title

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_comment')
    body = models.TextField()
    updated = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def children(self):
        return PostComment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.on_parent is None:
            return True
        return False