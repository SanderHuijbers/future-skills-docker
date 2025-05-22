# Gebruik een Alpine-gebaseerde Python image
FROM python:3.9-alpine

# Stel de working directory in de container in
WORKDIR /app

# Kopieer het requirements.txt bestand en installeer de afhankelijkheden
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de rest van de applicatiebestanden
COPY . .

# Expose de poort waarop de Flask app luistert
EXPOSE 5000

# Start de Flask applicatie
CMD ["python", "app.py"]
