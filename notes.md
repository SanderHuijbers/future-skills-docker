## Fase 1

### Opdracht 1
/webserver/Dockerfile gemaakt

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
Dit is de inhoud van het nieuwe /webserver/Dockerfile

```dockerfile
# Dockerfile voor de webserver
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

`curl http://localhost:8080`

#### opruimen
`docker stop web-alpine`

`docker rm web-alpine`




### Opdracht 2