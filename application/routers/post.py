from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from ..database import get_db
from typing import List

from fastapi import APIRouter

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    return post


@router.get("/", response_model=schemas.PostList)
def get_posts(db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, updated_post: schemas.Post, db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found")
    post_query.update(updated_post.model_dump())
    db.commit()
    return post_query.first()


@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.Post, db: Session = Depends(get_db), get_current_user=Depends(oauth2.get_current_user)):
    print(get_current_user)
    new_post = models.Post(**post.model_dump())  # Changed from Post to models.Post
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
