from django.urls import path
from . import views

urlpatterns = [
    path('', views.voir_panier, name='voir_panier'),
    path('ajouter/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('retirer/<int:produit_id>/', views.retirer_du_panier, name='retirer_du_panier'),
    path('supprimer/<int:produit_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    
    path('paiement/', views.paiement, name='paiement'),  # <- ici on remplace valider_commande
    path('historique/', views.historique_commandes, name='historique_commandes'),
]