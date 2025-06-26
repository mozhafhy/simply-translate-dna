from typing import TypedDict

# ! base type
class StranToStrandResult(TypedDict):
  nucleic_acid_type : str
  full_sequence: str
  sequence: str
  read_from: str
  to: str

class ToProteinResult(TypedDict):
  naming_type: str

# ! result types
class TranscribeResult(StranToStrandResult):
  """
  ### Value:
  ```
  {
    "nucleic_acid_type" : str,
    "full_sequence" : str,
    "sequence" : str,
    "read_from" : str,
    "to" : str
  }
  ```
  """
  pass

class RnaToDnaResult(StranToStrandResult):
  """
  ### Value:
  ```
  {
    "nucleic_acid_type" : str,
    "full_sequence" : str,
    "sequence" : str,
    "read_from" : str,
    "to" : str
  }
  ```
  """
  pass

class TranslateResult(ToProteinResult):
  """
  ### Value:
  ```
  {
    "naming_type" : str
    "proteins" : list[str],
    "sequence" : str,
    "has_stop_codon" : bool
  }
  ```
  """
  proteins: list[str]
  sequence: str
  has_stop_codon: bool

class CodonToProteinResult(ToProteinResult):
  """
  ### Value:
  ```
  {
    "naming_type" : str,
    "protein" : str,
    "synonymous_codons" : list[str]
  }
  ```
  """
  protein: str
  synonymous_codons: list[str]
