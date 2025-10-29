"""
URL configuration for Vente project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from Fashion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Fashion.urls')),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('debut/', views.home, name='debut'),
    path('profil/', views.profil_view, name='profil'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('', views.home, name='home'),
    path('ajouter-produit/', views.ajouter_produit, name='ajouter_produit'),

    path('panier/', views.panier, name='panier'),
path('panier/ajouter/<int:product_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
path('panier/supprimer/<int:product_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),

   
      path('catalogue/', views.catalogue, name='catalogue'),
    path('panier/', views.panier, name='panier'),
    path('panier/ajouter/<int:product_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/supprimer/<int:product_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('paiement/', views.paiement, name='paiement'),
    path('historique/', views.historique, name='historique'),

]

# pour affichage des images téléchargées
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
