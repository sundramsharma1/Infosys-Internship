# Generated by Django 5.0.4 on 2024-04-19 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sweetspot_app', '0002_remove_user_isactive_alter_user_mobileno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobileNo',
            field=models.CharField(max_length=10),
        ),
    ]
