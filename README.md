# Lost Person Finder 🧠📸

A web-based tool to help locate lost individuals using facial recognition. Users can upload a face photo, and the system will search for matches in a database of known profiles.

## 🔧 Tech Stack

- **Frontend:** React + TypeScript
- **Backend:** FastAPI (Python)
- **Facial Recognition:** face_recognition library

## 🚀 Features

- Upload a face photo to search for missing persons
- View potential matches with confidence scores
- Add new profiles with face data and metadata

## 📦 Installation

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
