from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    slug = models.SlugField(unique=True, help_text="Identifiant unique pour l'URL (ex: electronique)")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom

class Produit(models.Model):
    # Liaison avec la catégorie
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name='produits')
    
    nom = models.CharField(max_length=200)
    prix = models.PositiveIntegerField(verbose_name="Prix (FCFA)") # Changé en entier pour les FCFA
    description = models.TextField()
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom