# Generated by Django 4.0 on 2021-12-31 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0017_visited_ip_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visited_ip_product',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product_module.product'),
        ),
    ]
