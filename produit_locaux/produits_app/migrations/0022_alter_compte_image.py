# Generated by Django 4.2.6 on 2024-01-05 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits_app', '0021_alter_compte_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compte',
            name='image',
            field=models.ImageField(default='produits_app/static/images/default_image.png', upload_to='produits_app/static/images/'),
        ),
    ]
