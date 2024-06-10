# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory within the container
WORKDIR /app

# Copy the requirements.txt and app.py to the working directory
COPY requirements.txt requirements.txt
COPY app.py app.py

# Install the application dependencies
RUN pip install -r requirements.txt

# Expose the port that the Flask application runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]

#comando para executar
#sudo docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=12345678 -e MYSQL_DATABASE=steam -e MYSQL_USER=root -e MYSQL_PASSWORD=12345678
