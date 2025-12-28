from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games_v3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    face_descriptor = db.Column(db.Text, nullable=True) # JSON string of float array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GameRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_type = db.Column(db.String(50), nullable=False) # 'schulte' or 'stroop'
    player_name = db.Column(db.String(50), nullable=False, default="Unknown")
    difficulty = db.Column(db.String(20), nullable=True) # '3', '4', '5'
    score = db.Column(db.Float, nullable=False) # Time in seconds or score points
    accuracy = db.Column(db.Float, nullable=True) # Percentage
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'game_type': self.game_type,
            'player_name': self.player_name,
            'difficulty': self.difficulty,
            'score': self.score,
            'accuracy': self.accuracy,
            'created_at': self.created_at.isoformat()
        }

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/login_face', methods=['POST'])
def login_face():
    data = request.json
    if 'descriptor' not in data:
        return jsonify({'error': 'No descriptor provided'}), 400
    
    input_descriptor = np.array(data['descriptor'])
    users = User.query.all()
    
    best_match = None
    min_dist = 0.6 # Threshold for face matching (Euclidean distance)

    for user in users:
        if user.face_descriptor:
            stored_descriptor = np.array(json.loads(user.face_descriptor))
            dist = np.linalg.norm(input_descriptor - stored_descriptor)
            if dist < min_dist:
                min_dist = dist
                best_match = user
    
    if best_match:
        return jsonify({'name': best_match.name, 'match': True})
    else:
        return jsonify({'match': False})

@app.route('/api/register_face', methods=['POST'])
def register_face():
    data = request.json
    name = data.get('name')
    descriptor = data.get('descriptor')
    
    if not name or not descriptor:
        return jsonify({'error': 'Missing name or descriptor'}), 400
        
    # Check if user exists
    user = User.query.filter_by(name=name).first()
    if not user:
        user = User(name=name)
        db.session.add(user)
    
    # Update face descriptor
    user.face_descriptor = json.dumps(descriptor)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/record', methods=['POST'])
def add_record():
    data = request.json
    new_record = GameRecord(
        game_type=data['game_type'],
        player_name=data.get('player_name', '匿名勇士'),
        difficulty=str(data.get('difficulty', '3')),
        score=data['score'],
        accuracy=data.get('accuracy', 100.0)
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify(new_record.to_dict()), 201

@app.route('/api/records', methods=['GET'])
def get_records():
    game_type = request.args.get('game_type', 'schulte')
    best_records = []
    
    if game_type == 'schulte':
        levels = ['3', '4', '5']
        for level in levels:
            record = GameRecord.query.filter_by(game_type='schulte', difficulty=level)\
                .order_by(GameRecord.score.asc())\
                .first()
            if record:
                best_records.append(record.to_dict())
            else:
                best_records.append({
                    'difficulty': level,
                    'player_name': '---',
                    'score': 0,
                    'game_type': 'schulte'
                })
    elif game_type == 'stroop':
        # Stroop game: 20 trials
        record = GameRecord.query.filter_by(game_type='stroop', difficulty='20')\
            .order_by(GameRecord.score.asc())\
            .first()
        
        if record:
            best_records.append(record.to_dict())
        else:
            best_records.append({
                'difficulty': '20',
                'player_name': '---',
                'score': 0,
                'game_type': 'stroop'
            })
            
    return jsonify(best_records)

if __name__ == '__main__':
    app.run(debug=True)
