# Generated by Django 4.2.6 on 2023-12-19 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits_app', '0004_rename_historique_commandes_client_historique_panier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='image',
            field=models.ImageField(upload_to='produits_app/static/images'),
        ),
    ]