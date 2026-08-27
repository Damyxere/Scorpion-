from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import yt_dlp

# Se index.html è nella radice del progetto, usa template_folder='.'
# Se invece è nella cartella 'templates/', lascia solo app = Flask(__name__)
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
    print("🚀 Server Audio avviato su http://127.0.0.1:5000")
    app.run(port=5000)
    
