from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
import json
from datetime import datetime

from app.utils.dependencies import get_db
from app.models.article import Article

router = APIRouter(prefix="/digest", tags=["digest"])


def generate_weekly_digest(db: Session):
    articles = db.query(Article).filter(Article.is_published == True).all()
    data = [
        {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "author": article.author.username if article.author else None,
            "created_at": article.created_at.isoformat()
        }
        for article in articles
    ]

    filename = f"weekly_digest_{datetime.now().strftime('%Y_%m_%d')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f" Weekly digest generated: {filename}")


@router.post("/weekly")
def create_weekly_digest(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(generate_weekly_digest, db)
    return {"message": "Weekly digest generation started in background"}
