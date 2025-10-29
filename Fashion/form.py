# les modules important a importer
from django import forms
from .models import Profil, Product
from django.contrib.auth.forms import UserCreationForm


#  la structure de notre fomulaire 
class customUserCreationForm(UserCreationForm):  #model personaliser
    
    email = forms.EmailField(
        label='email', 
        max_length=254, 
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
                              )
  # pour le mot de paase 1 
    password1 = forms.CharField(
        label='Mot de passe', 
        strip=False, #deactivation de la supresion automatique des espaces
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
                               )
  

  
    password2 = forms.CharField(
        label='Confirmer le mot de passe', 
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
                               )
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("password1","password2")  
    

    #profile utilisateur

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['telephone', 'adresse', 'ville', 'code_postal', 'pays', 'photo']


# ajout D'un produit sans cote administrateur

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']