# Generated by Django 4.2.6 on 2024-01-09 16:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("produits_app", "0023_alter_fournisseur_produits"),
    ]

    operations = [
        migrations.AddField(
            model_name="panier",
            name="date_expiration",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
