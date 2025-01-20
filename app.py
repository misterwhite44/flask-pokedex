from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Fonction pour récupérer les données des Pokémon
def get_pokemon_data(pokemon_id):
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
        if response.status_code == 200:
            data = response.json()
            return {
                "id": data["id"],
                "name": data["name"],
                "height": data["height"] / 10,  # Convertir en mètres
                "weight": data["weight"] / 10,  # Convertir en kilogrammes
                "base_experience": data["base_experience"],
                "abilities": [ability["ability"]["name"] for ability in data["abilities"]],
                "types": [type_info["type"]["name"] for type_info in data["types"]],
                "moves": [move["move"]["name"] for move in data["moves"]],
                "image_url": data["sprites"]["other"]["official-artwork"]["front_default"]
            }
        else:
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération des données Pokémon : {e}")
        return None

# Récupérer les données des 150 premiers Pokémon
pokemon_list = [get_pokemon_data(i) for i in range(1, 191) if get_pokemon_data(i) is not None]

@app.route("/")
def index():
    return render_template("index.html", pokemons=pokemon_list)

@app.route("/api/pokemon/<int:pokemon_id>")
def get_pokemon(pokemon_id):
    pokemon = next((p for p in pokemon_list if p["id"] == pokemon_id), None)
    if pokemon:
        return jsonify(pokemon)
    else:
        return jsonify({"error": "Pokémon non trouvé"}), 404

@app.route("/search", methods=["POST"])
def search_pokemon():
    query = request.json.get("query", "").lower()
    found_pokemon = next((p for p in pokemon_list if p["name"].lower() == query), None)
    if found_pokemon:
        return jsonify(found_pokemon)
    else:
        return jsonify({"error": "Pokémon non trouvé"}), 404
    

@app.route('/combat')
def combat():
    return render_template('combat.html')

if __name__ == '__main__':
    app.run(debug=True)
