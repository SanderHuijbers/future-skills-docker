from flask import Flask, jsonify
import socket # Importeer de socket module

app = Flask(__name__)

# Haal de hostname van de container op
# Dit wordt een naam van deze container.
CONTAINER_HOSTNAME = socket.gethostname()

# De hoofd-API-route accepteert nu zowel /api als /api/ zonder redirect
@app.route('/api')
@app.route('/api/')
def hello_api():
    """Returns a simple greeting from the API, including the hostname."""
    # Voeg de hostname toe aan de respons
    return f'Hello from API! Running on host: {CONTAINER_HOSTNAME}'

# De health check route
@app.route('/api/health')
def health_check():
    """Returns a health status for the API, including the hostname."""
    # Voeg de hostname toe aan de JSON respons
    return jsonify(status="ok", hostname=CONTAINER_HOSTNAME)

if __name__ == '__main__':
    # Luister op alle beschikbare netwerkinterfaces
    app.run(host='0.0.0.0', port=5000)
