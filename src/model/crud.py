from sqlalchemy.orm import Session, sessionmaker
from .models import User, Base
from .database import SessionLocal, engine

Base.metadata.create_all(bind=engine)
db = SessionLocal()

def create_user(chat_id:int):
    db_user = User(id=chat_id, indicators=None, interval="1h", style="candle", timezone="America/New_York", scale="regular", exchange="png", pic_format="Binance")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True

# Define the indicator updating function
def update_indicators(id:int, indicators:str):
    user = db.query(User).filter(User.id == id).update({"indicators" : indicators})
    db.commit()
    return user

# Define the interval updating function
def update_interval(id:int, interval:str):
    user = db.query(User).filter(User.id == id).update({"interval" : interval})
    db.commit()
    return user

# Define the style updating function
def update_style(id:int, style:str):
    user = db.query(User).filter(User.id == id).update({"style" : style})
    db.commit()
    return user

# Define the timezone updating function
def update_timezone(id:int, timezone:str):
    user = db.query(User).filter(User.id == id).update({"timezone" : timezone})
    db.commit()
    return user

# Define the scale updating function
def update_scale(id:int, scale:str):
    user = db.query(User).filter(User.id == id).update({"scale" : scale})
    db.commit()
    return user

# Define the exchange updating function
def update_exchange(id:int, exchange:str):
    user = db.query(User).filter(User.id == id).update({"exchange" : exchange})
    db.commit()
    return user

# Define the pic_format updating function
def update_pic_format(id:int, pic_format:str):
    user = db.query(User).filter(User.id == id).update({"pic_format" : pic_format})
    db.commit()
    return user

def get_user_by_id(id:int):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        return False
    return user

def delete_user(id:int):
    try:
        db.query(User).filter(User.id == id).delete()
        db.commit()
        return True
    except:
        return False