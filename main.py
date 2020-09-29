from fastapi import FastAPI

app = FastAPI()

# Testing fastapi
@app.get("/ping")
def pong():
    return {"ping": "pong!"}
    