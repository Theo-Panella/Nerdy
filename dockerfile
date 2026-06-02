FROM python:3.11.15-trixie

workdir /app

COPY . .

ENV VIRTUAL_ENV=/app/venv

# Create a virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Activate the virtual environment and install dependencies
ENV PATH=$VIRTUAL_ENV/bin:$PATH

RUN pip install -r requirements.txt

EXPOSE 5000