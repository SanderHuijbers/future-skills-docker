# api-server/app.py

from flask import Flask, jsonify, Response
import socket # Importeer de socket module

app = Flask(__name__)

# Haal de hostname van de container op
# Dit wordt een naam van deze container.
CONTAINER_HOSTNAME = socket.gethostname()

# De hoofd-API-route accepteert nu zowel /api als /api/ zonder redirect
@app.route('/api')
@app.route('/api/')
def hello_api():
    """
    Retourneert een begroeting van de API met styling,
    inclusief de hostname en een unieke achtergrondkleur.
    """
    # Gebruik de eerste 6 karakters van de hostname als hex kleur
    # Zorg ervoor dat de string lang genoeg is om 6 karakters te pakken
    background_color_hex = CONTAINER_HOSTNAME[:6] if len(CONTAINER_HOSTNAME) >= 6 else "CCCCCC" # Fallback kleur
    
    # Genereer de HTML-inhoud met inline CSS
    html_content = f"""
    <!DOCTYPE html>
    <html lang="nl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Server Status</title>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh; /* Zorgt ervoor dat de body de hele viewport vult */
                margin: 0;
                font-family: 'Inter', sans-serif; /* Gebruik Inter font */
                background-color: #{background_color_hex}; /* Dynamische achtergrondkleur */
                transition: background-color 0.5s ease; /* Vloeiende overgang bij kleurverandering */
            }}
            .container {{
                text-align: center;
                padding: 2rem;
                background-color: rgba(255, 255, 255, 0.8); /* Semi-transparante witte achtergrond voor betere leesbaarheid */
                border-radius: 15px; /* Afgeronde hoeken */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtiele schaduw */
            }}
            h1 {{
                font-size: 3.5rem; /* Grotere tekst */
                color: black; /* Zwarte letters */
                text-shadow:
                    -2px -2px 0 #FFF, /* Witte randje */
                    2px -2px 0 #FFF,
                    -2px 2px 0 #FFF,
                    2px 2px 0 #FFF;
                margin: 0;
                padding: 0;
            }}
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    </head>
    <body>
        <div class="container">
            <h1>Hello from API! Running on host: {CONTAINER_HOSTNAME}</h1>
        </div>
    </body>
    </html>
    """
    return Response(html_content, mimetype='text/html')

# De health check route
@app.route('/api/health')
def health_check():
    """Returns a health status for the API, including the hostname."""
    # Voeg de hostname toe aan de JSON respons
    return jsonify(status="ok", hostname=CONTAINER_HOSTNAME)

if __name__ == '__main__':
    # Luister op alle beschikbare netwerkinterfaces
    app.run(host='0.0.0.0', port=5000)
