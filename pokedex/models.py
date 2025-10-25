from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=100, unique=True)
    normal_sprite = models.URLField()
    shiny_sprite = models.URLField()
    egg_moves = models.JSONField(default=list, blank=True)
    moves = models.JSONField(default=list, blank=True)
    generation = models.IntegerField()
    final_evolution = models.BooleanField(default=False)
    pre_evolution = models.CharField(max_length=100, null=True, blank=True)  # Name of the pre-evolution
    evolutions = models.JSONField(default=list, blank=True)  # List of evolution names
    evolution_chain = models.JSONField(default=list, blank=True)  # Full evolution chain

    def __str__(self):
        return self.name
