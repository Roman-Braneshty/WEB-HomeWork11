from sqlalchemy import and_


from src import db
from src import models


def upload_phone_for_user(contact_id, phone=''):
    phone = models.Phone(contact_id=contact_id, phone=phone)
    db.session.add(phone)
    db.session.commit()


def get_contact_phone(contact_id):
    return db.session.query(models.Phone).filter(models.Phone.contact_id == contact_id).all()


def delete_phone(contact_id, phone_id):
    db.session.query(models.Phone).filter(
        and_(models.Phone.contact_id == contact_id, models.Phone.id == phone_id)).delete()
    db.session.commit()


if __name__ == '__main__':
    contact_id = 2
    phone = '38061'
    print(upload_phone_for_user(contact_id, phone))
