# Generated by Django 4.2.6 on 2024-01-01 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits_app', '0016_alter_panier_quantite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panier',
            name='quantite',
            field=models.JSONField(default=dict),
        ),
    ]
