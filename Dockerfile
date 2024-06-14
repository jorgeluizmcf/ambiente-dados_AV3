# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory within the container
WORKDIR /app

# Copy the requirements.txt and app.py to the working directory
COPY requirements.txt requirements.txt
COPY app.py app.py

# Copy wait-for-it.sh script
COPY wait-for-it.sh wait-for-it.sh

# Install the application dependencies
RUN pip install -r requirements.txt

# Make wait-for-it.sh executable
RUN chmod +x wait-for-it.sh

# Expose the port that the Flask application runs on
EXPOSE 5000

# Command to run the application
CMD ["./wait-for-it.sh", "ambiente-dados-bd.jorgeluizmcf-dev.svc.cluster.local:3306", "--", "python", "app.py"]
