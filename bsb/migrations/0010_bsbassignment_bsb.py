# Generated by Django 4.1.3 on 2023-04-06 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bsb', '0009_bsbquiz_bsbassignment_ball_bsbquiztests_bsbquizball'),
    ]

    operations = [
        migrations.AddField(
            model_name='bsbassignment',
            name='Bsb',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='bsb.bsb'),
            preserve_default=False,
        ),
    ]
