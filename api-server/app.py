from flask import Flask, jsonify

app = Flask(__name__)

# De route accepteert nu zowel /api als /api/
@app.route('/api/', defaults={'path': ''})
@app.route('/api/<path:path>')
def hello_api(path):
    """Returns a simple greeting from the API or handles sub-paths."""
    if path == '':
        return 'Hello from API!'
    elif path == 'health':
        # Dit is de health check, die we nu ook via deze catch-all route afhandelen
        return jsonify(status="ok")
    else:
        return f"Hello from API at sub-path: /{path}!"

# De aparte @app.route('/api/health') is nu overbodig en kan verwijderd worden
# omdat de catch-all route '/api/<path:path>' deze nu afhandelt.
# Als je liever aparte routes houdt, kunnen we dat ook doen, maar dit is flexibeler.
# @app.route('/api/health')
# def health_check():
#     """Returns a health status for the API."""
#     return jsonify(status="ok")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
