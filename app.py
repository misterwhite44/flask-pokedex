from flask import Flask, render_template
import requests

app = Flask(__name__)

# URL de l'API PokeAPI pour récupérer les pokémons
POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon"

def get_pokemon_data(url):
    """Fonction pour récupérer les détails du pokémon depuis son URL."""
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        name = data['name']
        image_url = data['sprites']['front_default']  # Image du pokémon
        types = [t['type']['name'] for t in data['types']]  # Récupérer les types
        height = data['height'] / 10  # Convertir la taille en mètres
        weight = data['weight'] / 10  # Convertir le poids en kg
        
        return {
            'name': name,
            'image_url': image_url,
            'types': types,
            'height': height,
            'weight': weight
        }
    return None

@app.route('/')
def home():
    # Faire une requête GET à l'API PokeAPI pour récupérer la liste des pokémons
    response = requests.get(POKEAPI_URL)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        data = response.json()  # Récupérer les données au format JSON
        pokemons = []
        
        # Parcourir les pokémons et récupérer leurs détails
        for pokemon in data['results']:
            pokemon_data = get_pokemon_data(pokemon['url'])
            if pokemon_data:
                pokemons.append(pokemon_data)
        
        return render_template('index.html', pokemons=pokemons)  # Passer les pokémons au template HTML
    else:
        return "Impossible de récupérer les pokémons", 500

if __name__ == '__main__':
    app.run(debug=True)
