# Generated by Django 3.2.23 on 2024-10-30 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_subscription_subscribed'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='last_checkin',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
