from rest_framework import serializers
from .models import Pokemon

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ['name', 'normal_sprite', 'shiny_sprite', 'moves', 'egg_moves']
