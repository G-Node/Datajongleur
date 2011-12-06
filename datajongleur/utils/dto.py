from hashlib import sha1

def checksum_json(self):
  return sha1(self.getJSON()).hexdigest()
