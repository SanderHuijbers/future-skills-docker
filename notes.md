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

#### Testen

`curl http://localhost:8080`

#### opruimen
`docker stop web-alpine`

`docker rm web-alpine`

