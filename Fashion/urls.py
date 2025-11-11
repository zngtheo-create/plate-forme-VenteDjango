
from django.urls import path
from .views import *
#definition de la route en prendre
urlpatterns = [
    path('', home, name='home'),
    path('inscription/', inscription, name='inscription'),
    path('connexion/', connexion, name='connexion'),
    path('debut/', debut, name='debut'),
    path('catalogue/', catalogue, name='catalogue'),
    path('catalogue/', catalogue, name='catalogue'),
    path('historique/', historique, name='historique'),
    path('recu/', recu_view, name='recu'),
    
  
]
