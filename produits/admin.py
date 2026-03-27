from django.contrib import admin
from .models import Produit, Categorie

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    # Génère automatiquement le slug pendant que tu tapes le nom
    prepopulated_fields = {'slug': ('nom',)}
    list_display = ('nom', 'slug')

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste des produits
    list_display = ('nom', 'prix', 'categorie', 'disponible', 'cree_le')
    # Filtres sur le côté droit
    list_filter = ('disponible', 'categorie', 'cree_le')
    # Champs cliquables pour modifier
    list_editable = ('prix', 'disponible')
    # Barre de recherche
    search_fields = ('nom', 'description')