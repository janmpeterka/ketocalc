from flask import current_app as application

from sqlalchemy.exc import DatabaseError

from app import db


# Custom methods for all my classes
class BaseMixin(object):
    @classmethod
    def __init__(cls, **kwargs):
        obj = cls()
        for kwarg in kwargs:
            setattr(obj, kwarg.key, kwarg.value)

        return obj

    @classmethod
    def load(cls, *args, **kwargs):
        object_id = kwargs.get("id", args[0])
        return db.session.query(cls).filter(cls.id == object_id).first()

    @classmethod
    def load_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def load_last(cls):
        return db.session.query(cls).all()[-1]

    @classmethod
    def load_by_name(cls, name):
        return db.session.query(cls).filter(cls.name == name).first()

    @classmethod
    def load_by_attribute(cls, attribute, value):
        if not hasattr(cls, attribute):
            raise AttributeError

        return db.session.query(cls).filter(getattr(cls, attribute) == value).first()

    def edit(self, **kw):
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error("Edit error: {}".format(e))
            return False

    def save(self, **kw):
        """Saves (new) object
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self.id is not None
        except DatabaseError as e:
            db.session.rollback()
            application.logger.error("Save error: {}".format(e))
            return False

    def remove(self, **kw):
        """Deletes object
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except DatabaseError as e:
            db.session.rollback()
            application.logger.error("Remove error: {}".format(e))
            return False

    def expire(self, **kw):
        """Dumps database changes
        """
        try:
            db.session.expire(self)
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error("Expire error: {}".format(e))
            return False

    def refresh(self, **kw):
        try:
            db.session.refresh(self)
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error("Refresh error: {}".format(e))
            return False
