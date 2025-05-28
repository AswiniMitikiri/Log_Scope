# Use official Python image
FROM python:3.10

# Set work directory
WORKDIR /app

# Copy backend code
COPY ./backend /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
