# Generated by Django 4.2.10 on 2024-03-24 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0015_remove_order_price_alter_order_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="phone_number",
            field=models.TextField(blank=True, max_length=10),
        ),
    ]