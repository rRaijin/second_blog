# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-09 12:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment_commentator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commentator',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='commentator', to=settings.AUTH_USER_MODEL),
        ),
    ]
