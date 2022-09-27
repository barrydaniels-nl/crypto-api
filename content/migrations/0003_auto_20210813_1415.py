# Generated by Django 3.2.6 on 2021-08-13 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20210813_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'NewsCategories',
            },
        ),
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='categories',
            field=models.ManyToManyField(to='content.NewsCategory'),
        ),
    ]
