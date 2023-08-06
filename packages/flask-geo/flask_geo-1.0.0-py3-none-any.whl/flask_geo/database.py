import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

db = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
session = Session(db)
