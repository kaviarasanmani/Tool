# Generated by Django 5.0.4 on 2024-05-21 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_delete_locationinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencerprofile',
            name='youtube_link',
            field=models.CharField(blank=True, max_length=20, verbose_name='Youtube link'),
        ),
    ]
