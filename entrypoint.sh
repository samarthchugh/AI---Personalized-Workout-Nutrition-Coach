#!/bin/bash
set -e

echo "🚀 Starting AI Fitness Coach API..."

# ============================================
# 1. Wait for PostgreSQL
# ============================================
echo "⏳ Waiting for PostgreSQL..."
DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')

if [ -z "$DB_HOST" ]; then
    DB_HOST="postgres"
    DB_PORT="5432"
fi

while ! pg_isready -h $DB_HOST -p $DB_PORT > /dev/null 2>&1; do
  echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
  sleep 2
done
echo "✅ PostgreSQL ready!"

# ============================================
# 2. Pull Models from S3 (DVC)
# ============================================
echo "📦 Pulling models from S3..."
if dvc pull models/ 2>/dev/null; then
    echo "✅ Models downloaded"
    ls -lh models/*/
else
    echo "⚠️  DVC pull failed, checking local models..."
    if [ -d "models" ] && [ "$(ls -A models/)" ]; then
        echo "✅ Using local models"
    else
        echo "❌ No models found!"
        exit 1
    fi
fi

# ============================================
# 3. Pull Processed Data (Optional)
# ============================================
echo "📦 Pulling processed data..."
dvc pull data/processed/ 2>/dev/null || echo "⚠️  Using local data"

# ============================================
# 4. Seed Database
# ============================================
echo "🌱 Seeding database with raw CSV data..."
python -m scripts.seed_data || echo "⚠️  Database already seeded or seeding failed"

# ============================================
# 5. Start API
# ============================================
echo "🎯 Starting FastAPI server..."
exec uvicorn src.API.main:app --host 0.0.0.0 --port 8000