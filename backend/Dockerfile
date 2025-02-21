FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file first to install dependencies
COPY app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app /app/app

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Expose the application port
EXPOSE 8000

# Run the application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]