# Generated by Django 4.0 on 2022-01-03 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_module', '0005_alter_orderdetail_count_alter_orderdetail_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]
