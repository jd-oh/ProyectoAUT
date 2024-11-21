from flask import Flask, jsonify, request

# Configuración del servidor Flask
app = Flask(__name__)

# Variables para simular estados
state = {
    "food_container_open": False,
    "water_container_open": False,
    "toy_active": False
}

@app.route('/open_food', methods=['GET'])
def open_food():
    state["food_container_open"] = True
    return jsonify({"message": "Contenedor de comida abierto"}), 200

@app.route('/open_water', methods=['GET'])
def open_water():
    state["water_container_open"] = True
    return jsonify({"message": "Contenedor de agua abierto"}), 200

@app.route('/activate_toy', methods=['POST'])
def activate_toy():
    state["toy_active"] = True
    return jsonify({"message": "Juguete activado"}), 200

if __name__ == '__main__':
    # Ejecutar el servidor Flask
    app.run(host='127.0.0.1', port=5000)
