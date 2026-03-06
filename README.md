# DeepBindDTA

<p align="right">
  <a href="README.md"><b>English</b></a> | <a href="README.zh.md">中文</a>
</p>

## 📌 Project Overview

**DeepBindDTA** is an intelligent drug relationship analysis system that integrates deep learning, knowledge graphs, and large language models (LLMs). It is designed for:

- **Drug–Target Affinity (DTA) Prediction** — dual-encoder architecture (Mol2Vec + ESM-2) with bilinear attention
- **Drug–Drug Interaction (DDI) Analysis** — signed directed graph visualization
- **Drug & Protein Query** — database-backed entity search with alias resolution
- **AI Assistant** — LangChain-powered agent with local tool integration

### 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│                  GUI (app.py)               │
│  Drug Query │ DDI Analysis │ DTA Prediction │
│             │  3D Viewer   │  AI Assistant  │
└──────────────────┬──────────────────────────┘
                   │
       ┌───────────┴───────────┐
       ▼                       ▼
  MySQL Database          LLMDTA Model
  (drug_discovery)    (llmdta.py + attention_blocks.py)
       │                       │
  DDI / DTI data        Mol2Vec + ESM-2
  Knowledge Graph         features
```

### 📁 Key Files

| File | Description |
|------|-------------|
| `app.py` | Main GUI application (~2000 lines, Tkinter) |
| `llmdta.py` | LLMDTA neural network model |
| `attention_blocks.py` | Bilinear attention & Transformer blocks |
| `dataset.py` | PyTorch Dataset and DataLoader |
| `model_config.py` | Model hyperparameters |
| `utils.py` | Feature extraction (Mol2Vec / ESM-2) with caching |
| `data_extractor.py` | Drug/protein data extraction utilities |
| `config.py` | Global configuration (paths, DB, GUI) |
| `pred.py` | Standalone batch prediction script |
| `deploy.ps1` | **One-click deployment script** |

---

## 🚀 Quick Start

### Prerequisites

- Windows 10/11
- Python 3.9 ([download](https://www.python.org/downloads/release/python-3913/))
- Docker Desktop (for MySQL) — [download](https://www.docker.com/products/docker-desktop/)
- Git LFS — `git lfs install`

### Option A — One-click Deploy (Recommended)

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy.ps1
```

This will automatically:
1. Create/repair the Python virtual environment
2. Start MySQL via Docker
3. Ask whether to import the SQL database dump
4. Launch the GUI

Other deploy modes:

```powershell
# Already have external MySQL, skip Docker
.\deploy.ps1 -SkipDocker

# Force import SQL data (first time)
.\deploy.ps1 -ImportSQL

# Run prediction script only (no GUI)
.\deploy.ps1 -PredOnly
```

### Option B — Manual Setup

**Step 1: Create virtual environment**

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_py39.ps1
```

To use a specific Python interpreter:

```powershell
$env:VENV_PYTHON = "C:\Path\To\python.exe"
powershell -ExecutionPolicy Bypass -File .\scripts\setup_py39.ps1
```

**Step 2: Start MySQL via Docker**

```powershell
docker compose up -d
```

Custom credentials (optional):

```powershell
$env:MYSQL_ROOT_PASSWORD = "yourpassword"
$env:MYSQL_DATABASE      = "drug_discovery"
$env:MYSQL_PORT          = "3306"
docker compose up -d
```

**Step 3: Import database dump** (optional, large file)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\db_import_docker.ps1
```

**Step 4: Run**

```powershell
# Launch GUI
powershell -ExecutionPolicy Bypass -File .\run.ps1

# Run batch prediction
powershell -ExecutionPolicy Bypass -File .\run.ps1 pred
```

### Database Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | `localhost` | MySQL host |
| `DB_PORT` | `3306` | MySQL port |
| `DB_USER` | `root` | MySQL user |
| `DB_PASSWORD` | `12345` | MySQL password |
| `DB_NAME` | `drug_discovery` | Database name |

---

## 🔧 Git LFS

This repository uses **Git LFS** for large binary files (`*.pth`, `*.pkl`, `*.pt`, `*.h5`, `*.ckpt`, `*.onnx`, SQL dumps).

```bash
# After cloning, fetch all LFS objects
git lfs install
git lfs pull
```

> **Note:** If you have an existing clone, the safest update is to reclone:
> ```bash
> git clone https://github.com/LemuSakuya/DeepBindDTA--Preview-.git
> cd DeepBindDTA--Preview-
> git lfs pull
> ```

---

## 📎 Contact

Open an issue on GitHub for questions, bugs, or LFS tracking requests.
