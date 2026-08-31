import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg
from dotenv import load_dotenv
import os
from datetime import date, time, datetime

# Database is on 5324

# All init
app = FastAPI()
load_dotenv()
dbPass = os.getenv("DB_PASS")


@app.get("/init/") # For init database
async def initDb(passWord: str = None):
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

@app.get("/add/") # For adding tasks
async def addToDb(user: str = None, timeStart: str = None, timeEnd: str = None, timeZone: int = 0, dateStart: str = None, dateEnd: str = None):
    with psycopg.connect(f"dbname=TaskFlow user=postgres password={str(dbPass)}") as conn:
        with conn.cursor() as cur:
            if user:
                # Parse into objects to be sent to DB
                try:
                    timeStart = time.fromisoformat(timeStart)
                    timeEnd = time.fromisoformat(timeStart)
                    dateStart = date.fromisoformat(timeStart)
                    dateEnd = date.fromisoformat(timeStart)

                except:
                    raise ValueError("Couldn't convert times")
                cur.execute(f"""
    INSERT INTO (user, timeStart, timeEnd, timezone, dateStart, dateEnd)
    VALUES ({user}, {timeStart}, {timeEnd}, {timeZone}, {dateStart}, {dateEnd})
""")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
