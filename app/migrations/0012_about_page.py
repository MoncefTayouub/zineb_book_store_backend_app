# Generated by Django 3.2.5 on 2023-03-29 09:36

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_book_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='about_page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField()),
                ('content', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True)),
            ],
        ),
    ]
