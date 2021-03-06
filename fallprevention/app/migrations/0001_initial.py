# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DummyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dummy_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medication_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('question_score', models.IntegerField(default=1)),
                ('question_key', models.BooleanField(default=False)),
                ('question_why', models.CharField(max_length=200)),
                ('question_answer', models.BooleanField(default=False)),
            ],
        ),
    ]
