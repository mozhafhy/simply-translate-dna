from typing import TypedDict

class BaseResponse(TypedDict):
  status_code: int

class ErrorResponse(BaseResponse):
  """
  ### Value:
  ```
  {
    "status_code" : int,
    "error" : str
  }
  ```
  """
  error: str

class SuccessResponse(BaseResponse):
  """
  ### Value:
  ```
  {
    "status_code" : int,
    "data" : object
  }
  ```
  """
  data: object
  