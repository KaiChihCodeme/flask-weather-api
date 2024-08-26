FROM python:3.11
EXPOSE 5001

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:create_app()"]