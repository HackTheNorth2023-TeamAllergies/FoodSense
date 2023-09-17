from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from Backend.Models.transactions import delete_user_account, update_user_profile, read_user_data, create_user

class Database:
    def __init__(self, conn_string):
        self.engine = create_engine(conn_string)
        self.Session = sessionmaker(bind=self.engine)

    def create_user(self, mail, name, allergy, diet):
        session = self.Session()
        try:
            user = create_user(session, mail, name, allergy, diet)
            session.commit()
            return user
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def read_user_data(self, user):
        session = self.Session()
        try:
            data = read_user_data(session, user.id)
            return data
        finally:
            session.close()

    def delete_user_account(self, user):
        session = self.Session()
        try:
            delete_user_account(session, user.id)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_user_profile(self, user, new_data):
        session = self.Session()
        try:
            update_user_profile(session, user.id, new_data)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()
