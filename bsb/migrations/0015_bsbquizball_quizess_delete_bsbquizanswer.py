# Generated by Django 4.1.3 on 2023-04-17 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bsb', '0014_bsbquizanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='bsbquizball',
            name='quizess',
            field=models.ManyToManyField(related_name='quiz_answers', to='bsb.bsbquiztests'),
        ),
        migrations.DeleteModel(
            name='BsbQuizAnswer',
        ),
    ]
