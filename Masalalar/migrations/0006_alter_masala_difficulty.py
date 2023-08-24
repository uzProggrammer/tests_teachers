# Generated by Django 4.2.4 on 2023-08-20 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Masalalar', '0005_alter_masala_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masala',
            name='difficulty',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)], default=0),
        ),
    ]