#!/bin/bash

# stop.sh
# Dit script stopt en verwijdert alle Docker Compose services en hun netwerken.

echo "--- Stoppen van Docker Compose services ---"
# Stop en verwijder de Docker Compose services en hun netwerken
docker compose down

echo "Applicatie succesvol gestopt en opgeruimd."
