FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Startup script: write credentials, run migrations, start server
RUN printf '#!/bin/sh\n\
if [ -n "$GOOGLE_CREDENTIALS_JSON" ]; then\n\
  echo "$GOOGLE_CREDENTIALS_JSON" > /app/credentials.json\n\
fi\n\
python -m src.infrastructure.database.migrate --seed\n\
exec uvicorn src.main:app --host 0.0.0.0 --port 8080\n' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 8080

CMD ["/app/start.sh"]
