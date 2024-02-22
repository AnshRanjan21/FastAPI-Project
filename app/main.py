from fastapi import FastAPI
from . import models   # . means ki from current directory, import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)
#we no longer need this after alembic, however leaving this wont harm 

origins=["*"]

app=FastAPI()

app.add_middleware(
    CORSMiddleware,     # this is a function that runs before every request
    allow_origins=origins,     #domains to allow
    allow_credentials=True,
    allow_methods=["*"],   #allowing specific http methods
    allow_headers=["*"],
)

app.include_router(post.router) 
# we are importing the router object form posts.py ki like router = APIRouter
# when we get a http request, this line tells to include post.router, meaning, post file ke saare path operations match try honge
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")       #these lines are called path operation
async def root():
    return {"message": "Hello World "}

# @ symbol is a decorator 
#app is the api instance
#get is the HTTP method
#/ refers to the root of the path or the URL could be smth like /post/vote typish
#async means it's an ascynchronous function 
#def root is just a function can be any name

