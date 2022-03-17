# Create an ubuntu image with python 3 installed.
FROM python:3.9

# Set the working directory
WORKDIR /app

# copy all the files to the working directory
COPY . /app

# Install the dependencies
RUN apt-get -y update
RUN pip install -r requirements.txt

# Expose the required port
EXPOSE 5000

# Run the command
CMD python -m gunicorn --workers 4 --timeout 600 --bind 0.0.0.0:${PORT} app:app
