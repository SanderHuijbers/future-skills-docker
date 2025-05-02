# Dockerfile voor de webserver
FROM alpine:latest

# Installeer Nginx
RUN apk add --no-cache nginx

# Kopieer de statische HTML pagina
COPY index.html /usr/share/nginx/html/

# Kopieer de custom Nginx configuratie
# Dit overschrijft/plaatst de default site configuratie
COPY webserver.conf /etc/nginx/http.d/default.conf

# Maak log directories (Nginx draait vaak als non-root in productie, alhoewel de default Alpine image het als root start)
# RUN mkdir -p /var/log/nginx && \
#     chown -R nginx:nginx /var/log/nginx # Als je Nginx als 'nginx' user zou draaien

# Expose poort 80 (informatief voor Docker, niet functioneel voor host mapping)
EXPOSE 80

# Start Nginx in de foreground
CMD ["nginx", "-g", "daemon off;"]