# Generated by Django 5.1.6 on 2025-03-08 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbackApp', '0007_alter_customuser_yurt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='yurt',
            field=models.TextField(default='yurtsuz'),
        ),
    ]
