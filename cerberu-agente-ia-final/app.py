print('Bienvenido a Cerberu')
import os
import json
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

DATA_FOLDER = "data_web"
os.makedirs(DATA_FOLDER, exist_ok=True)

FILES_AND_DEFAULTS = {
    "visitas.json": {"visitas": 0},
    "descargas.json": {"descargas": 0},
    "comentarios.json": {"comentarios": []}
}

for filename, default_content in FILES_AND_DEFAULTS.items():
    file_path = os.path.join(DATA_FOLDER, filename)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(default_content, f, indent=4)

app = Flask(__name__)
CORS(app)

@app.route("/visitar", methods=["POST"])
def aumentar_visitas():
    visitas_path = os.path.join(DATA_FOLDER, "visitas.json")
    with open(visitas_path, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data["visitas"] += 1
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    return jsonify({"mensaje": "Visita registrada", "total": data["visitas"]})

@app.route("/descargar", methods=["GET"])
def descargar_archivo():
    descargas_path = os.path.join(DATA_FOLDER, "descargas.json")
    with open(descargas_path, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data["descargas"] += 1
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    return send_file("cerberu-agente-ia.zip", as_attachment=True)

@app.route("/comentar", methods=["POST"])
def agregar_comentario():
    nuevo = request.get_json()
    comentarios_path = os.path.join(DATA_FOLDER, "comentarios.json")
    with open(comentarios_path, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data["comentarios"].append(nuevo)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    return jsonify({"mensaje": "Comentario agregado correctamente"})

@app.route("/comentarios", methods=["GET"])
def obtener_comentarios():
    comentarios_path = os.path.join(DATA_FOLDER, "comentarios.json")
    with open(comentarios_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/estadisticas", methods=["GET"])
def estadisticas():
    with open(os.path.join(DATA_FOLDER, "visitas.json"), "r", encoding="utf-8") as v_file:
        visitas = json.load(v_file)["visitas"]
    with open(os.path.join(DATA_FOLDER, "descargas.json"), "r", encoding="utf-8") as d_file:
        descargas = json.load(d_file)["descargas"]
    return jsonify({"visitas": visitas, "descargas": descargas})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))