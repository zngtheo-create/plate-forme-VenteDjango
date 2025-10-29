from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# creation dune dable dans model p
class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mote_de_passe = models.CharField(max_length=100)




class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(max_length=10, blank=True, null=True)
    pays = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='profils/', blank=True, null=True)

    def __str__(self):
        return self.user.username



    

    #les produits
    

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du produit")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix (FCFA)")
    image = models.ImageField(upload_to='produits/', blank=True, null=True)

    def __str__(self):
        return self.name
    

# historique des commandes

class Commande(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    produits = models.JSONField()  # liste de produits avec nom, prix, quantité
    total = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    statut = models.CharField(max_length=50, default='Payé')

    def __str__(self):
        return f"Commande #{self.id} - {self.utilisateur.username}"
    

class Commentaire(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    texte = models.TextField()
    note = models.IntegerField(default=5)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Commentaire de {self.utilisateur.username} sur {self.produit.name}"