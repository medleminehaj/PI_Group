# Generated by Django 4.2.6 on 2023-12-21 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits_app', '0005_alter_produit_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='image',
            field=models.ImageField(upload_to='produits_app/static/images/'),
        ),
    ]