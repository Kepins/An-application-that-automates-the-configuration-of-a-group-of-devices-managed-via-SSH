# Generated by Django 4.2.3 on 2023-10-26 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='key_pair',
        ),
    ]