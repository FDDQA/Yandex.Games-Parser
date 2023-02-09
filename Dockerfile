FROM python:3.9

RUN pip3 install cryptography chromedriver-autoinstaller
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
CMD python3 parser.py
