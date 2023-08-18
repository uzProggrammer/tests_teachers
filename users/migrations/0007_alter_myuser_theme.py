# Generated by Django 4.1.3 on 2023-04-21 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_myuser_sinf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='theme',
            field=models.CharField(choices=[('default', 'dark'), ('light', 'light'), ('green', 'green'), ('black', 'black'), ('brown', 'brown')], default='light', max_length=30),
        ),
    ]