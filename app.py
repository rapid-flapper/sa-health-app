"""
SA Health App - Multilingual Medical Communication Tool
Flask Backend Application
"""

from flask import Flask, render_template, jsonify, request
import json
import os

# Initialize Flask app with correct template and static folders
app = Flask(__name__, 
           template_folder='app/templates',
           static_folder='app/static')

# Configure app
app.config['JSON_SORT_KEYS'] = False

# Path to data file
DATA_FILE = os.path.join('data', 'phrases.json')

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
    app.run(debug=True, host='0.0.0.0', port=5000)
