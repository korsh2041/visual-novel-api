from flask import Flask, request, jsonify
from flask_cors import CORS

# Создаем приложение
app = Flask(__name__)
CORS(app)

# Статистика выборов
stats = {
    'forest': 0,
    'river': 0,
    'cave': 0
}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Visual Novel API is running',
        'endpoints': {
            '/api/stats': 'GET - Get current statistics',
            '/api/choice': 'POST - Save a player choice'
        }
    })

@app.route('/api/choice', methods=['POST'])
def save_choice():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        choice = data.get('choice')
        if not choice:
            return jsonify({'error': 'No choice provided'}), 400
        
        if choice in stats:
            stats[choice] += 1
            return jsonify({
                'success': True,
                'stats': stats,
                'message': f'Choice "{choice}" recorded'
            })
        else:
            return jsonify({'error': f'Invalid choice: {choice}'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'stats': stats,
        'total': sum(stats.values())
    })

# Для Vercel - это обязательно!
app = app
