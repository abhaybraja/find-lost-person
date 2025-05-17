from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import models
from app.schemas.person import PersonCreate, PersonOut
from app.services.face_recognition import get_face_encoding, compare_faces
from app.utils.image_utils import save_upload_file
import numpy as np

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add-profile", response_model=PersonOut)
def add_profile(person: PersonCreate, file: UploadFile, db: Session = Depends(get_db)):
    image_path = save_upload_file(file)
    encoding = get_face_encoding(image_path)
    if encoding is None:
        raise HTTPException(status_code=400, detail="No face found")
    db_person = models.Person(
        name=person.name,
        age=person.age,
        location=person.location,
        last_seen=person.last_seen,
        image_url=image_path,
        face_encoding=encoding.tobytes()
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@router.post("/search-face")
def search_face(file: UploadFile, db: Session = Depends(get_db)):
    image_path = save_upload_file(file)
    new_encoding = get_face_encoding(image_path)
    if new_encoding is None:
        raise HTTPException(status_code=400, detail="No face found")

    persons = db.query(models.Person).all()
    known_encodings = [p.face_encoding for p in persons]
    matches = compare_faces(known_encodings, new_encoding.tobytes())

    results = [{"id": persons[i]["id"], "name": persons[i]["name"], "score": score}
               for i, score in matches]
    return {"matches": results}