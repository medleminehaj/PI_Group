# Generated by Django 4.2.6 on 2023-12-29 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits_app', '0009_alter_commentaire_evaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='panier',
            name='quantite',
            field=models.IntegerField(default=1),
        ),
    ]
