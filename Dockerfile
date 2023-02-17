FROM joyzoursky/python-chromedriver:3.8
RUN pip3 install cryptography
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
CMD ping mysql
CMD python3 parser.py
