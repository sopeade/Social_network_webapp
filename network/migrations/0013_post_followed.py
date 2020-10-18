# Generated by Django 3.0.6 on 2020-07-17 01:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_auto_20200716_0157'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='followed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followed', to=settings.AUTH_USER_MODEL),
        ),
    ]