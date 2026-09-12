FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /Project

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY Project/ .

RUN useradd -m -u 1000 appuser
RUN chown -R appuser:appuser /Project
USER appuser

CMD ["python", "main.py"]