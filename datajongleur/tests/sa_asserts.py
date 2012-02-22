def sa_access(iq):
  try:
    # load (`newByDTO` implicitly)
    iq.save()
    uuid = iq.uuid
    iq = iq.__class__.load(uuid)
    return True
  except Exception, e:
    print e
    return False
  
