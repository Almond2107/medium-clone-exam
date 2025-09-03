from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.dependencies import db_dep, current_user_dep
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse
from typing import List

router = APIRouter(prefix="/articles", tags=["Articles"])


# Create
@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(
    article_data: ArticleCreate,
    db: db_dep,
    current_user: current_user_dep
):
    new_article = Article(
        title=article_data.title,
        content=article_data.content,
        is_published=article_data.is_published,
        author_id=current_user.id
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


# Public list (faqat published)
@router.get("/", response_model=List[ArticleResponse])
def list_articles(db: db_dep):
    return db.query(Article).filter(Article.is_published == True).all()


# Get by ID (faqat published yoki owner)
@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: db_dep, current_user: current_user_dep = None):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if not article.is_published and (not current_user or article.author_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to view this article")

    return article


# Update (faqat owner)
@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    db: db_dep,
    current_user: current_user_dep
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    article.title = article_data.title or article.title
    article.content = article_data.content or article.content
    if article_data.is_published is not None:
        article.is_published = article_data.is_published

    db.commit()
    db.refresh(article)
    return article


# Delete (faqat owner)
@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(article_id: int, db: db_dep, current_user: current_user_dep):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(article)
    db.commit()
    return None
