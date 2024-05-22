# Generated by Django 5.0.4 on 2024-05-14 06:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_delete_locationinfo'),
        ('services', '0006_delete_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_title', models.CharField(max_length=255)),
                ('delivery_date', models.DateField()),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('pending', 'Pending'), ('in_progress', 'In Progress'), ('reported', 'Reported'), ('canceled', 'Canceled'), ('job_done', 'Job Done')], default='pending', max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ordered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.userprofile')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service')),
            ],
        ),
    ]
