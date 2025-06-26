from flask import Request
from dto.request_dto import (
  TranscribeReqDto,
  TranslateReqDto,
  RnaToDnaReqDto,
  CodonToProteinReqDto
)
from flaskr.response_type import SuccessResponse
from dna.dna_tools import (
  transcribe, 
  translate, 
  rna_to_dna, 
  codon_to_protein
)

# ! get json
def safely_get_json(request: Request):
  """
  Safely get json form request.
  
  ### Returns:
  ```
  json_data: any
  ```
  
  ### Raises:
    - **ValueError:**
      If the request is not JSON or has an invalid JSON format
  """
  if not request.is_json:
    raise ValueError("Request must be JSON type", status_code=415)
  
  json_data = request.get_json(silent=True)
  if json_data is None:
    raise ValueError("Invalid JSON format", status_code=400)
  
  return json_data

# ! process request
# ! transcribe
def process_transcribe_req(req_data: dict) -> SuccessResponse:
  """
  Memproses permintaan transkripsi DNA ke RNA.
  
  ### Returns:
  SuccessResponse

  ### Raises:
  - ValidationError
  - InvalidStrandReadError
  - InvalidDnaError
  """
  validated_data = TranscribeReqDto.model_validate(req_data)
  content = validated_data.content
  result = transcribe(
    dna=content.sequence,
    read_from=content.read_from,
    to=content.to
  )
  
  return {
    "data" : result,
    "status_code" : 200
  }

# ! translate
def process_translate_req(req_data: dict) -> SuccessResponse:
  """
  Memproses permintaan translasi RNA ke protein.
  
  ### Returns:
  SuccessResponse

  ### Raises:
  - ValidationError
  - InvalidStrandReadError
  - InvalidDnaError
  - NoStartCodonError
  """
  validated_data = TranslateReqDto.model_validate(req_data)
  content = validated_data.content
  result = translate(
    rna=content.sequence,
    naming_type=content.naming_type,
    read_from=content.read_from,
    to=content.to
  )
  
  return {
    "data" : result,
    "status_code" : 200
  }

# ! RNA to DNA
def process_rna_to_dna_req(req_data: dict) -> SuccessResponse:
  """
  Memproses permintaan konversi RNA ke DNA
  
  ### Returns:
  SuccessResponse

  ### Raises:
  - ValidationError
  - InvalidStrandReadError
  - InvalidRnaError
  """
  validated_data = RnaToDnaReqDto.model_validate(req_data)
  content = validated_data.content
  result = rna_to_dna(
    rna=content.sequence,
    read_from=content.read_from,
    to=content.to
  )
  
  return {
    "data" : result,
    "status_code" : 200
  }

# ! codon to protein
def process_codon_to_protein(req_data: dict) -> SuccessResponse:
  """
  Memproses permintaan konversi kodon ke asam amino
  
  ### Returns:
  SuccessResponse

  ### Raises:
  - ValidationError
  - InvalidCodonError
  """
  validated_data = CodonToProteinReqDto.model_validate(req_data)
  content = validated_data.content
  result = codon_to_protein(
    codon=content.codon,
    naming_type=content.naming_type
  )
  
  return {
    "data" : result,
    "status_code" : 200
  }
