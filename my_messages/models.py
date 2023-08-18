from django.db import models
from users.models import MyUser



class Chat(models.Model):
    author = models.ForeignKey(MyUser, related_name='chat_author', on_delete=models.CASCADE)
    recipient = models.ForeignKey(MyUser, related_name='chat_recipient', on_delete=models.CASCADE)

    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    is_pinned_recipient = models.BooleanField(default=False)
    is_archived_recipient = models.BooleanField(default=False)

    last_message = models.DateTimeField(null=True, blank=True)
    last_message_text = models.ForeignKey('Message', on_delete=models.CASCADE, related_name='last_chat', null=True, blank=True)


    is_block  = models.BooleanField(default=False)
    is_block_recipient = models.BooleanField(default=False)

    author_notification = models.BooleanField(default=True)
    recipient_notification = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)

    messages = models.ManyToManyField('Message', null=True, blank=True, related_name='chat',)

    def __str__(self):
        return f'{self.author} start chatting {self.recipient}'

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(MyUser, related_name='message_user', on_delete=models.CASCADE)
    is_pinned = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply', null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_forwarded = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='forward_message', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_recipient = models.BooleanField(default=False)

    def __str__(self):
        return self.message