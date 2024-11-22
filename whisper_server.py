from flask import Flask, request, jsonify
import whisper
import os

app = Flask(__name__)

# Cargar el modelo de Whisper
model = whisper.load_model("small")  # Cambia "small" según tus necesidades

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Obtener el nombre completo del archivo desde la solicitud
    data = request.get_json()
    if not data or 'filename' not in data:
        return jsonify({'error': 'No filename provided'}), 400

    # Verificar que el archivo existe
    file_path = data['filename']  # El cliente ya envía la ruta completa dentro de 'audios/'
    if not os.path.isfile(file_path):
        return jsonify({'error': f'File {file_path} not found'}), 404

    # Transcribir el archivo de audio usando Whisper
    try:
        result = model.transcribe(file_path)
    except Exception as e:
        return jsonify({'error': f'Whisper transcription error: {str(e)}'}), 500

    # Devolver la transcripción como respuesta JSON
    return jsonify({'text': result['text']})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Escucha en el puerto 5000
