# Generated by Django 5.0.4 on 2024-04-29 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_agencyprofile_contact_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='influencerprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='influencerprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='influencerprofile',
            name='last_name',
        ),
    ]
