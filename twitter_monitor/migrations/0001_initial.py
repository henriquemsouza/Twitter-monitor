# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quali', models.CharField(default=b'sem', max_length=3)),
                ('data_pub', models.DateField(null=True, blank=True)),
                ('texto', models.TextField(max_length=200, null=True, blank=True)),
                ('nome_twi', models.CharField(max_length=100)),
                ('tag', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Monitoramento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('palavra', models.CharField(max_length=60)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='monit',
            field=models.ForeignKey(to='twitter_monitor.Monitoramento'),
        ),
    ]
