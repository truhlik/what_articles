# Generated by Django 3.2.8 on 2021-10-13 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='name',
        ),
        migrations.AddField(
            model_name='tag',
            name='name_de',
            field=models.CharField(default='test', max_length=255, verbose_name='name de'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='name_en',
            field=models.CharField(default='test-de', max_length=255, verbose_name='name en'),
            preserve_default=False,
        ),
    ]
