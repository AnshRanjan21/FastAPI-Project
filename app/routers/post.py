from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

router=APIRouter(
    prefix="/posts", # this allows us to assign a prefix because sometimes urls can get very long and tiresome to type again and again
    tags=["Posts"] #this groups together all posts wale operations
)


#@router.get("/", response_model=List[schemas.PostsResponse])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user),
              Limit: int = 10, skip:int = 0, search: Optional[str] = ""):
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    #search is optional, abhi ke liye we just implementing searching title only

    results=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                       isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    #sql join by default is outer but sqlalchemy join by default is inner join
   
    #posts=db.query(models.Post).all()
    #posts=db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() 
    #this one is to only return all posts of the logged in user   
    return results

#user_id:int = Depends(oauth2.get_current_user)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostsResponse)
def create_post(new_post:schemas.PostsCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    #Posts is the schema(pydantic model) we defined above, and Post is the model we defined in models
  
    #created_post=models.Post(title=new_post.title, content=new_post.content, published=new_post.publish)   this can get messy if we have like 50 fields 
    created_post=models.Post(owner_id=current_user.id, **new_post.model_dump())   
    print(current_user.email)
    #The double asterisks (**) in front of new_post.model_dump() is the unpacking syntax. It unpacks the dictionary returned by model_dump()
    #into keyword arguments. This means that each key-value pair in the dictionary becomes a keyword argument passed to the Post model constructor.
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post


@router.get("/{id}", response_model=schemas.PostOut)   #{id} is a path parameter
def get_post(id:int, db: Session = Depends(get_db)):    #we keep this as an int even tho it's converted back to str later to prevent user from entering smth like /posts/avsd  
    
    #post = db.query(models.Post).filter(models.Post.id == id).first() 
    #.all() will keep searching even after we pind the post with our id, first() will stop when we find the post with the id

    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                  isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        #response.status_code=404     from fastapi import status taaki status.http likhne pr you get whole list
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist :(")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    post_query= db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post does not exist")
   
    if  post.owner_id != current_user.id:     #user can only delete own post
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to ")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    #return { "message" : "The post was sucessfully deleted"}       fastapi says ki since 204 hai toh why send a msg back, isliye we implement the line below
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostsResponse)
def update_post(id:int, updated_post:schemas.PostsBase, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post does not exist")
    
    if  post.owner_id != current_user.id:    #user can only modfy their own posts
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to ")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
