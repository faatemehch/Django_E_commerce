# Generated by Django 3.2.12 on 2022-03-22 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('fax', models.CharField(max_length=50)),
                ('address', models.TextField()),
            ],
        ),
    ]
