from sqlalchemy import and_


from src import db
from src import models


def get_contact(user_id, contact_id):
    contact = db.session.query(models.Contact).filter(and_(models.Contact.id == contact_id,
                                                           models.Contact.user_id == user_id
                                                           )).one()
    return contact


def get_all_contacts(user_id):
    contact = db.session.query(models.Contact).filter(models.Contact.user_id == user_id).all()
    return contact


def get_contact_id(user_id, first_name='', last_name='', birthday=''):
    if first_name != '':
        contact_id_ = db.session.query(models.Contact).filter(and_(models.Contact.user_id == user_id,
                                                                  models.Contact.first_name == first_name)).one()
    elif last_name != '':
        contact_id_ = db.session.query(models.Contact).filter(and_(models.Contact.user_id == user_id,
                                                                  models.Contact.last_name == last_name)).one()
    elif birthday != '':
        contact_id_ = db.session.query(models.Contact).filter(and_(models.Contact.user_id == user_id,
                                                                  models.Contact.birthday == birthday)).one()
    return contact_id_.id


def upload_contact_for_user(user_id, first_name='', last_name='', birthday=''):
    contact = models.Contact(user_id=user_id, first_name=first_name, last_name=last_name, birthday=birthday)
    db.session.add(contact)
    db.session.commit()


def update_first_name(user_id, contact_id, first_name=''):
    user_contact = get_contact(user_id, contact_id)
    user_contact.first_name = first_name
    db.session.commit()


def update_last_name(user_id, contact_id, last_name=''):
    user_contact = get_contact(user_id, contact_id)
    user_contact.last_name = last_name
    db.session.commit()


def update_birthday(user_id, contact_id, birthday=''):
    user_contact = get_contact(user_id, contact_id)
    user_contact.birthday = birthday
    db.session.commit()


def delete_contact(user_id, contact_id):
    db.session.query(models.Contact).filter(
        and_(models.Contact.user_id == user_id, models.Contact.id == contact_id)).delete()
    db.session.commit()
