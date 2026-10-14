import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from psycopg import sql
from dotenv import load_dotenv
import os
from datetime import date, time
import json
from pydantic import BaseModel

# Database is on 5324
# Front API is on 8080
# Auth API is on 8090
# This is on 8000

# All init
app = FastAPI()
load_dotenv()
dbPass = os.getenv("DB_PASS")
dbHost = os.getenv("PGHOST") or "localhost"
dbName = "TaskFlow"


def getDbConnection(): # Big handler to handle connecting, and internal schema handling, of database
    connectionOptions = {
        "user": "postgres",
        "password": str(dbPass),
        "host": dbHost,
    }
    try:
        return psycopg.connect(dbname=dbName, **connectionOptions)
    except psycopg.OperationalError as exc:
        # Some psycopg/server combinations report a missing database as an
        # OperationalError rather than the InvalidCatalogName subclass.
        if exc.sqlstate != "3D000":
            raise

    # Create the configured database if this PostgreSQL server has not initialized it.
    with psycopg.connect(
        dbname="postgres", autocommit=True, **connectionOptions
    ) as conn:
        try:
            conn.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbName))
            )
        except psycopg.errors.DuplicateDatabase:
            pass

    return psycopg.connect(dbname=dbName, **connectionOptions)

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
    with getDbConnection() as conn:
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

class task(BaseModel): # Creates the class of task to simplify and make code more readable
    user: str
    taskName: str
    taskDesc: str
    dateStart: date
    dateEnd: date
    timeStart: time
    timeEnd: time

 # For adding tasks

@app.post("/add/", status_code=201) # Call in as POST request with JSON payload
async def addToDb(payload: task):

    # CBA to recode the function below so just ignore this block
    user = payload.user
    taskName = payload.taskName
    taskDesc = payload.taskDesc
    dateStart = payload.dateStart
    dateEnd = payload.dateEnd
    timeStart = payload.timeStart
    timeEnd = payload.timeEnd
    # End of ignore

    timeZone = "0" # -- DEFAULT: 0 == UTC time. Change when actual ability is added in
    if not user:
        print("User not found")
        raise HTTPException(status_code=400, detail="User is required")

    print(taskName, taskDesc, dateStart, dateEnd, timeStart, timeEnd)

    # Create task class
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

    with getDbConnection() as conn:
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


# This can stay without OOP
@app.get("/find/") # CURRENT FORMAT FOR RETURN: USER, TASKNAME, TASK DESC, STRT TIME, END TIME, TIMEZONE, STRT DATE, END DATE
async def findTask(
    user: str = None,
    taskName: str = None
):
    with getDbConnection() as conn: # Connects to database
        with conn.cursor() as cur: # Adds database cursor
            cur.execute(f"""
        SELECT * FROM main
        WHERE "user" = '{user}' AND "taskName" = '{taskName}'
""") # Executes query
            record = cur.fetchone() # Fetches one record matching SQL query
            arrRecord = []
            for i in record: # Essentially converts tuple to array
                arrRecord.append(i)
            # Converting from time python objects to iso format 
            arrRecord[3] =  time.isoformat(arrRecord[3])
            arrRecord[4] = time.isoformat(arrRecord[4])
            # Converting from date python objects to iso format
            arrRecord[6] = date.isoformat(arrRecord[6])
            arrRecord[7] = date.isoformat(arrRecord[7])
            print(arrRecord[3])
            print(arrRecord)
    return {"record": f"{arrRecord}"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)