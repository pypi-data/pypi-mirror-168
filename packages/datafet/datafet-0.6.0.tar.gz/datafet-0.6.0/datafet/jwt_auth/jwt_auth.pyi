from ..custom_types import CustomError as CustomError, JwtParam as JwtParam
from ecdsa import SigningKey as SigningKey, VerifyingKey as VerifyingKey
from typing import Any, Dict, Union

DEFAULT_ALGORITHM: str

def create_jwt(
    jwt_param: JwtParam,
    signing_key: SigningKey,
    audience: str,
    issuer: str,
    exp_days: int,
    algorithm=...,
) -> Union[str, CustomError]: ...
def decode_jwt(
    jwt_string: str, verifying_key: VerifyingKey, audience: str, algorithm=...
) -> Union[Dict[str, Any], CustomError]: ...
