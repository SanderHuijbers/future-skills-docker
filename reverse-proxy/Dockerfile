# Dockerfile voor de Reverse Proxy
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
