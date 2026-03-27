import urllib.parse
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from produits.models import Produit
from .models import Panier, Commande, LigneCommande

# ================================
# VOIR LE PANIER
# ================================
def voir_panier(request):
    articles = Panier.objects.all()
    total_general = sum(item.produit.prix * item.quantite for item in articles)

    message = "Bonjour commerceligne, je souhaite commander :\n"
    for item in articles:
        message += f"- {item.produit.nom} (Qté: {item.quantite})\n"
    message += f"\n*Total à payer : {total_general} FCFA*"
    message_encode = urllib.parse.quote(message)

    return render(request, 'panier/panier.html', {
        'articles': articles,
        'total_general': total_general,
        'message_whatsapp': message_encode
    })

# ================================
# AJOUTER AU PANIER
# ================================
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    item, cree = Panier.objects.get_or_create(produit=produit)
    if not cree:
        item.quantite += 1
        item.save()
    messages.success(request, f"✅ {produit.nom} a été ajouté au panier !")
    return redirect('liste_produits')

# ================================
# RETIRER DU PANIER
# ================================
def retirer_du_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    item = Panier.objects.filter(produit=produit).first()
    if item:
        if item.quantite > 1:
            item.quantite -= 1
            item.save()
        else:
            item.delete()
    return redirect('voir_panier')

# ================================
# SUPPRIMER DU PANIER
# ================================
def supprimer_du_panier(request, produit_id):
    item = get_object_or_404(Panier, produit_id=produit_id)
    item.delete()
    messages.info(request, "L'article a été retiré du panier.")
    return redirect('voir_panier')

# ================================
# PAGE PAIEMENT
# ================================
def paiement(request):
    articles = Panier.objects.all()
    if not articles:
        messages.warning(request, "Votre panier est vide.")
        return redirect('voir_panier')

    total_general = sum(item.produit.prix * item.quantite for item in articles)

    if request.method == 'POST':
        mode = request.POST.get('mode_paiement')

        # ------------------------
        # Validation côté serveur
        # ------------------------
        if mode == "Mobile Money":
            numero = request.POST.get('numero_mobile', '')
            if not numero.isdigit() or len(numero) != 9 or not (numero.startswith('67') or numero.startswith('69')):
                messages.error(request, "Numéro MTN Mobile Money invalide (doit commencer par 67 ou 69 et contenir 9 chiffres).")
                return redirect('paiement')

        elif mode == "Orange Money":
            numero = request.POST.get('numero_orange', '')
            if not numero.isdigit() or len(numero) != 9 or not numero.startswith('69'):
                messages.error(request, "Numéro Orange Money invalide (doit commencer par 69 et contenir 9 chiffres).")
                return redirect('paiement')

        elif mode == "Carte bancaire":
            numero = request.POST.get('numero_carte', '').replace(' ', '')
            date_exp = request.POST.get('date_exp', '')
            cvc = request.POST.get('cvc', '')

            if not numero.isdigit() or len(numero) != 16:
                messages.error(request, "Numéro de carte invalide (16 chiffres).")
                return redirect('paiement')

            try:
                mois, annee = map(int, date_exp.split('/'))
                now = datetime.datetime.now()
                current_year = now.year % 100
                current_month = now.month
                if mois < 1 or mois > 12:
                    messages.error(request, "Mois de la date d'expiration invalide.")
                    return redirect('paiement')
                if annee < current_year or (annee == current_year and mois < current_month):
                    messages.error(request, "La date d'expiration est déjà passée.")
                    return redirect('paiement')
            except:
                messages.error(request, "Format de date invalide. Utilisez MM/AA.")
                return redirect('paiement')

            if not cvc.isdigit() or len(cvc) != 3:
                messages.error(request, "CVC invalide (3 chiffres).")
                return redirect('paiement')

        elif mode == "Paiement à la livraison":
            pass  # Aucun contrôle

        else:
            messages.error(request, "Veuillez sélectionner un mode de paiement valide.")
            return redirect('paiement')

        # ------------------------
        # Création de la commande
        # ------------------------
        commande = Commande.objects.create(
            total=total_general,
            mode_paiement=mode
        )

        for item in articles:
            LigneCommande.objects.create(
                commande=commande,
                produit=item.produit,
                quantite=item.quantite,
                prix=item.produit.prix
            )

        articles.delete()
        messages.success(request, f"Commande enregistrée avec succès ! Mode de paiement : {mode}")
        return redirect('historique_commandes')

    return render(request, 'panier/paiement.html', {
        'articles': articles,
        'total_general': total_general
    })

# ================================
# HISTORIQUE DES COMMANDES
# ================================
def historique_commandes(request):
    commandes = Commande.objects.all().order_by('-date')
    return render(request, 'panier/historique.html', {
        'commandes': commandes
    })