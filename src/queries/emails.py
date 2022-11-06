from sqlalchemy import and_


from src import db
from src import models


def upload_email_for_user(contact_id, email=''):
    email = models.Email(contact_id=contact_id, email=email)
    db.session.add(email)
    db.session.commit()


def get_contact_emails(contact_id):
    return db.session.query(models.Email).filter(models.Email.contact_id == contact_id).all()


def delete_email(contact_id, email_id):
    db.session.query(models.Email).filter(
        and_(models.Email.contact_id == contact_id, models.Email.id == email_id)).delete()
    db.session.commit()
