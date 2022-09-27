# Generated by Django 3.2.6 on 2021-11-10 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0013_auto_20210817_1231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prices',
            options={'verbose_name_plural': 'Prices'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-pk'], 'verbose_name_plural': 'Projects'},
        ),
        migrations.AddField(
            model_name='news',
            name='telegram_status',
            field=models.CharField(choices=[('WAITING', 'Waiting'), ('PUBLISHED', 'Placed in feed'), ('IGNORE', 'Ignore post')], default='WAITING', max_length=50),
        ),
    ]
