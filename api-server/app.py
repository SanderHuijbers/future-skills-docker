from flask import Flask, jsonify

app = Flask(__name__)

# De hoofd-API-route accepteert nu zowel /api als /api/ zonder redirect
@app.route('/api')
@app.route('/api/')
def hello_api():
    """Returns a simple greeting from the API."""
    return 'Hello from API!'

# De health check route
@app.route('/api/health')
def health_check():
    """Returns a health status for the API."""
    return jsonify(status="ok")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
