# Generated by Django 2.2 on 2020-03-17 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxyManager', '0003_auto_20200316_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxy',
            name='source',
            field=models.CharField(max_length=35, null=True, verbose_name='来源'),
        ),
    ]