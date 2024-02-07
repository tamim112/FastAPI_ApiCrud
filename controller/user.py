from fastapi import FastAPI, HTTPException, status ,APIRouter
from sqlalchemy import text
from config import models
from config.models import db_dependency
from config.models import UserBase
from config.models import User

user=APIRouter()

###################### View list Start ###########################

@user.get('/read')
def get_user(db:db_dependency):
    
    #model based
    # users = db.query(models.User.id, models.User.name).all()
    # result = [{"id": user.id, "name": user.name} for user in users]
    
    #Raw model
    raw_query = text("SELECT id, name FROM users")
    users = db.execute(raw_query)
    
    result=[]
    for user in users:
        result.append({"id": user.id,"name": user.name})

    return result
###################### View list End ###########################


###################### INSERT Start ###########################
#Raw Model specific field
@user.post('/create_user')
def create_user(db:db_dependency,name:str,email:str,mobile:str):
    user_name=name
    user_email=email
    user_mobile=mobile
    new_user = User(name=user_name,email=user_email,mobile=user_mobile)
    db.add(new_user)
    db.commit()
    res_data={
        'status':'200',
        'ret_str':'Successfully Inserted'
    }
    return res_data

#Model based
@user.post('/create_user_alt')
def create_user(db:db_dependency,user:UserBase):
    user_date=user.dict()
    new_user = User(**user_date)
    db.add(new_user)
    db.commit()
    res_data={
        'status':'200',
        'ret_str':'Successfully Inserted'
    }
    return res_data
###################### INSERT End ###########################

###################### Update Start ###########################
#Model based
@user.put('/update_user')
def update_user(db:db_dependency,id:int,user: UserBase):
    
    existing_user = db.query(User).filter(User.id == id).first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.query(User).filter(User.id == id).update(user.dict(), synchronize_session=False)

    db.commit()
    res_data={
        'status':'200',
        'ret_str':'Successfully Updated'
    }
    return res_data

#Raw Specific Field
@user.put('/update_user_alt')
def update_user_field(db:db_dependency, id:int, name: str, email: str):
    existing_user = db.query(User).filter(User.id == id).first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # update_query = text(f"UPDATE users SET name = :name,email = :email WHERE id = :id")
    
    update_query = text(f"UPDATE users SET name = '{name}',email = '{email}' WHERE id = '{id}'")

    db.execute(update_query, {"name": name,"email": email,  "id": id})

    db.commit()

    res_data = {
        'status': '200',
        'ret_str': f'Successfully Updated {name}'
    }
    
    return res_data
###################### Update End ###########################


###################### Delete Start ###########################

@user.delete('/delete_user')
def delete_user(db:db_dependency,id:int):
    existing_user = db.query(User).filter(User.id == id).first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    #Raw model
    # raw_query = text(f"DELETE FROM users where id=:id")
    # users = db.execute(raw_query,{'id':id})
    
    #model based
    db.delete(existing_user)
    
    db.commit()

    res_data = {
        'status': '200',
        'ret_str': f'Successfully Deleted'
    }
    
    return res_data
###################### Delete Start ###########################