FROM python:3.11-slim
# FROM selenium/standalone-chrome:114.0
# FROM browserless/chrome:latest

# USER root
# RUN apt-get update && apt-get install -y python3 python3-pip

RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    dpkg \
    curl \
    gnupg \
    chromium-driver

# RUN wget https://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb -O /tmp/chrome.deb
# RUN dpkg -i /tmp/chrome.deb || apt-get install -f -y

# RUN wget http://security.ubuntu.com/ubuntu/pool/universe/c/chromium-browser/chromium-browser_112.0.5615.49-0ubuntu0.18.04.1_amd64.deb -O /tmp/chromium.deb
# RUN dpkg -i /tmp/chromium.deb || apt-get install -f -y

# RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip -O /tmp/driver.zip && \
#     unzip /tmp/driver.zip -d /usr/local/bin/ && \
#     chmod +x /usr/local/bin/chromedriver

COPY . /app
# COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# COPY . /app

# ENV PATH="/usr/lib/chromium-browser/:${PATH}"
# ENV CHROME_BIN="/usr/bin/chromium"
# ENV CHROME_BIN=/usr/bin/google-chrome-stable
# ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
# ENV CHROMEDRIVER_PATH=/usr/lib/chromium-browser/chromedriver

# RUN pip install gunicorn

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]