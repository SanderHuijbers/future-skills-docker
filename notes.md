## Fase 1

### Opdracht 1
/webserver/Dockerfile.webserver gemaakt

/webserver/index.html gamaakt

docker image gemaakt

```bash
docker build -t my-web-server-alpine .
```

Webserver container gestart

```bash
docker run -d --name web-alpine -p 8080:80 my-web-server-alpine
```

server-blok toegevoegd aan de nginx.conf (zie voorbeeld /webserver/nginx.conf)

```bash
http {
    # ...bestaande configuratie...

    server {
        listen 80;
        server_name localhost;

        root /usr/share/nginx/html;
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }
    }
}
```

Herstart de Nginx-server in de container:
`docker exec -it web-alpine nginx -s reload`

Het handmatig aanpassen van de nginx.conf is niet de bedoeling. Ik heb dit opgelost door een los bestand webserver/webserver.conf en een extra copy commando aan de Dockerfile toe te voegen.
Dit is de inhoud van het nieuwe /webserver/Dockerfile.webserver

```dockerfile
# Dockerfile.webserver voor de webserver
FROM alpine:latest

# Installeer Nginx
RUN apk add --no-cache nginx

# Kopieer de statische HTML pagina
COPY index.html /usr/share/nginx/html/

# Kopieer de custom Nginx configuratie
# Dit overschrijft/plaatst de default site configuratie
COPY webserver.conf /etc/nginx/conf.d/default.conf

# Maak log directories (Nginx draait vaak als non-root in productie, alhoewel de default Alpine image het als root start)
# RUN mkdir -p /var/log/nginx && \
#     chown -R nginx:nginx /var/log/nginx # Als je Nginx als 'nginx' user zou draaien

# Expose poort 80 (informatief voor Docker, niet functioneel voor host mapping)
EXPOSE 80

# Start Nginx in de foreground
CMD ["nginx", "-g", "daemon off;"]

```
#### Debuggen

```bash
docker run --rm -it my-web-server2-alpine cat /etc/nginx/nginx.conf
```

#### Testen

```bash
curl http://localhost:8080
```

#### opruimen
```bash
docker stop web-alpine
```

```bash
docker rm web-alpine
```


### Opdracht 2

#### Bouwen ./reverse-proxy/Dockerfile

```Dockerfile
# Dockerfile.reverse-proxy voor de Reverse Proxy
FROM alpine:latest

# Installeer Nginx
RUN apk add --no-cache nginx

# Kopieer de custom Nginx configuratie naar de juiste map
# De standaard nginx.conf in deze Alpine image includeert bestanden uit http.d
COPY reverse_proxy.conf /etc/nginx/http.d/default.conf

# === SSL/TLS Certificaten ===
# VOEG HIER REGELS TOE OM JE EIGEN SSL/TLS CERTIFICATEN TE KOPIEREN
# Bijvoorbeeld:
# RUN mkdir /etc/nginx/ssl
# COPY path/to/your/nginx.crt /etc/nginx/ssl/nginx.crt
# COPY path/to/your/nginx.key /etc/nginx/ssl/nginx.key
# Voor nu gebruiken we placeholder paden in de nginx.conf, maar je moet deze bestanden zelf leveren.

# Maak log directories
RUN mkdir -p /var/log/nginx && \
    chown -R nginx:nginx /var/log/nginx

# Expose poorten 80 en 443
EXPOSE 80
EXPOSE 443

# Start Nginx in de foreground
CMD ["nginx", "-g", "daemon off;"]

```

#### Bouwen ./reverse-proxy/reverse-proxy.conf

```conf
# Definieer de backend webservers
# Gebruik hier de naam van de webserver container of de service naam in een Docker Compose netwerk
upstream backend_webserver {
    # De naam 'web-alpine' is de containernaam die we in docker-compose.yml hebben gedefinieerd.
    server web-alpine:80;
}

server {
    listen 80;
    listen [::]:80;
    server_name _; # Luister op elke hostnaam

    # HTTP naar HTTPS redirect (optioneel, maar aanbevolen voor HTTPS)
    # return 301 https://$host$request_uri;

    location / {
        # Stuur verkeer door naar de backend webserver gedefinieerd in de upstream
        proxy_pass http://backend_webserver;

        # Voeg standaard headers toe voor proxying
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Optioneel: Verbeter logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
}

# HTTPS Server blok
# Vereist SSL/TLS certificaten
# Tijdelijk uitgecommentarieerd omdat we nog geen certificaten hebben.
# We zullen dit in Fase 3 activeren en configureren met self-signed certificaten.
# server {
#     # Correcte syntax voor http2 in nieuwere Nginx versies
#     listen 443 ssl http2;
#     listen [::]:443 ssl http2;
#     server_name _; # Luister op elke hostnaam

#     # === SSL/TLS Configuratie ===
#     # VERVANG DEZE DOOR JE EIGEN CERTIFICATEN
#     # Dit zijn placeholder paden en bestanden!
#     # We zullen later self-signed certificaten genereren en hier plaatsen.
#     ssl_certificate /etc/nginx/ssl/nginx.crt;
#     ssl_certificate_key /etc/nginx/ssl/nginx.key;

#     # Optionele SSL/TLS settings voor betere beveiliging (aanbevolen)
#     # ssl_session_cache wordt al gedefinieerd in de hoofd nginx.conf, dus verwijderen we het hier.
#     # ssl_session_cache shared:SSL:10m; # <-- VERWIJDERD
#     ssl_session_timeout 10m;
#     ssl_protocols TLSv1.2 TLSv1.3;
#     ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:DHE-RSA-AES128-SHA256:DHE-RSA-AES256-SHA256:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256';
#     ssl_prefer_server_ciphers on;
#     ssl_session_tickets off; # Vaak aanbevolen voor beveiliging

#     location / {
#         # Stuur verkeer door naar de backend webserver gedefinieerd in de upstream
#         proxy_pass http://backend_webserver;

#         # Voeg standaard headers toe voor proxying
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#     }

#     # Optioneel: Verbeter logging
#     access_log /var/log/nginx/access.log;
#     error_log /var/log/nginx/error.log;
# }

```

#### Bouwen van de reverse-proxy container

```bash
docker build -t my-reverse-proxy -f Dockerfile.reverse-proxy .
```

#### Conclusie
De 2 containers kunnen elkaar niet goed bereiken, en dat wordt wel gedaan in opdracht 3

### Opdracht 3

#### Maak een ./docker-compose.yml file aan

```yml
# docker-compose.yml
# Definieert de webserver en reverse proxy services in een custom netwerk

version: '3.8' # Gebruik een recente Docker Compose versie

services:

  # Service voor de statische webserver
  webserver:
    image: my-web-server2-alpine # Gebruik de naam van jouw webserver image
    container_name: web-alpine # Optionele, maar handige, containernaam
    build:
      context: ./webserver # Ga ervan uit dat je Dockerfile en index.html hier staan
      dockerfile: Dockerfile.webserver # De naam van je Dockerfile voor de webserver
    # BELANGRIJK: Map poort 80 van de webserver container NIET naar de host.
    # De reverse proxy regelt de toegang.
    # ports:
    #   - "80:80" # DEZE REGEL UITCOMMENTARIEREN OF VERWIJDEREN!
    networks:
      - web-network # Plaats deze service in ons custom netwerk
    restart: always # Start automatisch opnieuw op

  # Service voor de Nginx reverse proxy
  reverse-proxy:
    image: my-reverse-proxy # Gebruik de naam van jouw reverse proxy image
    container_name: reverse-proxy # Optionele, maar handige, containernaam
    build:
      context: ./reverse-proxy # Ga ervan uit dat je Dockerfile en reverse_proxy.conf hier staan
      dockerfile: Dockerfile.reverse-proxy # De naam van je Dockerfile voor de reverse proxy
    ports:
      - "80:80"   # Map poort 80 van de container naar poort 80 op de host
      - "443:443" # Map poort 443 van de container naar poort 443 op de host
    networks:
      - web-network # Plaats deze service in ons custom netwerk
    restart: always # Start automatisch opnieuw op
    # Zorg ervoor dat de webserver service is opgestart voordat de reverse proxy start (optioneel maar goed voor afhankelijkheden)
    depends_on:
      - webserver

# Definieer het custom netwerk
networks:
  web-network:
    driver: bridge # Gebruik het standaard bridge netwerk type
    name: my-web-platform-network # Geef het netwerk een duidelijke naam


```

#### Compose het ./docker-compose.yml

```bash
docker compose up -d
```

#### Conclusie

Om de docker compose goe te laten werken moest in docker compose eerst installeren. Daarna heb ik het https gedeelte uit de reverse-proxy.conf moeten uitcommentarieeren.

### Opdracht 4

Code aan reverse-proxy.conf toegevoegd

```conf
    # Blokkeer TRACE en OPTIONS methoden
    if ($request_method ~* "(TRACE|OPTIONS)") {
        return 405;
    }

    # Stel beveiligingsheaders in
    add_header X-Frame-Options "DENY";
    add_header Content-Security-Policy "default-src 'self'";
```

### Opdracht 5

#### chown

Zie Dockerfiles
```bash
# Maak log directories
RUN mkdir -p /var/log/nginx && \
    chown -R nginx:nginx /var/log/nginx
```

#### chmod

zie Dockerfiles
```bash
# Voorbeeld in Dockerfile na COPY index.html
RUN chmod 644 /usr/share/nginx/html/index.html
```

#### ip a

```bash
docker exec web-alpine ip a
docker exec reverse-proxy ip a
```

#### ping 
```bash
docker exec web-alpine ping reverse-proxy
```

#### curl

```bash
docker exec reverse-proxy curl http://web-alpine:80
```

### Opdracht 6

```bash
curl -i http://localhost



HTTP/1.1 200 OK
Server: nginx
Date: Fri, 02 May 2025 15:21:23 GMT
Content-Type: text/html
Content-Length: 381
Connection: keep-alive
Last-Modified: Thu, 01 May 2025 13:38:23 GMT
ETag: "6813794f-17d"
Accept-Ranges: bytes
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'

<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Main page</title>
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="">
</head>

<body>
    <h1>Hello from Web Server via Reverse Proxy!</h1>
</body>
```
