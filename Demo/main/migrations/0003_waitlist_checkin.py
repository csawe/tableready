# Generated by Django 3.2.12 on 2022-03-24 15:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_waitlist_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitlist',
            name='checkin',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 24, 18, 45, 36, 331965)),
            preserve_default=False,
        ),
    ]
