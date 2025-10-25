from django.http import JsonResponse
from django.template.loader import render_to_string

def pokemon_list(request):
    # Get filter parameters
    generation = request.GET.get('generation')
    final_evolution = request.GET.get('final_evolution')
    search = request.GET.get('search', '')
    
    
    # Get dark mode preference from session or default to "dark"
    dark_mode = request.session.get('dark_mode', 'dark')

    # Handle AJAX request to update dark mode
    if request.method == 'POST':
        dark_mode = request.POST.get('dark_mode', 'dark')
        request.session['dark_mode'] = dark_mode
        return JsonResponse({'dark_mode': dark_mode})

    # Build the query
    queryset = Pokemon.objects.all()
    if generation:
        queryset = queryset.filter(generation=generation)
    if final_evolution:
        queryset = queryset.filter(final_evolution=True)
    if search:
        queryset = queryset.filter(name__icontains=search)

    # For AJAX requests, return only the grid HTML
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('pokedex/pokemon_grid.html', {'pokemon_list': queryset})
        return JsonResponse({'html': html})

    # Get all unique generations for the filter
    generations = Pokemon.objects.values_list('generation', flat=True).distinct().order_by('generation')

    return render(request, 'pokedex/pokemon_list.html', {
        'pokemon_list': queryset,
        'generations': generations,
        'final_evolution': final_evolution,
        'darkMode': dark_mode,
    })




from django.shortcuts import render, get_object_or_404
from .models import Pokemon


def pokemon_builder(request, pokemon_name):
    # Get the selected Pokémon
    pokemon = get_object_or_404(Pokemon, name=pokemon_name)

    # Fetch all Pokémon in the evolution chain
    evolution_chain = pokemon.evolution_chain  # Get the stored evolution chain
    related_forms = Pokemon.objects.filter(name__in=evolution_chain)

    # Sort the related forms based on their order in the evolution chain
    sorted_related_forms = sorted(related_forms, key=lambda p: evolution_chain.index(p.name))

    return render(request, 'pokedex/pokemon_builder.html', {
        'pokemon': pokemon,
        'related_forms': sorted_related_forms,
        'all_moves': pokemon.moves,
    })







