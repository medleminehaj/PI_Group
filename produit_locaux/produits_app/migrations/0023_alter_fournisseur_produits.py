# Generated by Django 4.2.6 on 2024-01-06 21:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("produits_app", "0022_alter_compte_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fournisseur",
            name="produits",
            field=models.ManyToManyField(blank=True, to="produits_app.produit"),
        ),
    ]