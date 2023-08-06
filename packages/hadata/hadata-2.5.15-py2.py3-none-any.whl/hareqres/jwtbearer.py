import hashlib
import json
import os
import datetime
from typing import Dict

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, Depends
from hautils.logger import logger
from dotenv import load_dotenv
import jwt
import time

from hautils.web import exception_log

load_dotenv(override=False)

from hadata.user import MongoUser

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer,
            self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403,
                                    detail="Invalid authentication scheme.")
            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403,
                                    detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403,
                                detail="Invalid authorization code.")


def verify_jwt(token_jwt: str) -> bool:
    is_token_valid: bool = False
    logger.info("verify jwt token %s" % (token_jwt,))
    try:
        payload = decode_jwt(token_jwt)
    except Exception:
        logger.info("payload exception")
        payload = None
    if payload:
        is_token_valid = True
    logger.info("payload status %s" % (is_token_valid,))
    return is_token_valid


def encode_jwt(payload):
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception:
        return {}


def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=120)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


# whats the point of creating dictionaries to communicate a single value
async def get_user(token: str = Depends(JWTBearer())) -> dict:
    payload = decode_jwt(token)
    return {
        "email": payload.get("user_id")
    }


def authenticate_user(email, password):
    hashed = hashlib.sha256(password.encode('utf-8'))
    hashed_password = hashed.hexdigest()
    logger.debug("authentication %s %s" % (password, hashed_password))
    user = MongoUser.objects(
        email=email,
        password=hashed_password,
        is_verified=True).first()
    if user is None:
        logger.warn("authentication failure %s" % (email,))
        raise Exception

    return True


async def get_mongo_user(token: str = Depends(JWTBearer())) -> dict:
    payload = decode_jwt(token)
    return MongoUser.objects(email=payload.get("user_id")).first()


async def verify_token(token: str):
    logger.info("verifying token %s " % (token,))
    try:
        payload = decode_jwt(token)
        logger.debug("verify token %s" % (json.dumps(payload)))
        return MongoUser.objects(email=payload.get("email")).first()
    except Exception as e:
        exception_log(e)

    raise Exception
