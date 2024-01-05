from django.urls import path
from . import views

urlpatterns = [
    # Login
    path('',views.login,name="login"),
    path('logout_view/',views.logout_view,name="logout_view"),
    path('creercompte',views.creercompte,name="creercompte"),

    # ========Admin client==================
    path('affiche_client',views.affiche_client,name="affiche_client"),
    path('info_client/',views.info_client,name="info_client"),
    path('ajouter_client/',views.ajouter_client,name="ajouter_client"),
    path('suprimer_client/<int:id_client>', views.suprimer_client, name="suprimer_client"),
    path('modifier_client/<int:id_client>', views.modifier_client, name="modifier_client"),

    # ==============Admin fournisseur==============
    path('affiche_fournisseur/',views.affiche_fournisseur,name="affiche_fournisseur"),
    path('ajouter_fournisseur/',views.ajouter_fournisseur,name="ajouter_fournisseur"),
    path('supprimer_fournisseur/<int:id_fournisseur>',views.supprimer_fournisseur,name="supprimer_fournisseur"),
    path('modifier_fournisseur/<int:id_fournisseur>',views.modifier_fournisseur,name="modifier_fournisseur"),


    # ==============Admin categorie==============
    path('affiche_categorie/',views.affiche_categorie,name="affiche_categorie"),
    path('ajouter_categorie/',views.ajouter_categorie,name="ajouter_categorie"),
    path('supprimer_categorie/<int:id_categorie>',views.supprimer_categorie,name="supprimer_categorie"),
    path('modifier_categorie/<int:id_categorie>',views.modifier_categorie,name="modifier_categorie"),


    #=============Admin produits==============
    path('affiche_produits/',views.affiche_produits,name="affiche_produits"),
    path('ajouter_produit/',views.ajouter_produit,name="ajouter_produit"),
    path('suprimer_produit/<int:id_produit>',views.suprimer_produit,name="suprimer_produit"),
    path('modifier_produit/<int:id_produit>', views.modifier_produit, name="modifier_produit"),


    #=============Admin comptes==============
    path('affiche_compte/',views.affiche_compte,name="affiche_compte"),
    path('ajouter_compte/',views.ajouter_compte,name="ajouter_compte"),
    path('supprimer_compte/<int:id_compte>',views.supprimer_compte,name="supprimer_compte"),
    path('modifier_compte/<int:id_compte>',views.modifier_compte,name="modifier_compte"),

    # =============Admin panier==============
    path('affiche_panier/', views.affiche_panier, name="affiche_panier"),
    path('ajouter_panier/',views.ajouter_panier,name="ajouter_panier"),
    path('modifier_panier/<int:id_panier>',views.modifier_panier,name="modifier_panier"),
    path('suprimer_panier/<int:id_panier>',views.suprimer_panier,name="suprimer_panier"),

    #=============Admin commentaire==============
    path('affiche_commentaire/',views.affiche_commentaire,name="affiche_commentaire"),
    path('ajouter_commentaire/',views.ajouter_commentaire,name="ajouter_commentaire"),
    path('supprimer_commentaire/<int:id_commentaire>',views.supprimer_commentaire,name="supprimer_commentaire"),
    path('modifier_commentaire/<int:id_commentaire>',views.modifier_commentaire,name="modifier_commentaire"),

    #=============Admin commandeProduit==============
    path('affiche_commandeProduit/',views.affiche_commandeProduit,name="affiche_commandeProduit"),
    path('ajouter_commandeProduit/',views.ajouter_commandeProduit,name="ajouter_commandeProduit"),
    path('suprimer_commandeProduit/<int:id_commande>',views.suprimer_commandeProduit,name="suprimer_commandeProduit"),
    path('modifier_commandeProduit/<int:id_commande>', views.modifier_commandeProduit, name="modifier_commandeProduit"),

    #=============Client home=========================

    path("index/", views.index, name="index"),
    path("details_produit/<int:id>", views.details_produit, name="details_produit"),
    path('ajouter_commentaire_client/<int:produit_id>/<int:selected_rating>/', views.ajouter_commentaire_client,name='ajouter_commentaire_client'),
    path("ajouter_panier_client/<int:id>", views.ajouter_panier_client, name="ajouter_panier_client"),
    path("panier/", views.panier, name="panier"),
    path("vider_panier/", views.vider_panier, name="vider_panier"),
    path("suprimer_panier_client/<int:id>", views.suprimer_panier_client, name="suprimer_panier_client"),
    path("categories/", views.categories,name="categories"),
    path("produits_par_categorie/<str:nom_categorie>", views.produits_par_categorie, name='produits_par_categorie'),
    path("paiement/",views.paiement,name="paiement"),
    path("historique/",views.historique,name="historique"),
    path("details_historique/<int:id>",views.details_historique,name="details_historique"),
    path("vider_historique/",views.vider_historique,name="vider_historique"),


]