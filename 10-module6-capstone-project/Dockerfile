FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/api.py src/api.py
COPY src/sentiment_model.pkl src/sentiment_model.pkl

EXPOSE 5000

# Cloudflare Containers (and most container platforms) expect the app to
# listen on the port they inject via $PORT; default to 5000 for local runs.
ENV PORT=5000
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 2 --chdir src api:app"]
