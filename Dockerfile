FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    dpkg \
    curl \
    gnupg

RUN wget http://security.ubuntu.com/ubuntu/pool/universe/c/chromium-browser/chromium-browser_112.0.5615.49-0ubuntu0.18.04.1_amd64.deb -O /tmp/chromium.deb
RUN dpkg -i /tmp/chromium.deb || apt-get install -f -y

RUN wget https://chromedriver.storage.googleapis.com/112.0.5615.49/chromedriver_linux64.zip -O /tmp/driver.zip && \
    unzip /tmp/driver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV CHROME_BIN="/usr/bin/chromium"
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

RUN pip install gunicorn

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]