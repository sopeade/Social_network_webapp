# Generated by Django 3.0.6 on 2020-07-10 01:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_auto_20200709_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='listfollowed',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listfollowed',
            name='people_followed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='the_followed', to=settings.AUTH_USER_MODEL),
        ),
    ]
