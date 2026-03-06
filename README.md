# DeepBindDTA

<p align="center">
  <a href="#english">English</a> | <a href="#中文说明">中文</a>
</p>

---

<a name="english"></a>

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
| ``app.py`` | Main GUI application (~2000 lines, Tkinter) |
| ``llmdta.py`` | LLMDTA neural network model |
| ``attention_blocks.py`` | Bilinear attention & Transformer blocks |
| ``dataset.py`` | PyTorch Dataset and DataLoader |
| ``model_config.py`` | Model hyperparameters |
| ``utils.py`` | Feature extraction (Mol2Vec / ESM-2) with caching |
| ``data_extractor.py`` | Drug/protein data extraction utilities |
| ``config.py`` | Global configuration (paths, DB, GUI) |
| ``pred.py`` | Standalone batch prediction script |
| ``deploy.ps1`` | **One-click deployment script** |

---

## 🚀 Quick Start

### Prerequisites

- Windows 10/11
- Python 3.9 ([download](https://www.python.org/downloads/release/python-3913/))
- Docker Desktop (for MySQL) — [download](https://www.docker.com/products/docker-desktop/)
- Git LFS — ``git lfs install``

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
| ``DB_HOST`` | ``localhost`` | MySQL host |
| ``DB_PORT`` | ``3306`` | MySQL port |
| ``DB_USER`` | ``root`` | MySQL user |
| ``DB_PASSWORD`` | ``12345`` | MySQL password |
| ``DB_NAME`` | ``drug_discovery`` | Database name |

---

## 🔧 Git LFS

This repository uses **Git LFS** for large binary files (``*.pth``, ``*.pkl``, ``*.pt``, ``*.h5``, ``*.ckpt``, ``*.onnx``, SQL dumps).

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

---

---

<a name="中文说明"></a>

## 📌 项目简介

**DeepBindDTA** 是一个融合深度学习、知识图谱与大语言模型（LLM）的智能药物关系分析系统，主要功能包括：

- **药物-靶标亲和力（DTA）预测** — 基于 Mol2Vec + ESM-2 双编码器 + 双线性注意力机制
- **药物-药物相互作用（DDI）分析** — 有向符号图可视化
- **药物与蛋白质查询** — 支持别名解析的数据库实体搜索
- **AI 智能助手** — 基于 LangChain Agent，集成本地工具调用

### 🏗️ 系统架构

```
┌─────────────────────────────────────────────────┐
│               GUI 主程序 (app.py)               │
│  药物查询 │ DDI 分析 │ DTA 预测 │ AI 智能助手  │
└──────────────────┬──────────────────────────────┘
                   │
       ┌───────────┴───────────┐
       ▼                       ▼
  MySQL 数据库              LLMDTA 模型
  (drug_discovery)   (llmdta.py + attention_blocks.py)
       │                       │
  DDI/DTI 数据           Mol2Vec + ESM-2
  知识图谱                   特征提取
```

### 📁 核心文件说明

| 文件 | 说明 |
|------|------|
| ``app.py`` | GUI 主程序（~2000 行，Tkinter） |
| ``llmdta.py`` | LLMDTA 神经网络模型定义 |
| ``attention_blocks.py`` | 双线性注意力 & Transformer 模块 |
| ``dataset.py`` | PyTorch 数据集与数据加载器 |
| ``model_config.py`` | 模型超参数配置 |
| ``utils.py`` | 特征提取工具（Mol2Vec / ESM-2，含缓存机制） |
| ``data_extractor.py`` | 药物/蛋白质数据提取工具 |
| ``config.py`` | 全局配置（路径、数据库、GUI） |
| ``pred.py`` | 独立批量预测脚本 |
| ``deploy.ps1`` | **一键部署脚本** |

---

## 🚀 快速开始

### 环境要求

- Windows 10/11
- Python 3.9（[下载地址](https://www.python.org/downloads/release/python-3913/)）
- Docker Desktop（用于 MySQL）— [下载地址](https://www.docker.com/products/docker-desktop/)
- Git LFS — ``git lfs install``

### 方式一：一键部署（推荐）

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy.ps1
```

该脚本将自动完成：
1. 创建/修复 Python 虚拟环境并安装依赖
2. 通过 Docker 启动 MySQL 容器
3. 询问是否导入 SQL 数据库
4. 启动 GUI 主程序

其他部署模式：

```powershell
# 已有外部 MySQL，跳过 Docker
.\deploy.ps1 -SkipDocker

# 强制导入 SQL 数据（首次部署）
.\deploy.ps1 -ImportSQL

# 仅运行预测脚本，不启动 GUI
.\deploy.ps1 -PredOnly
```

### 方式二：手动部署

**第一步：创建虚拟环境**

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_py39.ps1
```

指定 Python 路径（可选）：

```powershell
$env:VENV_PYTHON = "C:\Path\To\python.exe"
powershell -ExecutionPolicy Bypass -File .\scripts\setup_py39.ps1
```

**第二步：通过 Docker 启动 MySQL**

```powershell
docker compose up -d
```

自定义数据库配置（可选）：

```powershell
$env:MYSQL_ROOT_PASSWORD = "yourpassword"
$env:MYSQL_DATABASE      = "drug_discovery"
$env:MYSQL_PORT          = "3306"
docker compose up -d
```

**第三步：导入数据库**（可选，文件较大）

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\db_import_docker.ps1
```

**第四步：运行程序**

```powershell
# 启动 GUI
powershell -ExecutionPolicy Bypass -File .\run.ps1

# 运行批量预测
powershell -ExecutionPolicy Bypass -File .\run.ps1 pred
```

### 数据库环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| ``DB_HOST`` | ``localhost`` | MySQL 主机地址 |
| ``DB_PORT`` | ``3306`` | MySQL 端口 |
| ``DB_USER`` | ``root`` | MySQL 用户名 |
| ``DB_PASSWORD`` | ``12345`` | MySQL 密码 |
| ``DB_NAME`` | ``drug_discovery`` | 数据库名称 |

---

## 🔧 Git LFS 说明

本仓库使用 **Git LFS** 管理大型文件（``*.pth``, ``*.pkl``, ``*.pt``, ``*.h5``, ``*.ckpt``, ``*.onnx`` 及 SQL 转储文件）。

```bash
# 克隆后拉取所有 LFS 对象
git lfs install
git lfs pull
```

> **提示：** 如果已有本地克隆，最安全的更新方式是重新克隆：
> ```bash
> git clone https://github.com/LemuSakuya/DeepBindDTA--Preview-.git
> cd DeepBindDTA--Preview-
> git lfs pull
> ```

---

## 📎 联系与反馈

如有问题、Bug 报告或 LFS 追踪需求，请在 GitHub 上提交 Issue。
