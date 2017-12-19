# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-15 14:28
from __future__ import unicode_literals

import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa_stripe', '0018_stripecard'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripecard',
            name='is_created_at_stripe',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stripecard',
            name='stripe_js_response',
            field=jsonfield.fields.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='stripecharge',
            name='stripe_refund_id',
            field=models.CharField(blank=True, db_index=True, max_length=255),
        ),
    ]