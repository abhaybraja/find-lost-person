FROM python:3.13-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-python-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dlib and face_recognition
RUN pip install dlib

COPY requirements.txt .
RUN pip install -r requirements.txt

# Set workdir and copy code
WORKDIR /app
COPY . /app

# Expose port
EXPOSE 8000

# Run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]