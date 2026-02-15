from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Статистика для разных сцен
# Формат: {scene_id: {choice_id: count, ...}}
stats = {
    'glava1': {'forest': 0, 'cave': 0, 'river': 0},
    'glava2': {'forest': 0, 'cave': 0, 'river': 0},
    'glava3': {'forest': 0, 'cave': 0, 'river': 0},
    'glava5': {'forest': 0, 'cave': 0, 'river': 0}
}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Visual Novel API is running',
        'endpoints': {
            '/api/choice': 'POST - Save a player choice',
            '/api/stats': 'GET - Get current statistics for a scene'
        }
    })

@app.route('/api/choice', methods=['POST'])
def save_choice():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        scene = data.get('scene')
        choice_id = data.get('choice_id')
        
        if not scene or not choice_id:
            return jsonify({'error': 'Missing scene or choice_id'}), 400
        
        # Инициализируем сцену, если её нет
        if scene not in stats:
            stats[scene] = {}
        
        # Инициализируем выбор, если его нет
        if choice_id not in stats[scene]:
            stats[scene][choice_id] = 0
        
        # Увеличиваем счетчик
        stats[scene][choice_id] += 1
        
        return jsonify({
            'success': True,
            'message': f'Choice recorded for scene {scene}',
            'stats': stats[scene]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    scene = request.args.get('scene', 'glava1')
    
    if scene not in stats:
        return jsonify({
            'scene': scene,
            'choices': {},
            'total': 0
        })
    
    scene_stats = stats[scene]
    total = sum(scene_stats.values())
    
    return jsonify({
        'scene': scene,
        'choices': scene_stats,
        'total': total
    })

# Для Vercel
app = app
