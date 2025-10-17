"""
SA Health App - Multilingual Medical Communication Tool
Flask Backend Application
"""

from flask import Flask, render_template, jsonify, request, send_file
import json
import os
from gtts import gTTS
from io import BytesIO

# Initialize Flask app with correct template and static folders
app = Flask(__name__, 
           template_folder='app/templates',
           static_folder='app/static')

# Configure app
app.config['JSON_SORT_KEYS'] = False

# Path to data file (absolute path for deployment compatibility)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'phrases.json')

def load_phrases_data():
    """Load phrases data from JSON file"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"categories": [], "phrases": []}
    except json.JSONDecodeError:
        return {"categories": [], "phrases": []}

def get_phrases_by_category(category_id):
    """Get all phrases for a specific category"""
    data = load_phrases_data()
    filtered_phrases = [
        phrase for phrase in data['phrases']
        if category_id in phrase.get('categories', [])
    ]
    return filtered_phrases

# Routes

@app.route('/')
def home():
    """Home page route"""
    data = load_phrases_data()
    return render_template('index.html', 
                         categories=data.get('categories', []),
                         total_phrases=len(data.get('phrases', [])))

@app.route('/app')
def app_interface():
    """Interactive app interface"""
    return render_template('app.html')

@app.route('/api/categories')
def get_categories():
    """API endpoint to get all categories"""
    data = load_phrases_data()
    return jsonify({
        'success': True,
        'categories': data.get('categories', [])
    })

@app.route('/api/phrases')
def get_all_phrases():
    """API endpoint to get all phrases"""
    data = load_phrases_data()
    return jsonify({
        'success': True,
        'total': len(data.get('phrases', [])),
        'phrases': data.get('phrases', [])
    })

@app.route('/api/phrases/category/<category_id>')
def get_phrases_by_category_route(category_id):
    """API endpoint to get phrases by category"""
    phrases = get_phrases_by_category(category_id)
    
    return jsonify({
        'success': True,
        'category': category_id,
        'total': len(phrases),
        'phrases': phrases
    })

@app.route('/api/phrase/<phrase_id>')
def get_phrase_by_id(phrase_id):
    """API endpoint to get a specific phrase by ID"""
    data = load_phrases_data()
    phrase = next((p for p in data['phrases'] if p['id'] == phrase_id), None)
    
    if phrase:
        return jsonify({
            'success': True,
            'phrase': phrase
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Phrase not found'
        }), 404

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'app': 'SA Health App',
        'version': '1.0.0'
    })

@app.route('/api/audio/<phrase_id>/<language>')
def generate_audio(phrase_id, language):
    """Generate audio for a specific phrase in a specific language"""
    try:
        # Load phrase data
        data = load_phrases_data()
        phrase = next((p for p in data['phrases'] if p['id'] == phrase_id), None)
        
        if not phrase:
            return jsonify({
                'success': False,
                'error': 'Phrase not found'
            }), 404
        
        # Get translation
        if language not in phrase['translations']:
            return jsonify({
                'success': False,
                'error': f'Language {language} not available for this phrase'
            }), 404
        
        # gTTS language mapping - some SA languages not yet supported by Google TTS
        gtts_language_map = {
            'en': 'en',     # English - supported
            'af': 'af',     # Afrikaans - supported
            'zu': 'en',     # Zulu - not supported, use English as fallback
            'xh': 'en',     # Xhosa - not supported, use English as fallback  
            'nso': 'en'     # Sepedi - not supported, use English as fallback
        }
        
        gtts_lang = gtts_language_map.get(language, 'en')
        
        # For unsupported languages, try to use TTS-optimized pronunciation if available
        # This uses a special respelling format designed for TTS engines:
        # - Only ONE capitalized syllable for primary stress
        # - All other syllables lowercase
        # - Hyphens for syllable separation (helps TTS parse correctly)
        translation = phrase['translations'][language]
        
        if language in ['zu', 'xh', 'nso'] and 'tts_pronunciation' in translation:
            # Use TTS-optimized pronunciation respelling
            text = translation['tts_pronunciation']
        else:
            # Use native text (for supported languages or when no TTS pronunciation exists)
            text = translation['text']
        
        # Generate audio using gTTS
        tts = gTTS(text=text, lang=gtts_lang, slow=False)
        
        # Save to in-memory buffer
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Return audio file
        return send_file(
            audio_buffer,
            mimetype='audio/mp3',
            as_attachment=False,
            download_name=f'{phrase_id}_{language}.mp3'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handlers

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Run the app
    # Use debug=False for production, debug=True for local development
    import os
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
