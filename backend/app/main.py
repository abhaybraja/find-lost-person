from fastapi import FastAPI
from app.api.routes import face_search

app = FastAPI(title="Face Search API")

app.include_router(face_search.router, prefix="/api")