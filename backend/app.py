from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import config
from pose_detection import pose_detection

app = Flask(__name__)
CORS(app)

@app.route('/start', methods=['POST'])
def start_pose_detection():
    config.left_counter = 0
    config.right_counter = 0
    config.left_stage = None
    config.right_stage = None
    config.exercise_mode = request.json.get('mode', 'biceps')
    threading.Thread(target=pose_detection).start()
    return jsonify({'message': 'Pose detection started', 'mode': config.exercise_mode})

@app.route('/stop', methods=['POST'])
def stop_pose_detection():
    config.running = False
    return jsonify({'message': 'Pose detection stopped'})

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        'left_stage': config.left_stage,
        'right_stage': config.right_stage,
        'left_reps': config.left_counter,
        'right_reps': config.right_counter
    })

if __name__ == '__main__':
    app.run(debug=True)
