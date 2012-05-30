def sa_access(iq):
  try:
    print "test"
    # load (`newByDTO` implicitly)
    iq.save()
    print "test3", iq.uuid
    uuid = iq.uuid
    iq = iq.__class__.load(uuid)
    return True
  except Exception, e:
    print e
    return False
  
