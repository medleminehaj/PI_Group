from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Client)
admin.site.register(Categorie)
admin.site.register(CommandeProduit)
admin.site.register(Fournisseur)
admin.site.register(Produit)
admin.site.register(Commentaire)
admin.site.register(Compte)
admin.site.register(Panier)