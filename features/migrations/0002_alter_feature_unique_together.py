# Generated by Django 3.2.4 on 2021-06-22 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='feature',
            unique_together=set(),
        ),
    ]