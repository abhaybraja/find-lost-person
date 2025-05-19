import uuid
import os
from fastapi import UploadFile

import face_recognition
import numpy as np
import faiss

face_data = []
index = faiss.IndexFlatL2(128)

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(upload_file: UploadFile) -> str:
    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return filepath

def encode_face(image_file):
    image = face_recognition.load_image_file(image_file)
    encodings = face_recognition.face_encodings(image)
    return encodings[0] if encodings else None

def add_to_index(encoding, name):
    global face_data, index
    index.add(np.array([encoding]).astype('float32'))
    face_data.append(name)

def search_face(encoding, threshold=0.6):
    if index.ntotal == 0:
        return None
    D, I = index.search(np.array([encoding]).astype('float32'), k=1)
    if D[0][0] < threshold:
        return face_data[I[0][0]]
    return None
