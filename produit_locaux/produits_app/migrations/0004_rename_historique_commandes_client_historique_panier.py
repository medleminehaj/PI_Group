# Generated by Django 4.2.4 on 2023-12-08 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produits_app', '0003_client_id_email_fournisseur_id_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='historique_commandes',
            new_name='historique',
        ),
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id_panier', models.AutoField(primary_key=True, serialize=False)),
                ('id_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits_app.client')),
                ('produits', models.ManyToManyField(to='produits_app.produit')),
            ],
        ),
    ]
