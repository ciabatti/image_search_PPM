# Usa un'immagine di base Python
FROM python:3.10-slim

# Imposta la directory di lavoro nel contenitore
WORKDIR /app

# Copia il file di requisiti nella directory di lavoro
COPY requirements.txt /app/

# Installa le dipendenze
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione nella directory di lavoro
COPY . /app/

# Imposta le variabili di ambiente per Django
ENV PYTHONUNBUFFERED=1

# Espone la porta che Gunicorn userà
EXPOSE 8000

# Comando per avviare Gunicorn
CMD ["gunicorn", "image_search.wsgi:application", "--bind", "0.0.0.0:8000"]
