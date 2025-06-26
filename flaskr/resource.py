from flask import (
  Blueprint, request, jsonify, Response
)
from pydantic import ValidationError
from dna import error_types as err
from dto.request_dto import *
from flaskr import middleware as mw
from flaskr import response_type as restype

bp = Blueprint("resource", __name__, url_prefix="/api")

# ! error handlers
@bp.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError) -> Response:
  error: restype.ErrorResponse = {
    "error" : e.errors(),
    "status_code" : 400
  }
  return jsonify(error), error["status_code"]

@bp.errorhandler(ValueError)
def handle_json_error(e: ValueError) -> Response:
  error: restype.ErrorResponse = {
    "error" : e.args[0],
    "status_code" : e.args[1]
  }
  return jsonify(error), error["status_code"]

@bp.errorhandler(err.MoleculeStructureError)
def handle_json_error(e: err.MoleculeStructureError) -> Response:
  error: restype.ErrorResponse = {
    "error" : e.args[0],
    "status_code" : 400
  }
  return jsonify(error), error["status_code"]

# ! transcribe
@bp.route("/transcribe", methods=["POST"])
def transcribe() -> Response:
  data = mw.safely_get_json(request=request)
  result = mw.process_transcribe_req(data)
  
  return jsonify(result["data"]), result["status_code"]

# ! translate
@bp.route("/translate", methods=["POST"])
def translate() -> Response:
  data = mw.safely_get_json(request=request)
  result = mw.process_translate_req(data)
  
  return jsonify(result["data"]), result["status_code"]
  
# ! RNA to DNA
@bp.route("/rna-to-dna", methods=["POST"])
def rna_to_dna() -> Response:
  data = mw.safely_get_json(request=request)
  result = mw.process_rna_to_dna_req(data)
  
  return jsonify(result["data"]), result["status_code"]
    
# ! codon to protein
@bp.route("/codon-to-protein", methods=["POST"])
def codon_to_protein() -> Response:
  data = mw.safely_get_json(request=request)
  result = mw.process_codon_to_protein(data)
  
  return jsonify(result["data"]), result["status_code"]
