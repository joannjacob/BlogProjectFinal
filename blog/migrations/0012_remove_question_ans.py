# Generated by Django 2.0 on 2018-05-10 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_question_ans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='ans',
        ),
    ]
