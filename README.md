r

Deze repository bevat Docker-bestanden en instructies voor het opzetten van een ontwikkelomgeving gericht op het aanleren van toekomstige vaardigheden. Hier vind je voorbeelden, documentatie en scripts om snel aan de slag te gaan met Docker in het kader van Future Skills.

## Inhoud

- Dockerfiles en configuratiebestanden
- Voorbeelden van gebruik
- Stapsgewijze instructies

## Gebruik

1. Clone deze repository:
    ```bash
    git clone https://github.com/SanderHuijbers/future-skills-docker.git
    ```
2. Navigeer naar de map scripts:
    ```bash
    cd future-skills-docker
    ```
3. Voer start.sh uit om een certificaat te genereren en de containers te starten.
   ```bash
   ./script/start.sh
   ```
4. Testen door naar de volgende url`s te gaan:
   ```http
      # Webserver
      https://localhost

      # API server
      https://localhost/api

      # Grafana
      https://localhost:3000 ```
5. Voer stop.sh uit om de containers te stopen.
   ```bash
   ./scripts/stop.sh
   ```

## Contributie

Voel je vrij om bij te dragen via pull requests of issues.
