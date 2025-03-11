# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 8081

# Start the Gunicorn server
CMD ["gunicorn", "-b", "0.0.0.0:8081", "app:app"]
