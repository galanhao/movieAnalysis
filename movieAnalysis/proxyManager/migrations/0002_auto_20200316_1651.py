# Generated by Django 2.2 on 2020-03-16 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxyManager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxy',
            name='source',
            field=models.CharField(max_length=20, null=True, verbose_name='来源'),
        ),
    ]