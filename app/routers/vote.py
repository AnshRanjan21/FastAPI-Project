from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["VOTE"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session = Depends(database.get_db), current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:   #checking if post exists
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail= f"Post does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
        #checking if the current user has already voted for this post. cannot allow multiple votes
    found_vote = vote_query.first()

    if (vote.dir == 1):  #casting a new vote
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail= f"User {current_user.id} has already voted on the post {vote.post_id}")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message" : "sucessfully added vote"}
    
    else:  # dir = 0 matlab user wants to remove vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail= f"User {current_user.id} has not voted on the post {vote.post_id}")

        vote_query.delete(synchronize_session = False)
        db.commit()

        return{"message" : "sucessfully deleted vote"}