import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from dotenv import load_dotenv
import os
from datetime import date, time

# Database is on 5324
# Database API is on 8000

# All init
app = FastAPI()
load_dotenv()
dbPass = os.getenv("DB_PASS")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/init/")  # For init database
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
"taskName" varchar(255),
"taskDesc" text,
timeStart time,
timeEnd time,
timezone int,
dateStart date,
dateEnd date
)
""")
            conn.commit()
    return {"message": "Database init attempted"}


@app.get("/add/")  # For adding tasks
async def addToDb(
    user: str = None,
    taskName: str = None,
    taskDesc: str = None,
    timeStart: str = None,
    timeEnd: str = None,
    timeZone: int = 0,
    dateStart: str = None,
    dateEnd: str = None,
):
    if not user:
        print("User not found")
        raise HTTPException(status_code=400, detail="User is required")

    print(taskName, taskDesc, dateStart, dateEnd, timeStart, timeEnd)

    try:
        parsedTimeStart = time.fromisoformat(str(timeStart))
        parsedTimeEnd = time.fromisoformat(str(timeEnd))
        parsedDateStart = date.fromisoformat(str(dateStart))
        parsedDateEnd = date.fromisoformat(str(dateEnd))
    except (TypeError, ValueError) as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail="Invalid time/date format",
        )

    with psycopg.connect(f"dbname=TaskFlow user=postgres password={str(dbPass)}") as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO main ("user", "taskName", "taskDesc", timeStart, timeEnd, timezone, dateStart, dateEnd)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (user, taskName, taskDesc, parsedTimeStart, parsedTimeEnd, timeZone, parsedDateStart, parsedDateEnd),
            )
            conn.commit()

    return {"message": "Task added successfully"}


@app.get("/find/")
async def findTask(
    user: str = None,
    taskName: str = None
):
    with psycopg.connect(f"dbname=TaskFlow user=postgres password={str(dbPass)}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
        SELECT * FROM main
        WHERE "user" = '{user}' AND "taskName" = '{taskName}'
""")
            record = cur.fetchone()
            print(record)
    return {"message": f"{record}"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
