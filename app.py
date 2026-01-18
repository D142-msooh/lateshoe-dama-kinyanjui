from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Late Show API</h1>'

# GET all episodes
@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    episodes_list = [episode.to_dict(only=('id', 'date', 'number')) for episode in episodes]
    return jsonify(episodes_list), 200

# GET episode by id
@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.filter(Episode.id == id).first()
    
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    episode_dict = episode.to_dict(only=(
        'id', 'date', 'number', 
        'appearances.id', 'appearances.rating', 
        'appearances.episode_id', 'appearances.guest_id', 
        'appearances.guest.id', 'appearances.guest.name', 
        'appearances.guest.occupation'
    ))
    
    return jsonify(episode_dict), 200

# GET all guests
@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    guests_list = [guest.to_dict(only=('id', 'name', 'occupation')) for guest in guests]
    return jsonify(guests_list), 200

# POST new appearance
@app.route('/appearances', methods=['POST'])
def create_appearance():
    try:
        data = request.get_json()
        
        new_appearance = Appearance(
            rating=data.get('rating'),
            episode_id=data.get('episode_id'),
            guest_id=data.get('guest_id')
        )
        
        db.session.add(new_appearance)
        db.session.commit()
        
        appearance_dict = new_appearance.to_dict(only=(
            'id', 'rating', 'guest_id', 'episode_id',
            'episode.id', 'episode.date', 'episode.number',
            'guest.id', 'guest.name', 'guest.occupation'
        ))
        
        return jsonify(appearance_dict), 201
        
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        return jsonify({"errors": ["validation errors"]}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
