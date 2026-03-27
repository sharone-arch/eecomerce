from django.db import models
from produits.models import Produit  # Import des produits


# ================================
# PANIER
# ================================
class Panier(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"

    def total_ligne(self):
        return self.quantite * self.produit.prix


# ================================
# COMMANDE
# ================================
class Commande(models.Model):

    MODE_PAIEMENT_CHOICES = [
        ('livraison', 'Paiement à la livraison'),
        ('momo', 'MTN Mobile Money'),
        ('orange', 'Orange Money'),
    ]

    STATUT_CHOICES = [
        ('attente', 'En attente'),
        ('paye', 'Payée'),
        ('livree', 'Livrée'),
    ]

    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    # Nouveaux champs avec valeurs par défaut (important)
    mode_paiement = models.CharField(
        max_length=20,
        choices=MODE_PAIEMENT_CHOICES,
        default='livraison'
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='attente'
    )

    def __str__(self):
        return f"Commande {self.id} - {self.total} FCFA"


# ================================
# LIGNES DE COMMANDE
# ================================
class LigneCommande(models.Model):
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='lignes'
    )
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def total_ligne(self):
        return self.quantite * self.prix