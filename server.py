import os
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='.')
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/stream', methods=['GET'])
def get_audio_stream():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Nessuna query fornita'}), 400

    try:
        # 1. Cerca il brano tramite l'API di Piped
        search_url = f"https://pipedapi.kavin.rocks/search?q={query}&filter=music_songs"
        response = requests.get(search_url, timeout=10)
        data = response.json()

        items = data.get('items', [])
        if not items:
            return jsonify({'error': 'Brano non trovato'}), 404

        # Prendi il primo risultato
        first_track = items[0]
        video_id = first_track['url'].split('=')[-1]

        # 2. Recupera gli stream audio del brano
        stream_data = requests.get(f"https://pipedapi.kavin.rocks/streams/{video_id}", timeout=10).json()
        
        audio_streams = stream_data.get('audioStreams', [])
        if not audio_streams:
            return jsonify({'error': 'Stream audio non disponibile'}), 404

        # Seleziona lo stream audio con la qualità migliore
        best_audio = audio_streams[0]['url']

        return jsonify({
            'status': 'success',
            'audio_url': best_audio,
            'title': stream_data.get('title'),
            'duration': stream_data.get('duration')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
