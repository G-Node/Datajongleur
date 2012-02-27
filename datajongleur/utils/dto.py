from hashlib import sha1

def checksum_json(self):
  return sha1(self.getJSON()).hexdigest()

class BBConverter(object):
  def __init__(self, beanbag_list=[]):
    self.map_dto2bb = {}
    for beanbag in beanbag_list:
      self.register_bb(beanbag)

  def register_bb(self, cls):
    self.map_dto2bb[cls._DTO] = cls
    return self

  def convert_bb2dto(self, beanbag):
    return beanbag._dto

  def convert_dto2bb(self, dto):
    return self.map_dto2bb[dto.__class__].newByDTO(dto)
