from dna.result_types import (
  TranscribeResult,
  TranslateResult,
  RnaToDnaResult,
  CodonToProteinResult
)
from dna.error_enum import (
  ErrorMessage,
  invalid_edge_message
)
from dna.error_types import (
  InvalidDnaError,
  InvalidRnaError,
  NoStartCodonError,
  InvalidStrandReadError,
  InvalidCodonError
)

# constant terms declaration
_BASE_PAIRS = {
  "A" : "U",
  "T" : "A",
  "G" : "C",
  "C" : "G"
}

_PROTEIN_CODON = {
  ("V", "Val", "Valine"): {"GUU", "GUC", "GUA", "GUG"},
  ("A", "Ala", "Alanine"): {"GCU", "GCC", "GCA", "GCG"},
  ("D", "Asp", "Aspartic Acid"): {"GAU", "GAC"},
  ("E", "Glu", "Glutamic Acid"): {"GAA", "GAG"},
  ("G", "Gly", "Glycine"): {"GGU", "GGC", "GGA", "GGG"},
  ("F", "Phe", "Phenylalanine"): {"UUU", "UUC"},
  ("S", "Ser", "Serine"): {"UCU", "UCC", "UCA", "UCG", "AGU", "AGC"},
  ("Y", "Tyr", "Tyrosine"): {"UAU", "UAC"},
  ("C", "Cys", "Cysteine"): {"UGU", "UGC"},
  ("W", "Trp", "Tryptophan"): {"UGG"},
  ("L", "Leu", "Leucine"): {"CUU", "CUC", "CUA", "CUG", "UUA", "UUG"},
  ("P", "Pro", "Proline"): {"CCU", "CCC", "CCA", "CCG"},
  ("H", "His", "Histidine"): {"CAU", "CAC"},
  ("Q", "Gln", "Glutamine"): {"CAA", "CAG"},
  ("R", "Arg", "Arginine"): {"CGU", "CGC", "CGA", "CGG", "AGA", "AGG"},
  ("I", "Ile", "Isoleucine"): {"AUU", "AUC", "AUA"},
  ("T", "Thr", "Threonine"): {"ACU", "ACC", "ACA", "ACG"},
  ("N", "Asn", "Asparagine"): {"AAU", "AAC"},
  ("K", "Lys", "Lysine"): {"AAA", "AAG"},
  ("M", "Met", "Methionine"): {"AUG"},
  ("Stop", "Stop", "Stop"): {"UAA", "UAG", "UGA"}
}
_BASE_PAIRS_REV_MAP = { val: key for key, val in _BASE_PAIRS.items() }
_PROTEIN_CODON_REV_MAP = { val: key for key, values in _PROTEIN_CODON.items() for val in values }
_START_CODON = next(iter(_PROTEIN_CODON["M", "Met", "Methionine"]))
_STOP_CODONS = _PROTEIN_CODON["Stop", "Stop", "Stop"]
_VALID_EDGES = {("3", "5"), ("5", "3")}
_VALID_DNA_BASES = {"A", "T", "G", "C"}
_VALID_RNA_BASES = {"A", "G", "C", "U"}

# functions declaration
# ! transcribe
def transcribe(
  dna: str,
  read_from: str = "3",
  to: str = "5"
  ) -> TranscribeResult:
  """
  Mentranskripsikan sebuah DNA menjadi RNA, dibaca dari ujung <code>read_from</code> ke ujung <code>to</code> menghasilkan RNA dengan ujung <code>to</code> di kiri dan 
  <code>read_from di kanan</code>.
  
  ### Returns:
  TranscribeResult
  
  ### Raises:
    - **InvalidStrandReadError:**
      Jika DNA dibaca dengan arah yang tidak valid. Arah yang diizinkan adalah (3,5) atau (5,3)
    
    - **InvalidDnaResult:**
      Jika DNA mengandung basa nitrogen yang tidak valid. Basa nitrogen yang valid adalah `A`, `T`, `G`, dan `C`
  """
  dna = dna.upper()
  if (read_from, to) not in _VALID_EDGES:
    raise InvalidStrandReadError(
      message=invalid_edge_message((read_from, to)),
      status_code=400
    )
  
  if not all(base in _VALID_DNA_BASES for base in dna):
    invalid_bases = ", ".join([base for base in dna if base not in _VALID_DNA_BASES])
    message = f"{ErrorMessage.DNA_HAS_INVALID_BASE.value}: {invalid_bases}"
    raise InvalidDnaError(
      message=message,
      status_code=400
    )
  
  read_from, to = to, read_from
  seq = "".join(_BASE_PAIRS.get(base.upper(), "?") for base in dna)
  return {
    "nucleic_acid_type" : "RNA",
    "full_sequence" : f"{read_from}\'-{seq}-{to}\'",
    "sequence" : seq,
    "read_from" : read_from,
    "to" : to,
  }

# ! translate
def translate(
  rna: str,
  read_from: str = "5",
  to: str = "3",
  naming_type: str = "3 letters"
  ) -> TranslateResult:
  """
  Mentranslasikan sebuah RNA menjadi urutan asam amino, dibaca dari ujung 5\' ke ujung 3\'. 
  
  ### Return:
  TranslateResult
  
  ### Raises:
    - **InvalidStrandReadError:**
      Jika RNA dibaca dengan arah yang tidak valid. Arah yang diizinkan adalah (3,5) atau (5,3)
    - **InvalidRnaError:**
      Jika RNA mengandung basa nitrogen yang tidak valid. Basa nitrogen yang valid adalah `A`, `U`, `G`, dan `C`
    - **NoStartCodonError:**
      Jika RNA tidak memiliki start codon (AUG) setelah diformat sehingga dibaca dari ujung 5' ke 3'
  """
  
  rna = rna.upper()
  if (read_from, to) not in _VALID_EDGES:
    raise InvalidStrandReadError(
      message=invalid_edge_message((read_from, to)),
      status_code=400
    )
    
  if not all(base in _VALID_RNA_BASES for base in rna):
    invalid_bases = ", ".join([base for base in rna if base not in _VALID_RNA_BASES])
    message = f"{ErrorMessage.RNA_HAS_INVALID_BASE.value}: {invalid_bases}"
    raise InvalidRnaError(
      message=message,
      status_code=400
    )
  
  name_index, delim = 1, "-"
  match naming_type:
    case "short":
      name_index, delim = 0, ""
    case "3 letters":
      name_index, delim = 1, "-"
    case "long":
      name_index, delim = 2, "---"
    case _:
      naming_type = "3 letters"
  
  # balik urutan RNA-nya jika ia dibaca dari ujung 3' ke ujung 5'
  rna = rna[::-1] if (read_from, to) == ("3", "5") else rna
  
  if _START_CODON not in rna:
    raise NoStartCodonError(
      message=ErrorMessage.START_CODON_NOT_FOUND.value,
      status_code=400
    )
  
  start = rna.index(_START_CODON) # find the first occurance of start codon
  rna = rna[start:] # cut at start codon
  rna = rna[:(len(rna) - len(rna) % 3)] # make it divisible by 3
  triplets = [rna[i:i+3] for i in range(0, len(rna), 3)]
  
  stop_indices = [index for index, stop in enumerate(triplets)
                  if stop in _STOP_CODONS] # find all stop codon indices
  end = min(stop_indices) + 1 if stop_indices else len(triplets)
  # get the first stop codon
  
  triplets = triplets[:end] 
  # take only codons between the start and stop codon
  # else if no stop codons, get all codons
  
  proteins = [_PROTEIN_CODON_REV_MAP.get(codon, "?")[name_index] for codon in triplets]
  # convert codon into its amino acid, then list them
  has_stop_codon = "Stop" in proteins
  sequence = delim.join(proteins)
  return {
    "naming_type" : naming_type,
    "proteins" : proteins,
    "sequence" : sequence if has_stop_codon else (sequence + delim),
    "has_stop_codon" : has_stop_codon,
  }

# ! transcribe RNA to DNA
def rna_to_dna(
  rna: str,
  read_from: str = "5",
  to: str = "3"
  ) -> RnaToDnaResult:
  """
  Mengubah RNA ke DNA.
  
  ### Returns:
  RnaToDnaResult
  
  ### Raises:
    - **InvalidStrandReadError:**
      Jika RNA dibaca dengan arah yang tidak valid. Arah yang diizinkan adalah (3,5) atau (5,3)
    - **InvalidRnaError:**
      Jika RNA mengandung basa nitrogen yang tidak valid. Basa nitrogen yang valid adalah `A`, `U`, `G`, dan `C`
  """
  
  rna = rna.upper()
  if (read_from, to) not in _VALID_EDGES:
    raise InvalidStrandReadError(
      message=invalid_edge_message((read_from, to)),
      status_code=400
    )
  
  if not all(base in _VALID_RNA_BASES for base in rna):
    invalid_bases = ", ".join([base for base in rna if base not in _VALID_RNA_BASES])
    message = f"{ErrorMessage.RNA_HAS_INVALID_BASE.value}: {invalid_bases}"
    raise InvalidRnaError(
      message=message,
      status_code=400
    )
  
  read_from, to = to, read_from
  seq = "".join(_BASE_PAIRS_REV_MAP[base] for base in rna)
  return {
    "nucleic_acid_type" : "DNA",
    "full_sequence" : f"{read_from}\'-{seq}-{to}\'",
    "sequence" : seq,
    "read_from" : read_from,
    "to" : to
  }

# ! codon to protein
def codon_to_protein(
  codon: str,
  naming_type: str = "3 letters"
  ) -> CodonToProteinResult:
  """
  Mengonversi kodon menjadi asam aminonya.
  
  ### Returns:
  CodonToProteinResult
  
  ### Raises:
    - **InvalidCodonError:**
      Jika ```codon``` memiliki panjang atau basa nitrogen yang tidak valid. Panjang kodon yang tepat adalah 3 dan basa nitrogen yang diperbolehkan adalah `A`, `U`, `G`, dan `C`
  </code>
  """
  
  codon = codon.upper()
  if len(codon) != 3:
    raise InvalidCodonError(
      message=ErrorMessage.INVALID_CODON_LENGTH.value,
      status_code=400
    )
  
  if not all(base in _VALID_RNA_BASES for base in codon):
    invalid_bases = ", ".join([base for base in codon if base not in _VALID_RNA_BASES])
    message = f"{ErrorMessage.CODON_HAS_INVALID_BASE.value}: {invalid_bases}"
    raise InvalidCodonError(
      message=message,
      status_code=400
    )
    
  name_index = 1
  match naming_type:
    case "short": name_index = 0
    case "3 letters": name_index = 1
    case "long": name_index = 2
    case _: naming_type = "3 letters"
  
  protein = _PROTEIN_CODON_REV_MAP.get(codon)
  synonymous_codons = list(_PROTEIN_CODON.get(protein))
  protein = protein[name_index] if protein else None
  
  return {
    "naming_type" : naming_type,
    "protein" : "No result" if protein is None else protein,
    "synonymous_codons" : "No result" if synonymous_codons is None else synonymous_codons
  }
