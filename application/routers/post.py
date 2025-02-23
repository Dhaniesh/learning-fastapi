from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Depends, HTTPException, status
from ..database import get_db
from typing import Any, List

from fastapi import APIRouter

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user)):
    post = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True
    ).group_by(
        models.Post.id
    ).where(models.Post.id == post_id).first()
    return post


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0):
    results = []
    posts_votes = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True
    ).group_by(
        models.Post.id
    ).offset(skip).limit(limit).all()

    for post, votes in posts_votes:
        post_dict = {
            "Post": post,
            "votes": votes
        }
        results.append(post_dict)

    return results


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")
    if post.user_id != get_current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, updated_post: schemas.PostIn, db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")
    if post.user_id != get_current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.update(updated_post.model_dump())
    db.commit()
    return post_query.first()


@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostIn, db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user)):
    print(get_current_user)
    new_post = models.Post(**post.model_dump(), user_id=get_current_user.id)  # Changed from Post to models.Post
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
