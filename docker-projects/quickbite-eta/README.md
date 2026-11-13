# QuickBite ETA 🛵

A food-delivery **ETA predictor** built with scikit-learn + FastAPI, fully dockerized.
Part of the *Dockerize Everything: ML → LLM → Agents* masterclass.

> **Predicts:** how many minutes until a food order arrives, based on distance,
> restaurant prep time, rider availability, and whether it's raining.

---

## 📁 What's in this folder

| File | Purpose |
|---|---|
| `train.py` | Generates synthetic delivery data and trains a RandomForest → saves `eta_model.pkl` |
| `app.py` | FastAPI service that loads the model and exposes `/predict` |
| `requirements.txt` | Pinned Python dependencies (the "shopping list") |
| `Dockerfile` | The recipe — how to build the container image |
| `.dockerignore` | Files that should NOT go into the image |
| `README.md` | This file |

---

## ✅ Prerequisites

1. **Docker Desktop** installed and running:
   - **Windows:** Download and install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) (requires WSL 2 backend).
   - **macOS:** Install via Homebrew:
     ```bash
     brew install --cask docker
     ```
   - Launch Docker Desktop. Ensure the whale 🐳 icon appears in your system tray / menu bar and indicates that the engine is running.

2. Verify Docker is running:
   ```bash
   docker --version
   docker run hello-world
   ```

You do **not** need Python, pip, or a local virtual environment installed to run the Dockerized container.

---

## 🚀 Step-by-step: run this project

### Step 1 — Navigate to the project directory
From the repository root, open your terminal and navigate to this folder:

```powershell
# Windows PowerShell / macOS / Linux:
cd docker-projects/quickbite-eta
```

*(Alternatively, you can build directly from the repository root by specifying the context path `./docker-projects/quickbite-eta`)*

### Step 2 — Verify Docker Desktop is running
Ensure Docker Desktop is open and the status shows "Engine running".

### Step 3 — Build the Docker image
Run the following build command:

```bash
docker build -t quickbite-eta:v1 .
```

*Or from the repository root:*
```powershell
docker build -t quickbite-eta:v1 ./docker-projects/quickbite-eta
```

The first build may take **2–3 minutes** while it pulls `python:3.12-slim` and installs dependencies. Notice that `train.py` executes inside the image during build time, creating `eta_model.pkl` inside the image layer.

Confirm the image is created:
```bash
docker images
```

### Step 4 — Run the container
```bash
docker run -d -p 8000:8000 --name eta-service quickbite-eta:v1
```

- `-d` → run in background (detached mode)
- `-p 8000:8000` → map local port 8000 to container port 8000
- `--name eta-service` → friendly name for the container instance

Verify it is running:
```bash
docker ps
```

### Step 5 — Test the API

**Option A — Windows PowerShell (Invoke-RestMethod):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -ContentType "application/json" -Body '{"distance_km": 4.5, "prep_time_min": 15, "rider_available": 1, "is_raining": 1}'
```

**Option B — curl (macOS / Linux / Git Bash / curl.exe):**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"distance_km": 4.5, "prep_time_min": 15, "rider_available": 1, "is_raining": 1}'
```

Expected JSON response:
```json
{"eta_minutes": 40.5, "message": "Your food arrives in 40.5 min 🍔"}
```

**Option C — Swagger UI (Browser):**
Open **http://localhost:8000/docs** in your browser, expand `POST /predict`, click **Try it out**, edit values, and hit **Execute**.

### Step 6 — Explore the running container (optional)
```bash
docker logs -f eta-service          # view live logs (Ctrl+C to exit)
docker exec -it eta-service bash    # step inside the container
  ls                                # see app.py, eta_model.pkl, etc.
  cat app.py
  exit
```

### Step 7 — Stop and Clean up
```bash
docker stop eta-service
docker rm eta-service
docker rmi quickbite-eta:v1         # optional: remove image
```

---

## 🐍 Optional: run locally WITHOUT Docker

```powershell
# Windows (PowerShell):
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train.py
uvicorn app:app --reload
```

```bash
# macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python train.py
uvicorn app:app --reload
```

Then visit **http://localhost:8000/docs**.
Deactivate with `deactivate` when finished.

---

## 🍎 Apple Silicon (M1/M2/M3/M4) note

If you hit a platform mismatch warning or plan to deploy this image to a cloud
server (which is usually x86), build for AMD64:

```bash
docker build --platform linux/amd64 -t quickbite-eta:v1 .
docker run --platform linux/amd64 -d -p 8000:8000 --name eta-service quickbite-eta:v1
```

---

## 🪤 Troubleshooting

| Problem | Fix |
|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop isn't open. Launch it and wait for the whale icon. |
| `port is already allocated` | Something else is on 8000. Find it with `lsof -i :8000` (macOS/Linux) or `Get-NetTCPConnection -LocalPort 8000` (Windows PowerShell), or use a different host port: `-p 8080:8000` (then test on `localhost:8080`). |
| `The container name "/eta-service" is already in use` | Remove the old one: `docker rm -f eta-service` |
| Build is very slow / disk full | Check usage with `docker system df`, then clean up with `docker system prune` |
| Platform / arch warning | Add `--platform linux/amd64` to build and run |
| Code changes not showing up | You must rebuild: `docker build -t quickbite-eta:v1 .` then re-run |

---

## 🔑 Key concepts demonstrated here

- **Dockerfile anatomy** — `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`
- **Layer caching** — `requirements.txt` is copied *before* the rest of the code, so
  dependency installation is cached and only re-runs when dependencies actually change
- **Port mapping** — `-p host:container`
- **`.dockerignore`** — keeping `venv/`, `.git/`, and secrets out of the image
- **Build-time training** — the model is baked into the image, so the container is
  fully self-contained at runtime


