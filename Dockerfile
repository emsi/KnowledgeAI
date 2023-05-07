FROM emsi/deep-learning:11.7.1-cudnn8-runtime-ubuntu22.04

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY app /app

WORKDIR /

CMD ["python3", "-m", "streamlit", "run", "/app/app.py", "--server.port", "8501", "--server.enableCORS", "false"]