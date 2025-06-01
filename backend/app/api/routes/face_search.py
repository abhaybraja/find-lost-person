from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.db.db import SessionLocal, FaceEncoding
from app.utils.image_utils import encode_face, add_to_index, search_face
import numpy as np
from sqlalchemy.orm import Session
import shutil

router = APIRouter()
@router.post("/upload/")
def upload_face(name: str, city:str, address:str, file: UploadFile = File(...)):
    session: Session = SessionLocal()
    with open(f"temp.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    encoding = encode_face("temp.jpg")
    if encoding is None:
        return {"error": "No face found"}

    face = FaceEncoding(name=name, encoding=encoding.tolist(), address=address, city=city)
    session.add(face)
    session.commit()
    add_to_index(encoding, name)

    return {"message": "Face saved"}

@router.post("/search/")
def search(file: UploadFile = File(...)):
    with open("query.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    encoding = encode_face("query.jpg")
    if encoding is None:
        return {"match": None}

    match = search_face(encoding)
    return {"match": match}

@router.post("/search-name/")
def search(name: str):
    session: Session = SessionLocal()
    records = session.query(FaceEncoding).filter(FaceEncoding.name==name).all()
    if not records:
        raise HTTPException(status_code=404, detail="No records found with this name")
    
    return {"results": [
        {
            "id": r.id,
            "name": r.name,
            "mobile": r.mobile,
            "address": r.address,
            "city": r.city,
            "state": r.state,
            "filename": r.filename
        } for r in records
    ]}