FROM python:3.11-slim

RUN echo "deb http://deb.debian.org/debian bullseye main contrib" > /etc/apt/sources.list \
    && echo "deb https://deb.debian.org/debian-security bullseye-security main contrib" >> /etc/apt/sources.list \
    && echo "deb [signed-by=/usr/share/keyrings/lil-archive-keyring.gpg] https://repo.lil.tools/ bullseye-security updates/main" > /etc/apt/sources.list.d/lil-chromium.list

RUN apt-get update && apt-get install -y \
    chromium=114.0.5735.197 \
    chromium-driver \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PATH="/usr/lib/chromium-browser/:${PATH}"
ENV CHROME_BIN="/usr/bin/chromium"

RUN pip install gunicorn

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]