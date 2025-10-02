# docker/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -U pip && pip install -e .
EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
