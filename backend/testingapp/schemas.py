from pydantic import BaseModel

class GetStringResponse(BaseModel):
    result: str | None = None
    error: str | None = None

class UpdateStringRequest(BaseModel):
    signedTx: str
    address: str
    message: str
    signature: str