# -*- coding: utf-8 -*-
__author__ = 'philipp'
from datajongleur.tests import *

from datajongleur.beanbags.models import *
from datajongleur.addendum import *
from datajongleur.tests import *

def test_Addendum():
    a = Addendum(name="Max Mustermann", description="I am programmer", flag=True)
    b = Addendum(name=u"Hans Müller", description="Father of Max", flag=False)
    session.add(a)
    session.commit()
    a.references_to.append(b)
    return a

def test_access_from_Identity():
    tp = TimePoint(numbers[0], units[0])
    tp2 = TimePoint(numbers[1], units[1])
    assert tp.description == None
    tp.name = "Max Mustermann"
    assert tp.description == ""
    return tp

def test_ATreeNode():
    pass

if __name__ == "__main__":
    a = test_Addendum()
    tp = test_access_from_Identity()