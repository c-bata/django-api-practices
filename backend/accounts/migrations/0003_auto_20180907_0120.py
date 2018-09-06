# Generated by Django 2.1.1 on 2018-09-06 16:20

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180906_0312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. English lower alphabets, digits and hyphen only.', max_length=150, unique=True, validators=[accounts.validators.UsernameValidator()], verbose_name='username'),
        ),
    ]