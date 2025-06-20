from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/",response_model= List[schemas.PostResponse])

@router.get("/",response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),  limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return result



# response_model=schemas.PostResponse
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    

    # # %s make sure that the value is not SQL statement
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))

    # # fetch 를 통해서 결과 값을 받을수 있음.
    # new_post = cursor.fetchone()
    # conn.commit()   
    # print(**post.model_dump())   # unpack the dictionary 
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(current_user)
    
    
    
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


# id 가 string 으로 오므로 int 로 convert 해야함 ! 
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # new_post = cursor.fetchone()
    
    # grep all the post 
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post





@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # deleting post
    # find index in the array that has required ID
    # my_posts.pop(index)
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """,(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    
    # cursor.execute("""UPDATE posts SET title = %s, content= %s, published =%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()

    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    posts = post_query.first()
    
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")
    
    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")    
    
    
    post_query.update(post.model_dump(), synchronize_session=False)
    
    db.commit()
    
    return post_query.first()