# Generated by Django 4.2.6 on 2023-12-29 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits_app', '0008_alter_commentaire_evaluation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaire',
            name='evaluation',
            field=models.FloatField(),
        ),
    ]
