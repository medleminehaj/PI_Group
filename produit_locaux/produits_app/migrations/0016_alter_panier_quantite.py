# Generated by Django 4.2.6 on 2024-01-01 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits_app', '0015_alter_compte_image_alter_panier_quantite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panier',
            name='quantite',
            field=models.IntegerField(default=1),
        ),
    ]