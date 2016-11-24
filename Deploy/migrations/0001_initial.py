# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-24 10:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('DataBase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dns', models.CharField(max_length=20)),
                ('project', models.CharField(max_length=120)),
                ('createDate', models.DateTimeField(auto_now=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.Vendor')),
            ],
        ),
        migrations.CreateModel(
            name='DeployPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('compose', models.TextField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.Vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dns', models.CharField(max_length=20, unique=True)),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Deploy.Cluster')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='cluster',
            unique_together=set([('dns', 'project')]),
        ),
    ]
