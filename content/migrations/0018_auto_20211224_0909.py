# Generated by Django 3.2.6 on 2021-12-24 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0017_auto_20211224_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='newssources',
            name='article_selector_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
