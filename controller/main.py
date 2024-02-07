from fastapi import FastAPI
from controller.user import user
app=FastAPI()

@app.get('/')

def index():
    return {"Nice":"OK"}

app.include_router(user)