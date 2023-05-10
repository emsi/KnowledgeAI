FROM emsi/deep-learning:11.7.1-cudnn8-runtime-ubuntu22.04

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY app /app

WORKDIR /app

CMD ["python3", "-m", "streamlit", "run", "./app.py", "--server.port", "8501", "--browser.gatherUsageStats", "false"]
