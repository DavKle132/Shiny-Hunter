from django.urls import path
from .views import pokemon_list, pokemon_builder

urlpatterns = [
    path('', pokemon_list, name='pokemon-list'),
    path('<str:pokemon_name>/builder/', pokemon_builder, name='pokemon-builder'),
]
