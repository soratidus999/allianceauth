# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 02:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('optimer', '0003_make_strings_more_stringy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optimer',
            name='eve_character',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eveonline.EveCharacter'),
        ),
    ]
