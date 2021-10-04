FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--log-level", "debug", "--host", "0.0.0.0", "--port", "80", "--root-path", "/cep_finder"]
