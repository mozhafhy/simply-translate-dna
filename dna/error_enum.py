from enum import Enum

class ErrorMessage(Enum):
  START_CODON_NOT_FOUND = "Start codon not found"
  DNA_HAS_INVALID_BASE = "DNA contains invalid base(s)"
  RNA_HAS_INVALID_BASE = "RNA contains invalid base(s)"
  INVALID_CODON_LENGTH = "Codon length must be 3"
  CODON_HAS_INVALID_BASE = "Codon contains invalid base(s)"

def invalid_edge_message(pair: tuple[int, int]) -> str:
  return f"Edge pair is invalid: {pair}"
