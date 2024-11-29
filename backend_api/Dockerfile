FROM python:3.12-alpine3.20
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY app.py ./
CMD ["gunicorn", "-w", "8", "app:app", "--bind", "0.0.0.0:5000"]