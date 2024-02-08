from fastapi import FastAPI, HTTPException, status ,APIRouter
from sqlalchemy import text
from config import models
from config.models import db_dependency
from config.models import UserBase
from config.models import User
from config.models import Post

post=APIRouter()

###################### View list Start ###########################

@post.get('/read_post')
def get_post(db:db_dependency):
    
    #model based
    # users = db.query(models.User.id, models.User.name).all()
    # result = [{"id": user.id, "name": user.name} for user in users]
    
    #Raw model
    raw_query = text("SELECT u.id, u.name, p.title,p.content FROM users u,posts p where u.id=p.user_id")
    posts = db.execute(raw_query)
    
    result=[]
    for post in posts:
        result.append({"title": post.title,"content": post.content,'User':post.name})

    return result
###################### View list End ###########################


###################### INSERT Start ###########################
#Raw Model specific field
@post.post('/create_post')
def create_user(db:db_dependency,title:str,content:str,user_id:int):
    new_post = Post(title=title,content=content,user_id=user_id)
    db.add(new_post)
    db.commit()
    res_data={
        'status':'200',
        'ret_str':'Post Successfully Inserted'
    }
    return res_data

###################### INSERT End ###########################
