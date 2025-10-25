import requests
from django.core.management.base import BaseCommand
from pokedex.models import Pokemon


class Command(BaseCommand):
    help = "Fetch and populate Pokémon data from PokéAPI"

    def handle(self, *args, **kwargs):
        base_url = "https://pokeapi.co/api/v2/pokemon-species/"
        next_url = base_url

        while next_url:
            response = requests.get(next_url)
            if response.status_code == 200:
                data = response.json()
                for species in data['results']:
                    species_response = requests.get(species['url'])
                    if species_response.status_code == 200:
                        species_data = species_response.json()
                        name = species_data['name']
                        generation = int(species_data['generation']['url'].split('/')[-2])

                        # Get evolution chain data
                        evolution_chain_url = species_data['evolution_chain']['url']
                        evolution_chain_response = requests.get(evolution_chain_url)
                        pre_evolution = None
                        evolutions = []
                        evolution_chain = []
                        is_final_evolution = False

                        if evolution_chain_response.status_code == 200:
                            evolution_chain_data = evolution_chain_response.json()
                            chain = evolution_chain_data['chain']

                            # Traverse the chain to build the full evolution chain
                            while chain:
                                current_name = chain['species']['name']
                                evolution_chain.append(current_name)
                                if current_name == name:
                                    is_final_evolution = len(chain['evolves_to']) == 0
                                    evolutions = [evo['species']['name'] for evo in chain['evolves_to']]
                                chain = chain['evolves_to'][0] if chain['evolves_to'] else None

                        # Determine the pre-evolution
                        if name in evolution_chain:
                            idx = evolution_chain.index(name)
                            pre_evolution = evolution_chain[idx - 1] if idx > 0 else None

                        # Fetch Pokémon details for sprites and moves
                        pokemon_response = requests.get(species_data['varieties'][0]['pokemon']['url'])
                        if pokemon_response.status_code == 200:
                            pokemon_data = pokemon_response.json()
                            normal_sprite = pokemon_data['sprites']['front_default']
                            shiny_sprite = pokemon_data['sprites']['front_shiny']
                            moves = [move['move']['name'] for move in pokemon_data['moves']]

                            # Save to the database
                            Pokemon.objects.update_or_create(
                                name=name,
                                defaults={
                                    'normal_sprite': normal_sprite,
                                    'shiny_sprite': shiny_sprite,
                                    'moves': moves,
                                    'generation': generation,
                                    'final_evolution': is_final_evolution,
                                    'pre_evolution': pre_evolution,
                                    'evolutions': evolutions,
                                    'evolution_chain': evolution_chain,
                                },
                            )
                            self.stdout.write(f"Saved {name} (Final Evolution: {is_final_evolution})")
                next_url = data['next']
            else:
                self.stderr.write("Failed to fetch Pokémon data.")
                break
