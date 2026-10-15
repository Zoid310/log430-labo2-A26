FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie le projet (pyproject.toml + src/) pour que l'image soit autonome,
# même sans le volume monté par docker-compose (ex. image publiée sur GHCR).
COPY . .

WORKDIR /app/src
CMD ["python", "store_manager.py"]
