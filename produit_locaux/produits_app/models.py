from django.db import models

class Compte(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True,max_length=80)
    password = models.CharField(max_length=50)
    etat=models.CharField(max_length=20, default='active')
    image = models.ImageField(upload_to='produits_app/static/images/', default='produits_app/static/images/default_image.png')
    def __str__(self):
        return self.email


class Produit(models.Model):
    id_produit = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE)
    prix = models.FloatField()
    id_fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE)
    emplacement = models.CharField(max_length=100)
    date_publication = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='produits_app/static/images/')
    
class Fournisseur(models.Model):
    id_fournisseur = models.AutoField(primary_key=True)
    id_email = models.ForeignKey(Compte, on_delete=models.CASCADE, default=4) 
    nom_enterprise = models.CharField(max_length=100)
    num_tel = models.IntegerField(default=0)
    adresse = models.CharField(max_length=100, default='adresse')
    description = models.TextField()
    produits = models.ManyToManyField(Produit)

class CommandeProduit(models.Model):
    id_commande = models.AutoField(primary_key=True)
    produits = models.ManyToManyField(Produit)
    id_client = models.ForeignKey('Client', on_delete=models.CASCADE)
    date_commande = models.DateField()
    statut_commande = models.CharField(max_length=50)


class Categorie(models.Model):
    id_categorie = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    description = models.TextField()

class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    id_email = models.ForeignKey(Compte, on_delete=models.CASCADE, default=4)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, default='prenom_user')
    num_tel = models.IntegerField(default=0)
    adresse = models.CharField(max_length=100, default='adresse')
    historique = models.ManyToManyField(CommandeProduit,blank=True)
    
class Commentaire(models.Model):
    id_commentaire = models.AutoField(primary_key=True)
    id_produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    texte_commentaire = models.TextField()
    evaluation = models.FloatField()

class Panier(models.Model):
    id_panier = models.AutoField(primary_key=True)
    produits = models.ManyToManyField(Produit)
    quantite = models.JSONField(default=dict)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
