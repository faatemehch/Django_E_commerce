# Generated by Django 2.0.3 on 2022-05-28 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0002_auto_20220223_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
