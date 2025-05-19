from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import face_recognition
import numpy as np
import io
import os
from typing import List

router = APIRouter()

# Load known face encodings (could be replaced with a database later)
KNOWN_FACES_DIR = "known_faces"  # Place known images here (e.g., "john.jpg")
known_encodings = []
known_names = []

def load_known_faces():
    global known_encodings, known_names
    known_encodings = []
    known_names = []

    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR)

    for file in os.listdir(KNOWN_FACES_DIR):
        path = os.path.join(KNOWN_FACES_DIR, file)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(file)[0])
        else:
            print(f"[WARN] No face found in {file}")


@router.on_event("startup")
def startup_event():
    load_known_faces()


@router.post("/face-search")
async def face_search(file: UploadFile = File(...)):
    try:
        content = await file.read()
        image = face_recognition.load_image_file(io.BytesIO(content))
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        if not face_encodings:
            raise HTTPException(status_code=400, detail="No face detected in uploaded image.")

        matches: List[str] = []
        for encoding in face_encodings:
            results = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)
            distances = face_recognition.face_distance(known_encodings, encoding)
            if True in results:
                best_match_index = np.argmin(distances)
                matches.append(known_names[best_match_index])
            else:
                matches.append("Unknown")

        return JSONResponse({"matches": matches})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
