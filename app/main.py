from fastapi import FastAPI
from pydantic_settings import BaseSettings

from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# from pydantic import BaseSettings


# uvicorn app.main:app --reload  

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True     # default value is true   < optional field / default true. 
#     # rating: Optional[int] = None   # optional field / default None.




##############################################################################################################################
##                                  Post data   
##############################################################################################################################

app.include_router(post.router)

##############################################################################################################################
##                                  User Data   
##############################################################################################################################

app.include_router(user.router)

##############################################################################################################################
##                                  Auth   
##############################################################################################################################

app.include_router(auth.router)



app.include_router(vote.router)



# 두개 똑같은 route 를 가지고 있으면 first 로 match 되는것 select.
# Meaning order does impact the code. 
@app.get("/")
def root():
    return {"message": "Welcome to my API"}



    






