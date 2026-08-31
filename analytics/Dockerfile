FROM python:3.14

COPY / /

RUN pip install uvicorn & pip install fastapi
RUN pip install psycopg 

EXPOSE 8000

CMD python app.py