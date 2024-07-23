FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-warn-script-location --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "main.py"]
CMD ["-a", "2"]