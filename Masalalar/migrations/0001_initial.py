# Generated by Django 4.2.4 on 2023-08-18 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Masala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.IntegerField(choices=[(1, 'Beginner'), (2, 'Basic'), (3, 'Normal'), (4, 'Medium'), (5, 'Advanced'), (6, 'Hard'), (7, 'Extremal'), (8, 'For Expert')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('time_limit', models.PositiveIntegerField(default=1000)),
                ('memory_limit', models.PositiveIntegerField(default=6)),
                ('title', models.CharField(max_length=1000)),
                ('body', models.TextField()),
                ('slug', models.SlugField(max_length=40)),
                ('info_in', models.TextField(blank=True, null=True)),
                ('out', models.TextField(blank=True, null=True)),
                ('checker', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('masala', 'masala'), ('bir qator', 'bir qator'), ('bitta urinish', 'bitta urinish')], default='masala', max_length=40)),
                ('empty', models.BooleanField(default=True)),
                ('korinadigan_testlar', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='masalarim', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Urinish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tests', models.JSONField(blank=True, null=True)),
                ('turi', models.CharField(max_length=100)),
                ('time', models.CharField(max_length=3423)),
                ('memory', models.CharField(max_length=34234)),
                ('olcham', models.IntegerField()),
                ('til', models.CharField(choices=[('python', 'python')], max_length=213)),
                ('masala', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urinishlar', to='Masalalar.masala')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='masala_urinishlari', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Testlar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_in', models.TextField(max_length=100000000000)),
                ('out', models.TextField(max_length=100000000000)),
                ('masala', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testlar', to='Masalalar.masala')),
            ],
        ),
        migrations.CreateModel(
            name='MasalaTeg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tegs', to='Masalalar.masala')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Masalalar.teg')),
            ],
        ),
        migrations.CreateModel(
            name='Likelar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('masala', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lieks', to='Masalalar.masala')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='masala_like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
