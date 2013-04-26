from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
"""
Remark: hybrid_property doesn't work properly with "Date"-attributes.
        ==> safe date as String
"""

import datetime as dt
DATE_FORMAT = "%Y-%m-%d"


def date2string(date):
    return date.strftime(DATE_FORMAT)


def string2date(string):
    try:
        return dt.datetime.strptime(string, DATE_FORMAT).date()
    except BaseException, e:
        print "utils.string2date: BaseException, %s" % e
        return None


def now_as_string():
    return date2string(dt.datetime.now())


def add_caption_date_name(cls):
    @hybrid_property
    def __caption__(self):
        return self.date + "__" + self.name

    @__caption__.setter
    def __caption__(self, value):
        try:
            self.date, self.name = value.split("__")
        except BaseException, e:
            print "Couldn't set Data.__caption__, %s", e

    cls.__caption__ = __caption__
    return cls


def date_validation(cls):
    @validates('date')
    def validate_date(self, key, date):
        assert string2date(date) != None
        return date
    cls.validate_date = validate_date
    return cls


class DateNameCaption(object):
    """
    Usage:
    >>> class GeneralContainer(Base):
    >>> ...
    >>> caption = orm.composite(DateNameCaption, date, name)
    """
    @staticmethod
    def caption2attrs(caption):
        """
        "YYYY-MM-DD__NAME" --> self.date, self.name
        """
        try:
            date_string, name = caption.split("__")
            date = dt.datetime.strptime(date_string, DATE_FORMAT).date()
            return {'date': date, 'name': name}
        except Exception, e:
            print e
        return {'date': None, 'name': None}

    @classmethod
    def newByCaption(cls, caption):
        obj = cls(**cls.caption2attrs(caption))
        return obj

    def set_by_string(self, new_string):
        print "***************", self.caption2attrs(new_string)
        self.date = self.caption2attrs(new_string)['date']
        self.name = self.caption2attrs(new_string)['name']

    def __init__(self, date, name):
        self.date = date
        self.name = name

    def __composite_values__(self):
        return self.date, self.name

    def __repr__(self):
        return "DateNameCaption(caption=%r)" % (self.__str__())

    def __str__(self):
        caption = "%s__%s" %(self.date.strftime(DATE_FORMAT), self.name)
        return caption

    def __eq__(self, other):
        return isinstance(other, DateNameCaption) and \
               other.date == self.date and \
               other.name == self.name

    def __ne__(self, other):
        return not self.__eq__(other)

if __name__ == "__main__":
    pass

