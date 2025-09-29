from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai, os, time
from gtts import gTTS

# usa variable de entorno para la clave
openai.api_key = os.getenv("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")

app = Flask(__name__)
CORS(app)

# carpeta de audios dentro del proyecto
AUDIO_DIR = os.path.join(os.getcwd(), "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

SYSTEM_PROMPT = """Tu eres ChatGPT y conoces a Papi Ver-gon.
Debes hablar siempre de manera sensual, atrevida, lujuriosa y juguetona.
Usa un estilo coqueto y provocador, con dobles sentidos inocentes y humor travieso.
Recuerda las rimas, historias y juegos que le gustan a Papi Ver-gon.
"""

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    texto = data.get("text","")
    if not texto:
        return jsonify({"error":"No text provided"}), 400

    messages = [
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role":"user", "content": texto}
    ]

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = resp["choices"][0]["message"]["content"].strip()

    # generar audio con gTTS (español)
    filename = f"resp_{int(time.time())}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    tts = gTTS(text=reply, lang="es")
    tts.save(filepath)

    # devolvemos texto y la ruta relativa al audio
    return jsonify({
        "reply": reply,
        "audio_path": f"/audio/{filename}"
    })

# ruta para servir los audios
@app.route("/audio/<filename>", methods=["GET"])
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

if __name__ == "__main__":
    # Render necesita host 0.0.0.0
    app.run(host="0.0.0.0", port=5000)
