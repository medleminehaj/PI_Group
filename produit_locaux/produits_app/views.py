from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from datetime import date
from .models import *
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password, make_password
from datetime import timedelta

# =======================login , logout and creercompte===============================================

#==========================Debut verification==================================

def generate_verification_code():
    return str(randint(100000, 999999))

def send_verification_email(to_email, verification_code):
    subject = 'Verification Code'
    message = f'Your verification code is: {verification_code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [to_email]
    send_mail(subject, message, from_email, recipient_list)

def verify(request):
    email = request.session.get('email')
    verification_code = request.session.get('verification_code')
    if not email or not verification_code :
        messages.error(request, 'Invalid verification session data.')
        return redirect('index')
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        if entered_code == verification_code:
            password = make_password(request.POST.get('password'))
            etat = request.session.get('etat')
            if not Compte.objects.filter(email=email).exists():
                compte = Compte(email=email, password=password, etat=etat)
                compte.save()
                request.session['compte'] = compte.id
                client_pardefaut=66
                request.session['client'] = client_pardefaut
                del request.session['email']
                del request.session['password']
                del request.session['etat']
                del request.session['verification_code']
                if etat == 'client':
                    client = Client(id_email=compte)
                    client.save()
                elif etat == 'fournisseur':
                    fournisseur = Fournisseur(id_email=compte)
                    fournisseur.save()
                messages.success(request, 'le compt et cree avec succ')
                return redirect('login')
            else:
                messages.error(request, "Account already exists. Please log in.")
                return redirect('login')
        else:
            messages.error(request, 'Invalid verification code.')
    return render(request, 'verification/verify.html', {'email': email, 'verification_code': verification_code})

#==========================End verification==================================
 
#==========================Mot de pass oublier==============================

def request_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_exists = Compte.objects.filter(email=email).exists()
        if user_exists:
            reset_code = generate_verification_code()
            request.session['reset_email'] = email
            request.session['reset_code'] = reset_code
            subject = 'Password Reset Code'
            message = f'Your password reset code is: {reset_code}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'Password reset code sent to your email.')
            return redirect(verify_password_reset)
        else:
            messages.error(request, 'Account with this email does not exist.')
            return redirect(request_password_reset)
    return render(request, 'verification/request_password_reset.html')

def verify_password_reset(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        expected_code = request.session.get('reset_code')
        if entered_code == expected_code:
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid verification code.')
            return redirect('verify_password_reset')
    return render(request, 'verification/verify_password_reset.html')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            email = request.session.get('reset_email')
            user = Compte.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            del request.session['reset_email']
            del request.session['reset_code']
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password')
    return render(request, 'verification/reset_password.html')

#=========================End Mot de pass oublier=========================

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        compte_existe = Compte.objects.get(email=email)
        if compte_existe and check_password(password, compte_existe.password):
            request.session['compte'] = compte_existe.id
            if compte_existe.etat == 'admin':
                return redirect('affiche_client')
            elif compte_existe.etat == 'fournisseur':
                return redirect('home')
            else:
                return redirect('index')
        messages.error(request, "L'email ou le mot de passe est incorrect")
        return redirect('login')
    return render(request, "login/login.html")

def logout_view(request):
    logout(request)
    request.session.clear()
    return redirect('login')

def creercompte(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        request.session['email'] = email
        password = make_password(request.POST.get('password'))
        etat = request.POST.get('etat')
        compte_existe = Compte.objects.filter(email=email)
        if not compte_existe.exists():
            code = generate_verification_code()
            send_verification_email(email, code)
            request.session['verification_code'] = code
            request.session['email'] = email
            request.session['password'] = password
            request.session['etat'] = etat
            return redirect('verify')
        messages.error(request, "Le compte déja existe")
        return redirect('login')
    return render(request,"login/creercompte.html")

# ==========================================end login , logout and creercompte==========================================

# ====================================Client===============================================

def gerer_voter_compt(request):
    compte_id = request.session.get('compte')
    if compte_id is not None:
        compte = Compte.objects.get(id=compte_id)
        client=Client.objects.get(id_email=compte_id)
        return render(request,"interface_client\gerer_voter_compt.html",{'compte':compte,'client':client})
    else:
        return redirect('index')

def info_client(request):
    return HttpResponse("info inserted succefuly")

def index(request):
    supprimer_paniers_expires()
    produits = Produit.objects.all().order_by('?')[:20]
    
    compte_id = request.session.get('compte')
    if compte_id is not None and compte_id != 66:
        compte = get_object_or_404(Compte, id=compte_id)
        client = get_object_or_404(Client, id_email=compte_id)

        return render(request, "interface_client/index.html", {
            "produits": produits,
            'page_actuelle': 'index',
            'compte': compte,
            'client': client,
        })
    else:
        request.session['code_client'] = 66
        compte = get_object_or_404(Compte, id=66)
        client = get_object_or_404(Client, id_email=66)
        return render(request, "interface_client/index.html", {
            "produits": produits,
            'page_actuelle': 'index',
            'compte': compte,
            'client': client,
        })
       
        

def calculer_le_quart(products):
    total_sum = 0
    produits = Produit.objects.all()
    for produit in produits :
        total_sum += 1
    quart_1 = int(total_sum * 0.25)
    quart_2 = int(total_sum * 0.5)
    quart_3 = int(total_sum * 0.75)
    quart_4 = int(total_sum)
    return quart_1, quart_2, quart_3, quart_4

def categories(request):
    compte_id = request.session.get('compte')
    if compte_id is not None:
        compte = Compte.objects.get(id=compte_id)
        view_option = request.GET.get('view', 12)  # Valeur par défaut '12' si le paramètre n'est pas présent
        derniers_produits = Produit.objects.order_by('?')[:int(view_option)]
        quart_1, quart_2, quart_3, quart_4 = calculer_le_quart(derniers_produits)
        categorie = Categorie.objects.all()
        client=Client.objects.get(id_email=compte_id)
        context = {
            'derniers_produits': derniers_produits,
            'categories': categorie,
            'view_option': view_option,
            'quarter_1': quart_1,
            'quarter_2': quart_2,
            'quarter_3': quart_3,
            'quarter_4': quart_4,
            'page_actuelle': 'categorie',
            'compte':compte,
            'client':client,
        }
        return render(request, 'interface_client/categorie.html', context)
    else:

        compte = Compte.objects.get(id=66)
        view_option = request.GET.get('view', 12)  # Valeur par défaut '12' si le paramètre n'est pas présent
        derniers_produits = Produit.objects.order_by('date_publication')[:int(view_option)]
        quart_1, quart_2, quart_3, quart_4 = calculer_le_quart(derniers_produits)
        categorie = Categorie.objects.all()
        client=Client.objects.get(id_email=compte_id)
        context = {
            'derniers_produits': derniers_produits,
            'categories': categorie,
            'view_option': view_option,
            'quarter_1': quart_1,
            'quarter_2': quart_2,
            'quarter_3': quart_3,
            'quarter_4': quart_4,
            'page_actuelle': 'categorie',
            'compte':compte,
            'client':client,
        }
        return render(request, 'interface_client/categorie.html', context)

        # Gérer le cas où le compte_id n'est pas présent dans la session
        # Vous pouvez rediriger l'utilisateur vers la page de connexion par exemple
        messages.error(request, "La session est invalide vieuller connecter.")
        return redirect('login')

def supprimer_paniers_expires():
    paniers_expires = Panier.objects.filter(date_expiration__lt=timezone.now())
    paniers_expires.delete()

def panier(request):
    compte_id = request.session.get('compte')
    if compte_id is not None:
        compte = Compte.objects.get(id=compte_id)
        client=Client.objects.get(id_email=compte)
        la_panier, created = Panier.objects.get_or_create(id_client=client)
        if created or la_panier.date_expiration is None:
            la_panier.date_expiration = timezone.now() + timezone.timedelta(days=30)
        la_panier.save()
        produits = la_panier.produits.all()
        client=Client.objects.get(id_email=compte_id)
        panier_items = [{'produit': produit, 'quantity': la_panier.quantite.get(str(produit.id_produit), 0)} for produit in
                        produits]
        somme = 0
        for item in panier_items:
            somme += item['produit'].prix * int(item['quantity'])
        return render(request, "interface_client/panier.html", {'produits': produits, 'panier_items': panier_items, 'somme': somme,'compte':compte,'page_actuelle' : 'panier','client':client})
    else:
        compte = Compte.objects.get(id=66)
        client=Client.objects.get(id_email=66)
        la_panier, created = Panier.objects.get_or_create(id_client=client)
        produits = la_panier.produits.all()
        client=Client.objects.get(id_email=compte_id)
        panier_items = [{'produit': produit, 'quantity': la_panier.quantite.get(str(produit.id_produit), 0)} for produit in  produits]
        somme = 0
        for item in panier_items:
            somme += item['produit'].prix * int(item['quantity'])
        return render(request, "interface_client/panier.html", {'produits': produits, 'panier_items': panier_items, 'somme': somme,'compte':compte,'page_actuelle' : 'panier','client':client})

def details_produit(request, id):
    compte_id = request.session.get('compte')
    if compte_id is not None:
        compte = get_object_or_404(Compte, id=compte_id)
        produit = Produit.objects.filter(id_produit=id).first()
        commentaires=Commentaire.objects.filter(id_produit=id)
        client=Client.objects.get(id_email=compte_id)
        moyenne = 0.0
        evaluations = [com.evaluation for com in commentaires]
        if evaluations:
            moyenne = sum(evaluations) / len(evaluations)

        return render(request, "interface_client/details_produit.html", {'produit': produit,'commentaires':commentaires,'moyenne':moyenne,'compte':compte,'client':client})
    else:
        compte = get_object_or_404(Compte, id=66)
        produit = Produit.objects.filter(id_produit=id).first()
        commentaires=Commentaire.objects.filter(id_produit=id)
        client=Client.objects.get(id_email=66)
        moyenne = 0.0
        evaluations = [com.evaluation for com in commentaires]
        if evaluations:
            moyenne = sum(evaluations) / len(evaluations)
        return render(request, "interface_client/details_produit.html", {'produit': produit,'commentaires':commentaires,'moyenne':moyenne,'compte':compte,'client':client})
     
def ajouter_commentaire_client(request,produit_id,selected_rating):
    compte_id = request.session.get('compte')
    if compte_id is not None:
        client = Client.objects.get(id_email=compte_id)
        texte_commentaire = request.POST.get('nouveau_commentaire')
        commentaire = Commentaire(id_produit_id=produit_id, id_client_id=client.id_client, texte_commentaire=texte_commentaire,evaluation=selected_rating)
        commentaire.save()
        return redirect(f'/details_produit/{produit_id}')
    else:
        client = Client.objects.get(id_email=66)
        texte_commentaire = request.POST.get('nouveau_commentaire')
        commentaire = Commentaire(id_produit_id=produit_id, id_client_id=client.id_client, texte_commentaire=texte_commentaire,evaluation=selected_rating)
        commentaire.save()
        return redirect(f'/details_produit/{produit_id}')
    
def ajouter_panier_client(request, id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        produit = Produit.objects.get(id_produit=id)
        compte_id = request.session.get('compte')
        if compte_id is not None:
            compte = get_object_or_404(Compte, id=compte_id)
            client = get_object_or_404(Client, id_email=compte)
            panier, created = Panier.objects.get_or_create(id_client=client)
            panier.produits.add(produit)
            panier.quantite[str(produit.id_produit)] = quantity
            panier.save()
            return redirect(f'/details_produit/{id}')
        else:
            compte = get_object_or_404(Compte, id=66)
            client = get_object_or_404(Client, id_email=66)
            panier, created = Panier.objects.get_or_create(id_client=client)
            panier.produits.add(produit)
            panier.quantite[str(produit.id_produit)] = quantity
            panier.save()
            return redirect(f'/details_produit/{id}')
    else:
        return HttpResponse("Invalid request method")


def suprimer_panier_client(request, id):
    compte_id = request.session.get('compte')
    if compte_id is not None:
        client = Client.objects.get(id_email=compte_id)
        produit = get_object_or_404(Produit, id_produit=id)
        la_panier, created = Panier.objects.get_or_create(id_client=client.id_client)
        la_panier.produits.remove(produit)
        return redirect(panier)
    else:
        client = Client.objects.get(id_email=66)
        produit = get_object_or_404(Produit, id_produit=id)
        la_panier, created = Panier.objects.get_or_create(id_client=client.id_client)
        la_panier.produits.remove(produit)
        return redirect(panier)


def vider_panier(request):
    compte_id = request.session.get('compte')
    if compte_id is not None:
        client = Client.objects.get(id_email=compte_id)
        la_panier, created = Panier.objects.get_or_create(id_client=client.id_client)
        la_panier.produits.clear()
        return redirect(panier)
    else:
        client = Client.objects.get(id_email=66)
        la_panier, created = Panier.objects.get_or_create(id_client=client.id_client)
        la_panier.produits.clear()
        return redirect(panier)


def produits_par_categorie(request, nom_categorie):
    compte_id = request.session.get('compte')
    if compte_id is not None:
        compte = Compte.objects.get(id=compte_id)
        view_option = request.GET.get('view', 12)
        categorie1 = get_object_or_404(Categorie, nom=nom_categorie)
        categories=Categorie.objects.all()
        produits = Produit.objects.filter(categorie=categorie1)[:int(view_option)]
        quarter_1, quarter_2, quarter_3, quarter_4 = calculer_le_quart(produits)
        client=Client.objects.get(id_email=compte_id)
        context = {
            'categorie1': categorie1,
            'produits': produits,
            'categories':categories,
            'nom':nom_categorie,
            'view_option': view_option,
            'quarter_1': quarter_1,
            'quarter_2': quarter_2,
            'quarter_3': quarter_3,
            'quarter_4': quarter_4,
            'compte':compte,
            'client':client,
        }
        return render(request, 'interface_client/produits_par_categorie.html', context)
    else:
        compte = Compte.objects.get(id=66)
        view_option = request.GET.get('view', 12)
        categorie1 = get_object_or_404(Categorie, nom=nom_categorie)
        categories=Categorie.objects.all()
        produits = Produit.objects.filter(categorie=categorie1)[:int(view_option)]
        quarter_1, quarter_2, quarter_3, quarter_4 = calculer_le_quart(produits)
        client=Client.objects.get(id_email=66)
        context = {
            'categorie1': categorie1,
            'produits': produits,
            'categories':categories,
            'nom':nom_categorie,
            'view_option': view_option,
            'quarter_1': quarter_1,
            'quarter_2': quarter_2,
            'quarter_3': quarter_3,
            'quarter_4': quarter_4,
            'compte':compte,
            'client':client,
        }
        
        return render(request, 'interface_client/produits_par_categorie.html', context)

def paiement(request):
    compte_id = request.session.get('compte')
    compte = Compte.objects.get(id=compte_id)
    client = Client.objects.get(id_email=compte_id)
    la_panier, created = Panier.objects.get_or_create(id_client=client)
    if not la_panier.produits.exists():
        return HttpResponse("Le panier est vide. Vous ne pouvez pas passer une commande sans produits.")
    nouvelle_commande = CommandeProduit.objects.create(
        id_client_id=client.id_client,
        date_commande=timezone.now(),
        statut_commande='En cours'
    )
    nouvelle_commande.produits.set(la_panier.produits.all())
    nouvelle_commande.save()
    client.historique.add(nouvelle_commande)
    la_panier.delete()
    return redirect('panier')


def historique(request):
    compte_id = request.session.get('compte')
    if compte_id is not None:
        compte = Compte.objects.get(id=compte_id)
        client = Client.objects.get(id_email=compte_id)
        historique = CommandeProduit.objects.filter(id_client=client).order_by('-date_commande')
        client=Client.objects.get(id_email=compte_id)
        return render(request, 'interface_client/historique.html', {'historique': historique,'compte':compte,'page_actuelle':'historique','client':client})
    else:
        # Gérer le cas où le compte_id n'est pas présent dans la session
        # Vous pouvez rediriger l'utilisateur vers la page de connexion par exemple
        messages.error(request, "La session est invalide veiuller connecter.")
        return redirect('login')


def details_historique(request,id):
    compte_id = request.session.get('compte')
    if compte_id is not None:
        compte = Compte.objects.get(id=compte_id)
        client = Client.objects.get(id_email=compte_id)
        if not client.id_client:
            return HttpResponse("Vous n'êtes pas connecté.")
        try:
            client = Client.objects.get(id_client=client.id_client)
        except Client.DoesNotExist:
            return HttpResponse("Client non trouvé.")
        historique_commandes = CommandeProduit.objects.filter(id_client=client.id_client).order_by('-date_commande')
        produits_de_commande = []
        for commande in historique_commandes:
            if commande.id_commande == id:
                produits_de_commande = commande.produits.all()
                break
        return render(request, 'interface_client/details_historique.html', {'produits': produits_de_commande,'compte':compte})
    else:
        # Gérer le cas où le compte_id n'est pas présent dans la session
        # Vous pouvez rediriger l'utilisateur vers la page de connexion par exemple
        messages.error(request, "La session est invalide veiuller connecter.")
        return redirect('login')
    
def vider_historique(request):
    compte_id = request.session.get('compte')
    if compte_id is not None:
        try:
            compte = Compte.objects.get(id=compte_id)
            client = Client.objects.get(id_email=compte)
            CommandeProduit.objects.filter(id_client=client).delete()
            
        except (Compte.DoesNotExist, Client.DoesNotExist) as e:
            print(f"Erreur: {e}")
    else:
        print("Erreur: Le compte_id n'est pas présent dans la session.")
    return redirect('historique')

def modifier_compte_client(request,id):
    compte = get_object_or_404(Compte, id=id)
    client = Client.objects.get(id_email=id)
    if request.method == 'POST':
        client.nom = request.POST.get('nom')
        client.prenom = request.POST.get('prenom')
        client.num_tel = request.POST.get('num_tel')
        client.adresse = request.POST.get('adresse')
        client.save()
        if 'image' in request.FILES:
            compte.image = request.FILES['image']
        else:
            pass
        compte.save()
        return redirect('index')


# ==========================================end client==========================================

# =======================Admin Client===============================================
def affiche_client(request):
    clients = Client.objects.all()
    return render(request,"interface_admin/Admin_Client/client_affichage.html",{'clients':clients})

def ajouter_client(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = make_password(request.POST.get('password'))
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        num_tel = request.POST.get('num_tel')
        adresse = request.POST.get('adresse')
        compte_existe = Compte.objects.filter(email=email)
        if not compte_existe.exists():
            compte = Compte(email=email, password=password, etat="client")
            compte.save()
            client = Client(id_email=compte,nom=nom,prenom=prenom,num_tel=num_tel,adresse=adresse)
            client.save()
            return redirect('affiche_client')
        messages.error(request, "Le compte déja existe")
        return redirect('ajouter_client')
    Comptes = Compte.objects.filter(etat='client')
    return render(request,"interface_admin/Admin_Client/client_ajout.html",{'Comptes':Comptes})


def modifier_client(request, id_client):
    client = get_object_or_404(Client, id_client=id_client)
    if request.method == 'POST':
        client.nom = request.POST.get('nom')
        client.prenom = request.POST.get('prenom')
        client.num_tel = request.POST.get('num_tel')
        client.adresse = request.POST.get('adresse')
        client.save()
        return redirect('affiche_client')
    return render(request,"interface_admin/Admin_Client/client_modification.html", {'client': client})


def suprimer_client(request,id_client):
    objet = get_object_or_404(Client, id_client=id_client)
    if request.method == 'GET':
        objet.delete()
        return redirect('affiche_client')
    return HttpResponse("erreur")

# ==========================================end admin client==========================================



# =======================Admin Fournisseur===============================================

def affiche_fournisseur(request):
    produits=Produit.objects.all()
    fournisseurs = Fournisseur.objects.all()
    return render(request,"interface_admin/Admin_Fournisseur/fournisseur_affichage.html",{'fournisseurs':fournisseurs,'produits':produits})

def ajouter_fournisseur(request):
    if request.method == 'POST':
        Nom = request.POST.get('nom')
        num_tel = request.POST.get('num_tel')
        adresse = request.POST.get('adresse')
        description = request.POST.get('description')
        email = request.POST.get('email')
        mot_de_passe = make_password(request.POST.get('mot_de_passe'))
        etat = 'fournisseur'
        compte_existe = Compte.objects.filter(email=email)

        if not compte_existe.exists():
            compte = Compte(email=email, password=mot_de_passe, etat=etat)
            compte.save()

            fournisseur = Fournisseur(id_email=compte, nom_enterprise=Nom, num_tel=num_tel, adresse=adresse, description=description)
            fournisseur.save()

            return redirect('affiche_fournisseur')
        else:
            messages.error(request, "Le compte déjà existe")
            return redirect('ajouter_fournisseur')

    return render(request, "interface_admin/Admin_Fournisseur/fournisseur_ajout.html")


def modifier_fournisseur(request, id_fournisseur):
    fournisseur = get_object_or_404(Fournisseur, id_fournisseur=id_fournisseur)
    produits = Produit.objects.all()
    if request.method == 'POST':
        fournisseur.nom_enterprise = request.POST.get('nom')
        fournisseur.num_tel = request.POST.get('num_tel')
        fournisseur.adresse = request.POST.get('adresse')
        fournisseur.description = request.POST.get('description')
        fournisseur.save()
        return redirect('affiche_fournisseur')
    return render(request, 'interface_admin/Admin_Fournisseur/fournisseur_modification.html', {'fournisseur': fournisseur,'produits':produits})


def supprimer_fournisseur(request,id_fournisseur):
    objet = get_object_or_404(Fournisseur, id_fournisseur=id_fournisseur)
    if request.method == 'GET':
        objet.delete()
        return redirect('affiche_fournisseur')
    return HttpResponse("erreur")

# ==========================================end admin fournisseur==========================================






# =======================Admin categorie===============================================

def affiche_categorie(request):
    categories = Categorie.objects.all()
    return render(request,"interface_admin/Admin_categorie/categorie_affichage.html",{'categories':categories})

def ajouter_categorie(request):
    if request.method == 'POST':
        Nom = request.POST.get('nom')
        description = request.POST.get('description')
        categorie = Categorie(nom=Nom, description=description)
        categorie.save()
        return redirect('affiche_categorie')
    return render(request, "interface_admin/Admin_categorie/categorie_ajout.html")


def modifier_categorie(request, id_categorie):
    categorie = get_object_or_404(Categorie , id_categorie=id_categorie)
    if request.method == 'POST':
        categorie.nom = request.POST.get('nom')
        categorie.description = request.POST.get('description')
        categorie.save()
        return redirect('affiche_categorie')
    return render(request, 'interface_admin/Admin_categorie/categorie_modification.html', {'categorie': categorie})


def supprimer_categorie(request,id_categorie):
    objet = get_object_or_404(Categorie, id_categorie=id_categorie)
    if request.method == 'GET':
        objet.delete()
        return redirect('affiche_categorie')
    return HttpResponse("erreur")

# ==========================================end admin Catagorie==========================================

# =======================Admin Produits===============================================

def affiche_produits(request):
    produits = Produit.objects.all()
    return render(request,"interface_admin/Admin_Produits/produits_affichage.html",{'produits':produits})

def ajouter_produit(request):
    if request.method == 'POST':
        id_fournisseur_id=request.POST.get('fournisseur')
        categorie_id=request.POST.get('categorie')
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        prix = request.POST.get('prix')
        emplacement = request.POST.get('emplacement')
        image =request.FILES['image']
        produit = Produit(nom=nom, description=description,categorie_id=categorie_id, prix=prix,id_fournisseur_id=id_fournisseur_id, emplacement=emplacement,image=image)
        produit.save()
        return redirect('affiche_produits')
    fournisseurs = Fournisseur.objects.all()
    categories = Categorie.objects.all()
    return render(request, "interface_admin/Admin_Produits/produits_ajout.html",{'fournisseurs':fournisseurs,'categories':categories})

def modifier_produit(request, id_produit):
    produit = get_object_or_404(Produit, id_produit=id_produit)
    if request.method == 'POST':
        produit.id_fournisseur_id = request.POST.get('fournisseur')
        produit.categorie_id = request.POST.get('categorie')
        produit.nom = request.POST.get('nom')
        produit.description = request.POST.get('description')
        produit.prix = request.POST.get('prix')
        produit.emplacement = request.POST.get('emplacement')
        if 'image' in request.FILES:
            produit.image = request.FILES['image']
        else:
            pass

        produit.save()
        return redirect('affiche_produits')
    fournisseurs = Fournisseur.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'interface_admin/Admin_Produits/produits_modification.html', {'produit': produit,'fournisseurs':fournisseurs,'categories':categories})



def suprimer_produit(request,id_produit):
    objet = get_object_or_404(Produit, id_produit=id_produit)
    if request.method == 'GET':
        objet.delete()
        return redirect('affiche_produits')
    return HttpResponse("erreur")

# ==========================================end admin Produits==========================================

# =======================Admin compte===============================================

def affiche_compte(request):
    comptes = Compte.objects.all()
    return render(request,"interface_admin/Admin_compte/compte_affichage.html",{'comptes':comptes})

def ajouter_compte(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = make_password(request.POST.get('password'))
        etat=request.POST.get('etat')
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image = 'produits_app/static/images/default_image.png'
        compte_existe = Compte.objects.filter(email=email)
        if compte_existe.exists():
            redirect(ajouter_compte)
        else:
            compte = Compte(email=email, password=password, etat=etat, image=image)
            compte.save()
            return redirect('affiche_compte')
        messages.error(request, "L'email deja exite , saisir un autre ...")
    return render(request, "interface_admin/Admin_compte/compte_ajout.html")


def modifier_compte(request, id_compte):
    compte = get_object_or_404(Compte , id=id_compte)
    if request.method == 'POST':
        compte.email = request.POST.get('email')
        compte.etat = request.POST.get('etat')
        if 'image' in request.FILES:
            compte.image = request.FILES['image']
        else:
            pass
        compte.save()
        return redirect('affiche_compte')
    return render(request, 'interface_admin/Admin_compte/compte_modification.html', {'compte': compte})


def supprimer_compte(request,id_compte):
    objet = get_object_or_404(Compte, id=id_compte)
    if request.method == 'GET':
        objet.delete()
        return redirect('affiche_compte')
    return HttpResponse("erreur")

# ==========================================end admin compte==========================================


# =======================Admin panier===============================================

def affiche_panier(request):
    paniers = Panier.objects.all()
    return render(request,"interface_admin/Admin_Panier/panier_affichage.html",{'paniers':paniers})

def ajouter_panier(request):
    if request.method == 'POST':
        id_client=request.POST.get('id_client')
        id_produit=request.POST.get('id_produit')
        quantite=request.POST.get('quantite')
        client = get_object_or_404(Client, id_client=id_client)
        panier = Panier.objects.create(id_client=client)
        product_ids = request.POST.getlist('id_produit')
        for product_id in product_ids:
            produit = get_object_or_404(Produit, id_produit=product_id)
            panier.produits.add(produit)
        panier.save()
        return redirect('affiche_panier')
    clients=Client.objects.all()
    produits=Produit.objects.all()
    return render(request, "interface_admin/Admin_panier/panier_ajout.html",{'clients':clients,'produits':produits})


def modifier_panier(request, id_panier):
    panier = get_object_or_404(Panier , id_panier=id_panier)
    if request.method == 'POST':
        panier.id_client_id = request.POST.get('id_client')
        product_ids = request.POST.getlist('id_produit')
        panier.produits.clear()
        for product_id in product_ids:
            produit = get_object_or_404(Produit, id_produit=product_id)
            panier.produits.add(produit)
        panier.quantite=request.POST.get('quantite')
        panier.save()
        return redirect('affiche_panier')
    clients = Client.objects.all()
    produits = Produit.objects.all()
    return render(request, 'interface_admin/Admin_panier/panier_modification.html', {'panier': panier,'clients':clients,'produits':produits})



def suprimer_panier(request,id_panier):
    objet = get_object_or_404(Panier, id_panier=id_panier)
    if request.method == 'GET':
        objet.delete()
        return redirect('affiche_panier')
    return HttpResponse("erreur")

# ==========================================end admin panier==========================================


# =======================Admin Commentaire===============================================

def affiche_commentaire(request):
    commentaires = Commentaire.objects.all()
    return render(request,"interface_admin/Admin_commentaire/commentaire_affichage.html",{'commentaires':commentaires})

def ajouter_commentaire(request):
    if request.method == 'POST':
        id_produit_id=request.POST.get('produit')
        client_id=request.POST.get('client')
        texte_commentaire = request.POST.get('commentaire')
        evaluation = request.POST.get('evaluation')
        commentaire = Commentaire(id_produit_id=id_produit_id, id_client_id=client_id, texte_commentaire=texte_commentaire,evaluation=evaluation)
        commentaire.save()
        return redirect('affiche_commentaire')
    produits = Produit.objects.all()
    clients = Client.objects.all()
    return render(request, "interface_admin/Admin_commentaire/commentaire_ajout.html",{'produits':produits,'clients':clients})

def modifier_commentaire(request, id_commentaire):
    commentaire = get_object_or_404(Commentaire, id_commentaire=id_commentaire)
    if request.method == 'POST':
        commentaire.id_produit_id = request.POST.get('produit')
        commentaire.id_client_id = request.POST.get('client')
        commentaire.texte_commentaire = request.POST.get('commentaire')
        commentaire.evaluation = request.POST.get('evaluation')
        commentaire.save()
        return redirect('affiche_commentaire')
    produits = Produit.objects.all()
    clients = Client.objects.all()
    return render(request, 'interface_admin/Admin_commentaire/commentaire_modification.html', {'commentaire':commentaire,'produits': produits,'clients':clients})



def supprimer_commentaire(request,id_commentaire):
    objet = get_object_or_404(Commentaire, id_commentaire=id_commentaire)
    if request.method == 'GET':
        objet.delete()
        return redirect('affiche_commentaire')
    return HttpResponse("erreur")

# ==========================================end admin Commentaire==========================================


# =======================Admin commandeProduit===============================================

def affiche_commandeProduit(request):
    commandes = CommandeProduit.objects.all()
    return render(request,"interface_admin/Admin_commande_Produit/commandeProduit_affichage.html",{'commandes':commandes})

def ajouter_commandeProduit(request):
    if request.method == 'POST':
        id_client=request.POST.get('client')
        statut_commande=request.POST.get('statut')
        date_commande = date.today()
        commande = CommandeProduit(id_client_id=id_client, date_commande=date_commande,statut_commande=statut_commande)
        commande.save()
        return redirect('affiche_commandeProduit')
    clients = Client.objects.all()
    return render(request, "interface_admin/Admin_commande_produit/commandeProduit_ajout.html",{'clients':clients})

def modifier_commandeProduit(request, id_commande):
    commande = get_object_or_404(CommandeProduit, id_commande=id_commande)
    if request.method == 'POST':
        commande.id_client_id = request.POST.get('client')
        commande.date_commande = date.today()
        commande.statut_commande = request.POST.get('statut')
        commande.save()
        return redirect('affiche_commandeProduit')
    clients = Client.objects.all
    return render(request, 'interface_admin/Admin_commande_produit/commandeProduit_modification.html', {'clients': clients,'commande':commande})



def suprimer_commandeProduit(request,id_commande):
    objet = get_object_or_404(CommandeProduit, id_commande=id_commande)
    if request.method == 'GET':
        objet.delete()
        return redirect('affiche_commandeProduit')
    return HttpResponse("erreur")

# ==========================================end admin commandeProduit==========================================

# =============================Fournisseur===============================

def info_fournisseur(request):
    if request.method == 'POST':
        id_email = request.session.get('compte')
        nom_enterprise = request.POST.get('nom_enterprise')
        numero_tel = request.POST.get('num_tel')
        adresse = request.POST.get('adresse')
        Description = request.POST.get('Description')
        fournisseur = Fournisseur(id_email_id=id_email, nom_enterprise=nom_enterprise, num_tel=numero_tel, adresse=adresse, description=Description)
        fournisseur.save()
        return redirect('home')
    return render(request,"interface_fournisseur/info_fournisseur.html")

def home(request):
    produits = Produit.objects.all()[:20]
    return render(request, "interface_fournisseur/index.html" , context={"produits": produits})

def product_details(request, id):
    produit = Produit.objects.filter(id_produit=id).first()
    return render(request, "interface_fournisseur/product-details.html", {'produit': produit})

def produit_form(request):
    categories=Categorie.objects.all()
    fournisseurs=Fournisseur.objects.all()
    context={
        "categories":categories,
        "fournisseurs":fournisseurs,
    }
    return render(request, 'interface_fournisseur/ajouter_produit.html',context)

def ajouter_produit(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        categorie_id = request.POST.get('categorie')
        categorie = Categorie.objects.get(id_categorie=categorie_id)
        prix = request.POST.get('prix')
        fournisseur_id = 12
        fournisseu = Fournisseur.objects.get(id_fournisseur=fournisseur_id)
        emplacement = request.POST.get('emplacement')
        image_produit = request.FILES['image_produit']
        nouveau_produit = Produit(
            nom=nom,
            description=description,
            categorie=categorie,
            prix=prix,
            id_fournisseur=fournisseu,
            emplacement=emplacement,
            image=image_produit,
        )
        nouveau_produit.save()
    return redirect('home')

def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, id_produit=produit_id)
    produit.delete()
    return redirect('home')

def categorie_form(request):
    return render(request, 'interface_fournisseur/ajouter_categorie.html')

def ajouter_categorie(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        nouvelle_categorie = Categorie(
            nom=nom,
            description=description
        )
        nouvelle_categorie.save()
    return redirect('produit_form')

def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, id_produit=produit_id)
    categories = Categorie.objects.all()
    if request.method == 'POST':
        produit.nom = request.POST.get('nom')
        produit.description = request.POST.get('description')
        produit.categorie_id = request.POST.get('categorie')
        produit.prix = request.POST.get('prix')
        image_produit = request.FILES.get('image_produit')
        if image_produit:
            produit.image = image_produit
        produit.save()
        return redirect('product_details', id=produit.id_produit)
    return render(request, 'interface_fournisseur/modifier_produit.html', {'produit': produit, 'categories': categories})
