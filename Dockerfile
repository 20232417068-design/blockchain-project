FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "blockchain_app.py"]
# Use official Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy all project files to container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 5003 (Flask default)
EXPOSE 5003

# Run the Flask app
CMD ["python", "blockchain_app.py"]
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "blockchain_app:app"]
