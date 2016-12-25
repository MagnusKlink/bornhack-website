# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-24 22:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('camps', '0010_auto_20161220_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('headline', models.CharField(help_text='The headline of this info category', max_length=100)),
                ('anchor', models.SlugField(help_text='The HTML anchor to use for this info category.')),
                ('weight', models.PositiveIntegerField(help_text='Determines sorting/ordering. Heavier categories sink to the bottom. Categories with the same weight are ordered alphabetically.')),
                ('camp', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='infocategories', to='camps.Camp')),
            ],
            options={
                'ordering': ['-weight', 'headline'],
            },
        ),
        migrations.CreateModel(
            name='InfoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('headline', models.CharField(help_text='Headline of this info item.', max_length=100)),
                ('anchor', models.SlugField(help_text='The HTML anchor to use for this info item.')),
                ('body', models.TextField(help_text='Body of this info item. Markdown is supported.')),
                ('weight', models.PositiveIntegerField(help_text='Determines sorting/ordering. Heavier items sink to the bottom. Items with the same weight are ordered alphabetically.')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='infoitems', to='info.InfoCategory')),
            ],
            options={
                'ordering': ['-weight', 'headline'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='infoitem',
            unique_together=set([('headline', 'category'), ('anchor', 'category')]),
        ),
        migrations.AlterUniqueTogether(
            name='infocategory',
            unique_together=set([('headline', 'camp'), ('anchor', 'camp')]),
        ),
    ]
