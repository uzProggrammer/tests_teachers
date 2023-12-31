# Generated by Django 4.1.3 on 2023-05-01 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_messages', '0002_message_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='last_message_text',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='last_chat', to='my_messages.message'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chat',
            name='messages',
            field=models.ManyToManyField(blank=True, null=True, related_name='chat', to='my_messages.message'),
        ),
    ]
