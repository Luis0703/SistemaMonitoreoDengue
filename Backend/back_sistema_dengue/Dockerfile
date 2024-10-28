FROM python:3.11

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./ /app
EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
