# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-06 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa_stripe', '0018_stripecustomer_sources'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripecustomer',
            name='default_source',
            field=models.CharField(blank=True, help_text='ID of default source from Stripe', max_length=255),
        ),
    ]
