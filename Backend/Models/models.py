from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import INT

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True)
    email = Column(String)
    full_name = Column(String)
    allergies = Column(ARRAY(String))
    dietaryRestricitons = Column(ARRAY(String))

    # def set_password(self, password):
    #     self.password = generate_password_hash(password, method="sha256")

    # def check_password(self, password):
    #     return check_password_hash(self.password, password)

    # def __repr__(self):
    #     return f"<User id={self.id}, name={self.name}, email={self.email}>"