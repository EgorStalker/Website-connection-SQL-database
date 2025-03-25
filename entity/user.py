from Hamaxi_Flask.app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import  Mapped,mapped_column

from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name_people: Mapped[str] = mapped_column(db.String(128), nullable=False)
    email: Mapped[str] = mapped_column(db.String(128), nullable=False)
    date: Mapped[str] = mapped_column(db.String(128), nullable=False)
    password: Mapped[str] = mapped_column(db.String(128), nullable=False)

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)