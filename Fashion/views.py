from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .form import customUserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.decorators import login_required
from .models import Profil, Product, Commande
from .form import ProfilForm,ProductForm
from django.contrib.auth.models import User
from django.utils import timezone






# creation des fontion pour afficher les pages html avec les differentes routes
def home(request):
    return render(request, 'MAISON.html')

def inscription(request):
    if request.method == 'POST':
        #verification et enregistrement du formulaire
        form = customUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('connexion')  # Rediriger vers la page d'accueil après l'inscription réussie
    else:
        # afficher le formulaire vide 
        form = customUserCreationForm()
    
    return render(request, 'inscription.html', {'form': form})


def connexion(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        # 🔍 Vérifier si l'utilisateur a saisi un email
        try:
            user = User.objects.get(email=username_or_email)
            username = user.username
        except User.DoesNotExist:
            username = username_or_email  # il a mis un nom d'utilisateur

        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} 👋")
            return redirect("debut")  # 👉 redirige vers la page d’accueil
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    
    return render(request, "connexion.html")



@login_required # connexion requise pour evite le suvolement des page
def debut(request):
    return render(request, 'debut.html')
    


#profile utilisateur


@login_required
def profil_view(request):
    profil, created = Profil.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            return redirect('debut')
    else:
        form = ProfilForm(instance=profil)

    return render(request, 'profil.html', {'form': form})

#pour les produits
from django.shortcuts import render
from .models import Product

def catalogue(request):
    produits = Product.objects.all()
    return render(request, 'catalogue.html', {'produits': produits})


# pour la recherche dun produit



def catalogue(request):
    # On récupère les valeurs du formulaire
    query = request.GET.get('q', '')
  
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # On commence avec tous les produits
    produits = Product.objects.all()

    # Filtrage avancé
    if query:
        produits = produits.filter(name__icontains=query)  # filtre par nom
    
    if min_price:
        produits = produits.filter(price__gte=min_price)  # prix min
    if max_price:
        produits = produits.filter(price__lte=max_price)  # prix max

    # Envoie des produits au template
    context = {'produits': produits}
    return render(request, 'catalogue.html', context)







def ajouter_produit(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Fichiers pour l'image
        if form.is_valid():
            form.save()
            return redirect('catalogue')  # Redirige vers la page catalogue après ajout
    else:
        form = ProductForm()
    
    return render(request, 'ajouter_produit.html', {'form': form})




def ajouter_au_panier(request, product_id):
    produit = get_object_or_404(Product, id=product_id)
    panier = request.session.get('panier', {})

    if str(product_id) in panier:
        panier[str(product_id)]['quantite'] += 1
    else:
        panier[str(product_id)] = {
            'name': produit.name,
            'price': float(produit.price),
            'quantite': 1,
            'image': produit.image.url if produit.image else None
        }

    request.session['panier'] = panier
    return redirect(request.META.get('HTTP_REFERER', 'catalogue'))

# Supprimer un produit du panier
def supprimer_du_panier(request, product_id):
    panier = request.session.get('panier', {})
    if str(product_id) in panier:
        del panier[str(product_id)]
        request.session['panier'] = panier
    return redirect('panier')




# Afficher le panier
def panier(request):
    panier = request.session.get('panier', {})
    for item in panier.values():
        item['subtotal'] = item['price'] * item['quantite']
    total = sum(item['subtotal'] for item in panier.values())
    return render(request, 'panier.html', {'panier': panier, 'total': total})




# Page paiement (simple pour démo)
def paiement(request):
    panier = request.session.get('panier', {})
    total = sum(item['price'] * item['quantite'] for item in panier.values())
    return render(request, 'paiement.html', {'total': total})

# Historique des commandes

@login_required
def historique(request):
    commandes = Commande.objects.filter(utilisateur=request.user).order_by('-date')
    return render(request, 'historique.html', {'commandes': commandes})

#affichage des 6 premier produit dans l acceuil
def home(request):
    produits = Product.objects.all()[:6]  # Récupère les 6 premiers produits
    return render(request, 'MAISON.html', {'produits': produits})

#affichage des 6 premier produit dans debut
def debut(request):
    produits = Product.objects.all()[:6]  # Récupère les 6 premiers produits
    return render(request, 'debut.html', {'produits': produits})

#exemple de recu 



def recu_view(request):
    user = request.user

    # On récupère le panier depuis la session
    panier = request.session.get('panier', {})

    # On prépare les articles sous forme de liste
    items = []
    total = 0
    for key, item in panier.items():
        subtotal = float(item['price']) * int(item['quantite'])
        total += subtotal
        items.append({
            'name': item['name'],
            'quantite': item['quantite'],
            'price': item['price'],
            'subtotal': subtotal,
        })

    # Exemple d’objet commande fictif (pas besoin de modifier ton modèle)
    commande = {
        'date_commande': timezone.now(),
        'items': items,
    }

    context = {
        'user': user,
        'commande': commande,
        'items': items,
        'total': total,
        'site_name': "TC Fashion Boutique",
    }

    return render(request, 'recu.html', context)