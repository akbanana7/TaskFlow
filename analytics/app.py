import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg
from dotenv import load_dotenv
import os

# Database is on 5324

# All init
app = FastAPI()
load_dotenv()
dbPass = os.getenv("DB_PASS")


@app.get("/init/")
async def initDb():
    with psycopg.connect(f"dbname=TaskFlow user=postgres password={str(dbPass)}") as conn:
        with conn.cursor() as cur:
            cur.execute("""
DROP TABLE IF EXISTS main

""")
            conn.commit()
            cur.execute("""
CREATE TABLE main (
"user" varchar(255),
timeStart time,
timeEnd time,
timezone int,
dateStart date,
dateEnd date
)
""")

            conn.commit()      
    return("Database init attempted")

@app.get("/add/")
async def addToDb():
    print("WAZAAAAAA")
    return "WAZAAAA"

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
