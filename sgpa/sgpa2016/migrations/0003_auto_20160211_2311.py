# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgpa2016', '0002_roles_observacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles_Usuarios',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('roles', models.ForeignKey(to='sgpa2016.Roles')),
                ('usuario', models.ForeignKey(to='sgpa2016.Usuarios')),
            ],
        ),
        migrations.AddField(
            model_name='usuarios',
            name='roles',
            field=models.ManyToManyField(to='sgpa2016.Roles', through='sgpa2016.Roles_Usuarios'),
        ),
    ]
