# IsleGo Booking — Local Development

This is a simple Flask-based mock booking application styled as a travel agency.

Run locally:

```powershell
cd "C:\Users\reyan\OneDrive\Desktop\New folder"
$env:FLASK_APP='app/app.py'
C:\Users\reyan\AppData\Local\Programs\Python\Python312\python.exe -m flask run --host 127.0.0.1 --port 5000
```

What's added:
- Gallery hero and featured destination descriptions
- Destination cards with images and short descriptions
- `static/styles.css` for improved visuals

Next steps:
- Replace the placeholder images with your attached images by saving them into `app/static/images/` and updating the `src` attributes in `index.html`.

Run locally (dev):

PowerShell:
```powershell
cd "C:\Users\reyan\OneDrive\Desktop\New folder"
$env:FLASK_APP='app.app'
python -m flask run --host 127.0.0.1 --port 5000
```

Linux / macOS:
```bash
export FLASK_APP=app.app
python -m flask run --host 0.0.0.0 --port 5000
```

Run with Docker (recommended for publishing):

Build and run locally:
```bash
docker build -t islego:latest .
docker run -p 5000:5000 islego:latest
```

Publish via Docker Hub (example):
```bash
docker tag islego:latest <your-dockerhub-username>/islego:latest
docker push <your-dockerhub-username>/islego:latest
```

Heroku / similar hosts:
- Use the provided `Procfile` which starts the app with `gunicorn`.

CI/CD template:
- See `.github/workflows/docker-publish.yml` for a GitHub Actions example that builds and pushes a Docker image (you must configure `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` in repository secrets).

If you want, I can set up the GitHub Actions file with your DockerHub repo name and help configure secrets.
