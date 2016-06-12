# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-06 14:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL("""CREATE EXTENSION IF NOT EXISTS "uuid-ossp";"""),
        migrations.RunSQL("""CREATE EXTENSION IF NOT EXISTS ltree;"""),
        #migrations.RunSQL("CREATE INDEX IF NOT EXISTS restapi_share_tree_path_6dcc1339 ON restapi_share_tree USING GIST(path);"),
    ]
