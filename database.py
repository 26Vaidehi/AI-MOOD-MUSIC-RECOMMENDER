import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Create a base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Create database instance
db = SQLAlchemy(model_class=Base)