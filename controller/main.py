from fastapi import FastAPI
from controller.user import user
from controller.post import post
app=FastAPI()

@app.get('/')

def index():
    return {"Nice":"OK"}

app.include_router(user)
app.include_router(post)