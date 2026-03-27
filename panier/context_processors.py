from .models import Panier

def panier_global(request):
    # On récupère tous les objets du panier
    articles = Panier.objects.all()
    
    # On additionne les quantités (ex: 2 savons + 1 parfum = 3)
    nombre_total = sum(item.quantite for item in articles)
    
    # On retourne un dictionnaire que le HTML pourra lire
    return {
        'compteur_panier': nombre_total
    }