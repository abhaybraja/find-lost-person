import face_recognition
import numpy as np
from typing import List

def get_face_encoding(image_path: str):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    return encodings[0] if encodings else None

def compare_faces(known_encodings: List[bytes], new_encoding: bytes, threshold=0.6):
    known_encodings = [np.frombuffer(e, dtype=np.float64) for e in known_encodings]
    new_encoding = np.frombuffer(new_encoding, dtype=np.float64)
    distances = face_recognition.face_distance(known_encodings, new_encoding)
    return [(i, 1 - dist) for i, dist in enumerate(distances) if dist < threshold]