FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose ports
EXPOSE 8000

# Run database migrations and collect static files
RUN python manage.py migrate 

# Start Daphne server
CMD daphne -b 0.0.0.0 -p 8000 project.asgi:application
