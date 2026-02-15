from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Статистика для разных сессий и сцен
# Формат: {session_id: {scene_id: {choice_id: count}}}
stats = {}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Visual Novel API is running',
        'endpoints': {
            '/api/choice': 'POST - Save a player choice',
            '/api/stats': 'GET - Get current statistics for a scene and session'
        }
    })

@app.route('/api/choice', methods=['POST'])
def save_choice():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        session_id = data.get('session_id')
        scene = data.get('scene')
        choice_id = data.get('choice_id')
        
        if not session_id or not scene or not choice_id:
            return jsonify({'error': 'Missing session_id, scene or choice_id'}), 400
        
        # Инициализируем структуры данных
        if session_id not in stats:
            stats[session_id] = {}
        
        if scene not in stats[session_id]:
            stats[session_id][scene] = {}
        
        if choice_id not in stats[session_id][scene]:
            stats[session_id][scene][choice_id] = 0
        
        # Увеличиваем счетчик
        stats[session_id][scene][choice_id] += 1
        
        return jsonify({
            'success': True,
            'message': f'Choice recorded for session {session_id}, scene {scene}',
            'stats': stats[session_id][scene]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    session_id = request.args.get('session_id')
    scene = request.args.get('scene', 'glava1')
    
    if not session_id:
        return jsonify({'error': 'Missing session_id'}), 400
    
    # Возвращаем статистику только для указанной сессии
    if session_id not in stats or scene not in stats[session_id]:
        return jsonify({
            'scene': scene,
            'session': session_id,
            'choices': {},
            'total': 0
        })
    
    scene_stats = stats[session_id][scene]
    total = sum(scene_stats.values())
    
    return jsonify({
        'scene': scene,
        'session': session_id,
        'choices': scene_stats,
        'total': total
    })

# Для Vercel
app = app
