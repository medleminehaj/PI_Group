# Generated by Django 4.2.6 on 2024-01-09 16:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("produits_app", "0024_panier_date_expiration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="panier",
            name="date_expiration",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
