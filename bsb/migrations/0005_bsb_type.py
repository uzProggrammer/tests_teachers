# Generated by Django 4.1.3 on 2023-04-04 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bsb', '0004_alter_bsb_holati'),
    ]

    operations = [
        migrations.AddField(
            model_name='bsb',
            name='type',
            field=models.CharField(choices=[('Masala', 'Masala'), ('Topshiriq', 'Topshiriq'), ('Test', 'Test')], default='Topshiriq', max_length=20),
        ),
    ]
