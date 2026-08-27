import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import yt_dlp

# template_folder='.' dice a Flask di cercare index.html nella stessa cartella di server.py
app = Flask(__name__, template_folder='.')
CORS(app)

@app.route('/', methods=['GET'])
def home():
    # Serve l'interfaccia principale index.html direttamente da Render
    return render_template('index.html')

@app.route('/stream', methods=['GET'])
def get_audio_stream():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Nessuna query fornita'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1:',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                video_data = info['entries'][0]
                audio_url = video_data['url']
                return jsonify({
                    'status': 'success',
                    'audio_url': audio_url,
                    'title': video_data.get('title'),
                    'duration': video_data.get('duration')
                })
            else:
                return jsonify({'error': 'Brano non trovato'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Render assegna una porta dinamica tramite variabile d'ambiente PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
