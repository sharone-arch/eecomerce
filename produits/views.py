from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Produit

# 1. Vue pour la liste de tous les produits (avec recherche)
def liste_produits(request):
    query = request.GET.get('q') 
    if query:
        # Recherche dans le nom ou la description
        produits = Produit.objects.filter(
            Q(nom__icontains=query) | Q(description__icontains=query)
        )
    else:
        produits = Produit.objects.all()
    
    return render(request, 'produits/liste.html', {'produits': produits})

# 2. Vue pour le détail d'un produit spécifique
def detail_produit(request, pk):
    # On récupère le produit par son ID (pk). Si l'ID n'existe pas, erreur 404.
    produit = get_object_or_404(Produit, pk=pk)
    return render(request, 'produits/detail.html', {'produit': produit})

# 3. Vue pour la page À propos
def a_propos(request):
    return render(request, 'produits/a_propos.html')