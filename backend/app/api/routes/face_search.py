from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from app.db.db import SessionLocal, FaceEncoding
from app.utils.image_utils import encode_face, add_to_index, search_face
import numpy as np
from sqlalchemy.orm import Session
import shutil

from app.db.deps import get_db

router = APIRouter(tags=['upload','search'])
@router.post("/upload/")
def upload_face(name: str, city:str, address:str, file: UploadFile = File(...), db: Session=Depends(get_db)):
    
    with open(f"temp.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    encoding = encode_face("temp.jpg")
    if encoding is None:
        return {"error": "No face found"}

    face = FaceEncoding(name=name, encoding=encoding.tolist(), address=address, city=city)
    db.add(face)
    db.commit()
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

@router.get("/search-name/")
def get_records_by_name(name: str= Query(...), db: Session=Depends(get_db)):
    records = db.query(FaceEncoding).filter(FaceEncoding.name==name).all()
    if not records:
        raise HTTPException(status_code=404, detail="No records found with this name")
    
    return JSONResponse({"results": [
        {
            "id": r.id,
            "name": r.name,
            "address": r.address,
            "city": r.city,
            "state": r.state
        } for r in records
    ]})
