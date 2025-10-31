# 🧠 AI-powered Personalized Workout & Nutrition Coach

An end-to-end **AI-driven system** that generates **personalized workout and nutrition recommendations** based on user input — built to demonstrate advanced proficiency in **Machine Learning**, **MLOps**, and **Cloud Deployment**.

Hosted entirely on **AWS EC2**, the project integrates **ETL, training, and inference pipelines**, **model versioning with DVC**, **experiment tracking with MLflow**, and a **hybrid AI chatbot** capable of both retrieval and generative responses.

---

## 🎯 Project Objective

The goal of this project is to showcase a **complete MLOps lifecycle**, from data ingestion to cloud deployment, while solving a real-world problem — helping users receive AI-based **fitness and nutrition guidance**.

**Key Highlights**

* End-to-end ML lifecycle automation (ETL → Train → Inference)
* Cloud-native MLOps integration with AWS
* Hybrid chatbot (retrieval + generative)
* Dockerized API deployed via CI/CD to EC2
* Data versioning and experiment tracking using DVC + MLflow

---

## 🧩 Features

### 🏋️ Personalized Recommendations

* Suggests **workouts** (type, duration, difficulty)
* Recommends **meals** (nutritional value breakdown)
* Predictions powered by ML pipelines with preprocessing (scaling, encoding, KNN imputation, label encoding)

### 💬 Intelligent Chatbot

* Hybrid model combining **retrieval** and **generative** approaches
* Uses embeddings from `all-MiniLM-L6-v2` for context retrieval
* Generates answers via `google/gemma-2-2b-it` (Hugging Face Inference API)
* Automatically switches between retrieval and generative modes based on similarity threshold

### ☁️ Full MLOps Integration

* **ETL Pipeline:** Pulls raw data from PostgreSQL (AWS RDS), performs transformations, and stores processed data in AWS S3 via DVC
* **Training Pipeline:** Fetches processed data from S3, runs DVC stages, and tracks model performance using MLflow + Dagshub
* **Inference Pipeline:** Loads latest model from S3/DVC for serving predictions through a FastAPI endpoint

### 🐳 Deployment & CI/CD

* **Dockerized FastAPI application** for reproducible inference environment
* **GitHub Actions** for continuous deployment to AWS EC2
* **Entrypoint script** automates data seeding, model retrieval, and API startup

---

## 🏗️ Architecture Overview

```
           ┌───────────────────────────┐
           │ Synthetic CSV Data        │
           │ • Workouts (100)          │
           │ • Nutrition (100)         │
           │ • FAQs (20)               │
           └─────────────┬─────────────┘
                         │
           ┌─────────────▼─────────────┐
           │ PostgreSQL (AWS RDS)      │
           │ Seeded via SQLAlchemy ORM │
           └─────────────┬─────────────┘
                         │
           ┌─────────────▼─────────────┐
           │ ETL Pipeline              │
           │ Clean + Transform + DVC   │
           └─────────────┬─────────────┘
                         │
           ┌─────────────▼─────────────┐
           │ Training Pipeline          │
           │ MLflow + Dagshub Tracking │
           │ DVC for Model Versioning  │
           └─────────────┬─────────────┘
                         │
           ┌─────────────▼─────────────┐
           │ Inference Pipeline        │
           │ FastAPI on AWS EC2        │
           └───────────────────────────┘
```

---

## 🧠 Tech Stack

| Category                | Technologies                                      |
| ----------------------- | ------------------------------------------------- |
| **Language**            | Python 3.11                                       |
| **Data Processing**     | Pandas, NumPy, Scikit-learn                       |
| **Database**            | PostgreSQL (AWS RDS), SQLAlchemy ORM              |
| **Modeling**            | Scikit-learn, Transformers, Sentence-Transformers |
| **Model Versioning**    | DVC with AWS S3 remote                            |
| **Experiment Tracking** | MLflow + Dagshub                                  |
| **Web Framework**       | FastAPI, Uvicorn                                  |
| **Cloud Services**      | AWS EC2, S3, RDS                                  |
| **Containerization**    | Docker                                            |
| **CI/CD**               | GitHub Actions                                    |
| **Others**              | boto3, awscli, python-dotenv                      |

---

## 🧮 Data & Model Management

* **Synthetic data** generated via ChatGPT:

  * 100 Nutrition entries
  * 100 Workout entries
  * 20 FAQs
* **Database:** Seeded into AWS RDS PostgreSQL using SQLAlchemy ORM
* **Models & Processed Data:** Versioned using **DVC** and stored in AWS S3
* **Experiments:** Tracked with **MLflow** integrated with **Dagshub**

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/samarthchugh/AI---Personalized-Workout-Nutrition-Coach.git
cd AI---Personalized-Workout-Nutrition-Coach
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment

Create a `.env` file in the root directory:

```
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_DEFAULT_REGION=your_region
DATABASE_URL=postgresql+psycopg2://<user>:<password>@<rds-endpoint>/<db>
```

### 5️⃣ Initialize DVC

```bash
dvc init
dvc pull    # fetches versioned data/models from S3
```

### 6️⃣ Run Locally

```bash
uvicorn src.API.main:app --host 0.0.0.0 --port 8000
```

Access interactive API docs at
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🐳 Docker Deployment

```bash
docker build -t ai-personal-coach .
docker run -p 8000:8000 ai-personal-coach
```

**Entrypoint Script (`entrypoint.sh`)**

* Seeds data into RDS
* Pulls latest model from DVC (S3)
* Starts FastAPI server

---

## 🔄 CI/CD Workflow

* Triggered on each **push/commit to main**
* GitHub Actions:

  * Builds Docker image
  * Connects via SSH to AWS EC2
  * Pulls latest code and restarts container
* Ensures **seamless production updates** with no downtime

---

## 🧾 Key Files & Modules

| File / Directory                      | Description                                    |
| ------------------------------------- | ---------------------------------------------- |
| `scripts/seed_data.py`                | Seeds CSV data into PostgreSQL RDS             |
| `src/pipelines/etl_pipeline.py`       | Extract → Transform → Load pipeline            |
| `src/pipelines/training_pipeline.py`  | Trains and tracks models                       |
| `src/pipelines/inference_pipeline.py` | Runs inference from trained models             |
| `src/chatbot/`                        | Hybrid chatbot models (retrieval + generative) |
| `dvc.yaml`                            | Pipeline stages for reproducibility            |
| `entrypoint.sh`                       | Automates EC2 container startup                |

---

## 📜 License

This project is licensed under the **MIT License**.
See the [LICENSE](./LICENSE) file for details.

---

## 👤 Author

**👨‍💻 Samarth Chugh**
MLOps & Machine Learning Engineer
📍 Hosted on **AWS EC2**
🔗 [GitHub Profile](https://github.com/samarthchugh)

---

### ⭐ If you find this project inspiring, please give it a star — it helps others discover it and supports future improvements!
