# Generated by Django 4.2.10 on 2024-03-24 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0014_order_full_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="price",
        ),
        migrations.AlterField(
            model_name="order",
            name="date",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app.product"
            ),
        ),
    ]
