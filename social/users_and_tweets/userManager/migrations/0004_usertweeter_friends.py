# Generated by Django 3.0.3 on 2020-04-14 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userManager', '0003_usertweeter'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertweeter',
            name='friends',
            field=models.TextField(default=''),
        ),
    ]