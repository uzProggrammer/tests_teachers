from datetime import datetime

from django.db import models
from users.models import MyUser
from ckeditor.fields import RichTextField


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
        time = datetime.now()
        if self.date_created.day == time.day:
            return str(time.hour - self.date_created.hour) + " soat oldin"
        else:
            if self.date_created.month == time.month:
                return str(time.day - self.date_created.day) + " kun oldin"
            else:
                if self.date_created.year == time.year:
                    return str(time.month - self.date_created.month) + " oy oldin"
        return self.date_created

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