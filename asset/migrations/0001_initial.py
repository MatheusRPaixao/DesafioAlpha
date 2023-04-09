# Generated by Django 4.1.7 on 2023-04-08 03:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=40, unique=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('current_price', models.FloatField(default=0)),
                ('lowest_price', models.FloatField(null=True)),
                ('highest_price', models.FloatField(null=True)),
                ('update_period', models.IntegerField()),
                ('tunnel_top', models.FloatField(default=0)),
                ('tunnel_bottom', models.FloatField(default=0)),
                ('schedule_running', models.BooleanField(default=False)),
                ('top_breach', models.BooleanField(default=False)),
                ('bottom_breach', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
