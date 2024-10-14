# Generated by Django 5.0.4 on 2024-05-02 10:13

import clubadmins.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clubs',
            fields=[
                ('id', clubadmins.models.CustomClubID(editable=False, max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('logo', models.URLField()),
                ('aboutus', models.TextField()),
                ('vision', models.TextField()),
                ('mission', models.TextField()),
                ('insta_link', models.URLField()),
                ('homephoto', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Admins',
            fields=[
                ('id', clubadmins.models.CustomAdminID(editable=False, max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('club_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubadmins.clubs')),
            ],
        ),
        migrations.CreateModel(
            name='CoreCommittee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('president', models.CharField(max_length=100)),
                ('vice_president', models.CharField(max_length=100)),
                ('treasurer', models.CharField(max_length=100)),
                ('club_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubadmins.clubs')),
            ],
        ),
    ]