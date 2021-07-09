# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iss', '0003_auto_20151111_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='primary_email',
            field=models.CharField(max_length=256, blank=True),
        ),
    ]
