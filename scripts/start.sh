#!/bin/bash

# start.sh
# Dit script genereert een nieuw zelfondertekend SSL-certificaat
# en start vervolgens de Docker Compose services.

echo "--- Genereren van zelfondertekende SSL-certificaten ---"
# Zorg ervoor dat het generate_certs.sh script uitvoerbaar is
chmod +x generate_certs.sh
# Voer het script uit om nieuwe certificaten te genereren
./generate_certs.sh

echo "--- Starten van Docker Compose services ---"
# Start de Docker Compose services op de achtergrond (-d)
# en wacht tot ze 'healthy' zijn (--wait)
docker compose up -d --wait

echo "Applicatie succesvol gestart."
echo "Je kunt de webserver benaderen via https://localhost"
echo "De API is beschikbaar via https://localhost/api"
