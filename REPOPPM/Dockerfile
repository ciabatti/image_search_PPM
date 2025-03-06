# Use a base Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . /app/

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1

# Expose the port that Gunicorn will use
EXPOSE 8000

# Command to start Gunicorn
CMD ["gunicorn", "image_search.wsgi:application", "--bind", "0.0.0.0:8000"]
