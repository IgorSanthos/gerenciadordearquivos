from flask import Flask, request, jsonify
import shutil
import os

app = Flask(__name__)

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    source = data['source']
    destination = data['destination']

    try:
        if not os.path.exists(source):
            return jsonify({'status': 'error', 'message': f'Source directory {source} does not exist'})
        
        if not os.path.exists(destination):
            os.makedirs(destination)

        shutil.move(source, destination)
        return jsonify({'status': 'success', 'message': f'Moved {source} to {destination}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(port=5001)
