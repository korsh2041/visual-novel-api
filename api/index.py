from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Статистика выборов
stats = {
    'forest': 0,
    'river': 0,
    'cave': 0
}

@app.route('/api/choice', methods=['POST'])
def save_choice():
    data = request.json
    choice = data.get('choice')
    
    if choice in stats:
        stats[choice] += 1
    
    return jsonify({
        'success': True,
        'stats': stats
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'stats': stats,
        'total': sum(stats.values())
    })

# Для Vercel
app = app
