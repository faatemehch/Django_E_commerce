# Generated by Django 2.0.3 on 2022-05-28 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_module', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='price',
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='final_price',
            field=models.IntegerField(blank=True, help_text='the price will fix after payment', null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='province',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
