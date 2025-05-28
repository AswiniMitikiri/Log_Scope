# Use official Python image
FROM python:3.10

# Set work directory
WORKDIR /app

# Copy frontend code
COPY ./frontend /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Start Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]