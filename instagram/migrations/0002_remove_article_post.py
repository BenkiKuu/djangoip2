# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-27 11:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='post',
        ),
    ]