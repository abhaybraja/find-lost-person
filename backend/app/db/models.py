from sqlalchemy import Column, Integer, String, LargeBinary
from app.db.session import Base

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    location = Column(String)
    last_seen = Column(String)
    image_url = Column(String)
    face_encoding = Column(LargeBinary)