FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 python3-dev python3-venv python3-pip
    
workdir /app

COPY . .

ENV VIRTUAL_ENV=/app/venv

# Create a virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Activate the virtual environment and install dependencies
ENV PATH=$VIRTUAL_ENV/bin:$PATH

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["nohup", "python3", "nerdy_web/Aplicacao_WEB/main.py", ">", "/tmp/nerdy.log 2>&1 &"]