# Generated by Django 4.1.3 on 2023-04-08 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bsb', '0010_bsbassignment_bsb'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studentanswerball',
            options={'ordering': ('-ball',)},
        ),
        migrations.RemoveField(
            model_name='bsbproblemball',
            name='bsb_problem',
        ),
        migrations.AddField(
            model_name='bsbproblemball',
            name='bsb_problem_answer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='balls', to='bsb.bsbproblemanswer'),
            preserve_default=False,
        ),
    ]