# DeepBindDTA (Preview)

## 📌 Project overview
A deep learning framework for Drug–Target Affinity (DTA) prediction. Includes models, datasets, and utility scripts for training and evaluation.

---

## ▶️ Quick start (Windows / .venv)

### 1) Create the virtual environment
Run the bootstrap script (it creates/rebuilds `.venv` and installs `requirements.txt`):

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_py39.ps1
```

If you want to force a specific Python interpreter (recommended when your `python` in PATH is the Windows Store alias), set `VENV_PYTHON`:

```powershell
$env:VENV_PYTHON = "C:\\Path\\To\\python.exe"
powershell -ExecutionPolicy Bypass -File .\setup_py39.ps1
```

### 2) (Optional) Configure database connection
The GUI uses MySQL. You can override defaults via environment variables:

- `DB_HOST` (default: `localhost`)
- `DB_PORT` (default: `3306`)
- `DB_USER` (default: `root`)
- `DB_PASSWORD`
- `DB_NAME` (default: `drug_discovery`)

Example (current PowerShell session):

```powershell
$env:DB_HOST = "127.0.0.1"
$env:DB_USER = "root"
$env:DB_PASSWORD = "12345"
$env:DB_NAME = "drug_discovery"
```

#### Use Docker to start MySQL (recommended)
This repo includes a minimal `docker-compose.yml` that starts MySQL for local development.

```powershell
docker compose up -d
```

To import the provided SQL dump into Docker MySQL (optional, large file):

```powershell
powershell -ExecutionPolicy Bypass -File .\db_import_docker.ps1
```

Note: the SQL dump is large; the import can take a long time.

If you want to customize credentials/port for Docker, set these env vars before running compose:

- `MYSQL_ROOT_PASSWORD` (default: `12345`)
- `MYSQL_DATABASE` (default: `drug_discovery`)
- `MYSQL_PORT` (default: `3306`)

### 3) Run
Start the GUI:

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

Run prediction script:

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1 pred
```

---

## 🔧 Git Large File Storage (Git LFS) — Usage
This repository uses Git LFS to store large binary/model files. This keeps the Git history lightweight and avoids GitHub file-size restrictions.

### What is tracked (examples)
- Tracked patterns (glob): `*.pth`, `*.pkl`, `*.pt`, `*.h5`, `*.ckpt`, `*.onnx`
- Some specific large files moved to LFS: `database/test.sql`, `database/test_fixed.sql`, `model_300dim.pkl`, `savemodel/*.pth`

### Common commands
- Install/enable LFS locally (once):
  ```bash
  git lfs install
  ```
- After cloning the repository, fetch LFS objects:
  ```bash
  git lfs pull
  ```
- See which files are tracked by LFS locally:
  ```bash
  git lfs ls-files
  ```
- To add new file types to be tracked (example):
  ```bash
  git lfs track "*.ckpt" "*.onnx"
  git add .gitattributes
  git add <large-file>
  git commit -m "chore: track <ext> with Git LFS"
  git push
  ```

> Note: Track file types *before* committing large files so that they are stored in LFS from the start.

### Rewriting history / collaborator notice
The repository history was rewritten to migrate existing large files into LFS. Backup branches were created:
- `backup/main-before-lfs`
- `backup/main-before-lfs-2`

If you have a local clone or fork, the safest way to synchronize is to reclone the repository:
```bash
# safest (recommended)
git clone https://github.com/LemuSakuya/DeepBindDTA--Preview-.git
cd DeepBindDTA--Preview-
# fetch LFS objects
git lfs pull
```
If you cannot reclone, you can reset to the remote `main`:
```bash
git fetch origin
git reset --hard origin/main
git lfs pull
```

---

## 📎 Notes & Contact
If you want additional extensions or size thresholds tracked by LFS (e.g., images, CSVs, database dumps), open an issue or contact the maintainer and we will update `.gitattributes` and migrate history accordingly.z