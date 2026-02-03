# Use Python 3.9
FROM python:3.9

# Set working directory
WORKDIR /code

# Copy requirements and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code
COPY . /code

# Create a writable cache directory for the AI model
# (Hugging Face needs this permission setup)
RUN mkdir -p /code/cache && chmod 777 /code/cache
ENV XDG_CACHE_HOME=/code/cache

# Start the server on port 7860 (Hugging Face default)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]