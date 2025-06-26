class MoleculeStructureError(Exception):
  """Base exception for molecule (DNA, RNA, codon) structure error"""
  def __init__(self, message: str, status_code: int):
    super().__init__(message)
    self.status_code = status_code

class InvalidDnaError(MoleculeStructureError):
  """Raised when DNA contains invalid character"""
  pass

class InvalidRnaError(MoleculeStructureError):
  """Raised when RNA contains invalid character"""
  pass

class InvalidCodonError(MoleculeStructureError):
  """Raised when codon length is not 3 or contains invalid character"""
  pass

class InvalidStrandReadError(MoleculeStructureError):
  """Raised when DNA or RNA has invalid read direction
  (not on of these pairs: (3,5), (5,3))"""
  pass

class NoStartCodonError(MoleculeStructureError):
  """Raised when RNA has no start codon"""
  pass
