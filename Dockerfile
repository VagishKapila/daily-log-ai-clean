FROM python:3.10.13-slim

# Set working directory
WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y build-essential libjpeg-dev zlib1g-dev

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app
COPY . .

# Run the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
