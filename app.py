from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

locations = {}

@app.route('/')
def index():
    return render_template("map.html")

# 📍 接收 GPS
@socketio.on('send_location')
def handle_location(data):
    user = data['user']

    locations[user] = {
        "lat": data['lat'],
        "lng": data['lng'],
        "acc": data.get('acc', 999)
    }

    # 🔥 即時廣播給所有人
    emit('update_map', locations, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
