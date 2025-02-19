# Generated by Django 5.1.6 on 2025-02-19 22:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_party_rsvp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='party',
            name='dishes',
        ),
        migrations.AddField(
            model_name='dish',
            name='party',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main_app.party'),
            preserve_default=False,
        ),
    ]
