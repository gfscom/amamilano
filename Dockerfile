FROM python:3.13-slim

# Copy the script and requirements
WORKDIR /app
COPY amamilano.py requirements.txt verbs.txt ./

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Start the script
CMD ["python", "amamilano.py"]
