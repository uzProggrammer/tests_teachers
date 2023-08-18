# Generated by Django 4.1.3 on 2023-04-25 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bsb', '0020_remove_bsb_problem_ball'),
    ]

    operations = [
        migrations.CreateModel(
            name='Yakuniy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball', models.FloatField()),
                ('bsb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='yakuniy', to='bsb.bsb')),
            ],
        ),
    ]