FROM python:3.11-slim

WORKDIR /app

## Install system dependencies
# - git for DVC
# - postgresql-client for database interactions
RUN apt-get update && apt-get install -y \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

## Install Python dependencies
RUN pip install --no-cache-dir torch==2.8.0 --index-url https://download.pytorch.org/whl/cpu
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip cache purge

# Copy application code
COPY scripts/ ./scripts/
COPY src/ ./src/
COPY data/raw_data/ ./data/raw_data/

# Copy DVC configuration (needed for dvc pull)
COPY .dvc/ ./.dvc/
COPY models.dvc ./
COPY data/processed.dvc ./
COPY dvc.yaml dvc.lock ./

# Copy DVC metadata files (*.dvc pointers to S3)
# COPY models/ ./models/
# COPY data/processed/ ./data/processed/

# Initialize git repo (DVC requires it)
RUN git init && \
    git config --global user.email "api@fitness-coach" &&\
    git config --global user.name "Fitness Coach API" 

# Copy and setup entrypoint
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh


EXPOSE 8000
ENTRYPOINT [ "./entrypoint.sh" ]