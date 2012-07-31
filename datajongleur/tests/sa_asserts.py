import numpy as np

def sa_access(iq):
    try:
        # load (`newByUUID` implicitly)
        iq.save()
        uuid = iq.uuid
        iq.session.expunge(iq)
        iq2 = iq.__class__.load(uuid)
    except Exception as e:
        print e
        return False
    try:
        assert np.array_equal(iq.amount, iq2.amount), ".amount not equal"
        assert iq.units == iq2.units, ".units not equal"
        assert iq.info.__repr__() == iq2.info.__repr__(), ".info not equal"
        return True
    except Exception as e:
        print "The following line pairs should be equal:"
        print "--------------------------------"
        print "iq.amount:  %r" % iq.amount
        print "iq2.amount: %r" % iq2.amount
        print "--------------------------------"
        print "iq.units:  %r" % iq.units
        print "iq2.units: %r" % iq2.units
        print "--------------------------------"
        print "iq.info:  %r" % iq.info
        print "iq2.info: %r" % iq2.info
        print "--------------------------------"
        return False
  
