from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/clientData', methods=['POST'])
def receive_data():
    data = request.json
    sensorDataRecieved = data.get('sensorData')
    
    print('Received sensor data:', sensorDataRecieved)
    
    return jsonify({"message": "Data received successfully", "sensorData": sensorDataRecieved})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, ssl_context='adhoc', debug=True)
