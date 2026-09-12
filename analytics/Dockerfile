FROM python:3.14

COPY / /

RUN pip install uvicorn & pip install fastapi
RUN pip install psycopg 
RUN pip install dotenv
RUN pip install datetime

EXPOSE 8000

CMD python app.py