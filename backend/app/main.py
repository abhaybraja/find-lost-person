from fastapi import FastAPI
from app.api.routes import face_search
from app.db.db import Base, engine
app = FastAPI(title="Face Search API")

Base.metadata.create_all(bind=engine)

app.include_router(face_search.router, prefix="/api")