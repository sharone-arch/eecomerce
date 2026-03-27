from django.urls import path
from .views import liste_produits, a_propos, detail_produit
from . import views

urlpatterns = [
    path('', liste_produits, name='liste_produits'),
    path('a-propos/', a_propos, name='a_propos'),
    path('produit/<int:pk>/', views.detail_produit, name='detail_produit'),
]
