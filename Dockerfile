# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit when container starts
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
