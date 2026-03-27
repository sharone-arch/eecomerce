from django.contrib import admin
from .models import Panier, Commande, LigneCommande


# Affichage des lignes de commande dans la commande
class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 0
    readonly_fields = ('produit', 'quantite', 'prix')


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'total', 'mode_paiement', 'statut')
    list_filter = ('statut', 'mode_paiement', 'date')
    search_fields = ('id',)
    inlines = [LigneCommandeInline]


@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ('produit', 'quantite', 'date_ajout')


@admin.register(LigneCommande)
class LigneCommandeAdmin(admin.ModelAdmin):
    list_display = ('commande', 'produit', 'quantite', 'prix')