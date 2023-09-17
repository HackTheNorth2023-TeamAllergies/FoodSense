from cockroachdb.sqlalchemy import run_transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from transactions import delete_user_account, update_user_profile,read_user_data,create_user


class UserActions:
    def __init__(self, conn_string):
        self.engine = create_engine(conn_string, convert_unicode=True)
        self.sessionmaker = sessionmaker(bind=self.engine)
    
    def create_user(self,mail, name, allergy, diet):
        return run_transaction(self.sessionmaker,lambda session: self.create_user(session,mail, name, allergy, diet))
    
    def read_user_data(self,user):
        return run_transaction(self.sessionmaker,lambda session: self.read_user_data(session,user.id))
    
    def delete_user_account(self,user):
        return run_transaction(self.sessionmaker,lambda session: self.prepare_scores(session,user.id))
    
    def update_user_profile(self,user,new_data):
        return run_transaction(self.sessionmaker,lambda session: self.prepare_scores(session,user.id,new_data))




