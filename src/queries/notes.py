from sqlalchemy import and_


from src import db
from src import models


def get_all_notes(user_id):
    notes = db.session.query(models.Note).filter(models.Note.user_id == user_id).all()
    return notes


def update_tag(tag):
    tag = models.Tag(name=tag)
    db.session.add(tag)
    db.session.commit()


def get_tag(tag):
    got_tag = db.session.query(models.Tag).filter(models.Tag.name == tag).first()
    return got_tag


def add_note(name, description, tags_obj, user_id):
    note = models.Note(name=name, description=description, tags=tags_obj, user_id=user_id)
    db.session.add(note)
    db.session.commit()


def get_all_tags():
    tags = db.session.query(models.Tag).all()
    return tags


def get_note(user_id, note_id):
    note = db.session.query(models.Note).filter(and_(models.Note.id == note_id,
                                                models.Note.user_id == user_id)).first()
    return note
