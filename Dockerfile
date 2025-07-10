FROM python:3.11-slim

WORKDIR /app
COPY check_new_episodes.py .

RUN pip install requests

CMD ["python", "check_new_episodes.py"]
