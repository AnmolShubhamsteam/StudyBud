# Generated by Django 5.0.4 on 2024-05-01 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_room_host_alter_topic_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
    ]
