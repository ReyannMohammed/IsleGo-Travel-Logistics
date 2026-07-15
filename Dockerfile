FROM python:3.12-slim
WORKDIR /app

# install system deps (if any) and python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY . .

ENV FLASK_APP=app.app
ENV FLASK_ENV=production
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]
