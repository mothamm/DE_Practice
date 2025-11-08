import sqlite3
import requests, json

conn = sqlite3.connect("/workspaces/DE_Practice/sqlite_proj/test.db")
cur = conn.cursor()

def get_pokemon_data(pokemon):
  base_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
  response = requests.get(base_url)
  data = response.json()

  pokemon_id = data.get('id')
  pokemon_name = data.get('name')
  pokemon_height = data.get('height')
  pokemon_weight = data.get('weight')
  pokemon_types = json.dumps([type['type']['name'] for type in data.get('types')])
  pokemon_abilities = json.dumps([ability["ability"]["name"] for ability in data.get("abilities", [])])
  pokemon_stats = json.dumps({stat["stat"]["name"]: stat["base_stat"] for stat in data.get("stats", [])})
  pokemon_moves = json.dumps([move["move"]["name"] for move in data.get("moves", [])])
  pokemon_game_indices = json.dumps([game_index["game_index"] for game_index in data.get("game_indices", [])])

  return (pokemon_id, pokemon_name, pokemon_height, pokemon_weight, pokemon_types, pokemon_abilities, pokemon_stats, pokemon_moves, pokemon_game_indices)

def get_pokemon_list(limit=1000):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
    response = requests.get(url)
    data = response.json()
    # Extract just the names
    return [p['name'] for p in data['results']]


poke_list = get_pokemon_list(1000)
poke_list_values = [get_pokemon_data(pokemon) for pokemon in poke_list]

cur.executemany("""
INSERT OR REPLACE INTO pokemon
(id, name, height, weight, types, abilities, stats, moves, game_indices)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", poke_list_values)
conn.commit()
print(f"Inserted {len(poke_list_values)} successfully")