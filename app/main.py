from fastapi import Depends, FastAPI

app = FastAPI(title="Example template")

@app.get("/health")
def health():
    return{"status": "ok"}

@app.get("/hello")
def hello():
    return{"status": "hello FROM FASTAPI"}
