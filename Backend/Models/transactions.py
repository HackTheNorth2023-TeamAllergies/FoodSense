from Backend.Models.models import User
import uuid
import os

def create_user(session, mail, name, allergy, diet):
    user = User(
        id=str(
            uuid.uuid4()),
        email=mail,
        full_name=name,
        allergies=allergy,
        dietaryRestrictions=diet,
    )
    session.add(user)


def read_user_data(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        return {
            'email': user.email,
            'full_name': user.full_name,
            'allergies': user.allergies,
            'dietary_restrictions': user.dietaryRestrictions
        }
    else:
        return None


def delete_user_account(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return True
    else:
        return False

def update_user_profile(session, user_id, new_data):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        for key, value in new_data.items():
            setattr(user, key, value)
        session.commit()
        return True
    else:
        return False

