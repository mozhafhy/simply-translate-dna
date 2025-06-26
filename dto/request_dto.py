from pydantic import BaseModel

# ! base DTO and content
class BaseDto(BaseModel):
  action: str
  molecule_type: str

class BaseStrandReqContent(BaseModel):
  sequence: str
  read_from: str
  to: str

class ToProteinOperation(BaseModel):
  naming_type: str

# ! content
class TranscribeReqContent(BaseStrandReqContent):
  """
  Content that will be used for transcribe method.
  
  ### Value:
  ```
  {
    "sequence" : str,
    "read_from" : str,
    "to" : str
  }
  ```
  """
  pass

class RnaToDnaReqContent(BaseStrandReqContent):
  """
  Content that will be used for RNA to DNA conversion.
  
  ### Value:
  ```
  {
    "sequence" : str,
    "read_from" : str,
    "to" : str
  }
  ```
  """
  pass

class TranslateReqContent(BaseStrandReqContent, ToProteinOperation):
  """
  Content that will be used for translate method.
  
  ### Value:
  ```
  {
    "sequence" : str,
    "read_from" : str,
    "to" : str
    "naming_type" : str
  }
  ```
  """
  pass

class CodonToProteinContent(ToProteinOperation):
  """
  Content that will be used for converting codon to amino acid.
  
  ### Value:
  ```
  {
    "naming_type" : str,
    "codon" : str
  }
  ```
  """
  codon: str

# ! DTO
class TranscribeReqDto(BaseDto):
  """
  DTO for transcribe request: convert DNA to RNA.
  
  ### Value:
  ```
  {
    "action" : str,
    "molecule_type" : str,
    "content" : TranscribeReqContent
  }
  ```
  """
  content: TranscribeReqContent

class TranslateReqDto(BaseDto):
  """
  DTO for translate request: convert RNA to amino acids sequence.
  
  ### Value:
  ```
  {
    "action" : str,
    "molecule_type" : str,
    "content" : TranslateReqContent
  }
  ```
  """
  content: TranslateReqContent

class RnaToDnaReqDto(BaseDto):
  """
  DTO for converting RNA to DNA.
  
  ### Value:
  ```
  {
    "action" : str,
    "molecule_type" : str,
    "content" : RnaToDnaReqContent
  }
  ```
  """
  content: RnaToDnaReqContent

class CodonToProteinReqDto(BaseDto):
  """
  DTO for converting codon to protein.
  
  ### Value:
  ```
  {
    "action" : str,
    "molecule_type" : str,
    "content" : CodonToProteinReqContent
  }
  ```
  """
  content: CodonToProteinContent
