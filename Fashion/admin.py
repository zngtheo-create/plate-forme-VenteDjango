from django.contrib import admin


from .models import Product  # importe ton modèle

# pour lajout des produits dans longle ladministration

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')  # colonnes affichées
    search_fields = ('name',)
