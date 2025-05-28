from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/') # Let op de toevoeging van '/api/'
def hello_api():
    """Returns a simple greeting from the API."""
    return 'Hello from API!'

@app.route('/api/health') # Let op de toevoeging van '/api/'
def health_check():
    """Returns a health status for the API."""
    return jsonify(status="ok")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
