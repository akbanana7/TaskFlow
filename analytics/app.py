import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/add/")
async def addToDb():
    print("WAZAAAAAA")
    return "WAZAAAA"

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
