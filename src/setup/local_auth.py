import os
from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
import bcrypt
from fastapi import HTTPException, status
from dotenv import load_dotenv

load_dotenv()

# Secret key to encode the JWT token
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-fallback-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

import logging

logger = logging.getLogger(__name__)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not plain_password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Central SSO / Keycloak JWT configurations
KEYCLOAK_ISSUER_URL = os.getenv("KEYCLOAK_ISSUER_URL")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_AUDIENCE = os.getenv("KEYCLOAK_AUDIENCE")
KEYCLOAK_JWKS_URI = os.getenv("KEYCLOAK_JWKS_URI")
try:
    KEYCLOAK_JWKS_CACHE_TTL_SECONDS = int(os.getenv("KEYCLOAK_JWKS_CACHE_TTL_SECONDS", "300"))
except ValueError:
    KEYCLOAK_JWKS_CACHE_TTL_SECONDS = 300

CENTRAL_JWT_SECRET = os.getenv("CENTRAL_JWT_SECRET")
CENTRAL_JWT_PUBLIC_KEY = os.getenv("CENTRAL_JWT_PUBLIC_KEY")
CENTRAL_ALGORITHM = os.getenv("CENTRAL_ALGORITHM", "HS256")

_jwks_client: Optional[jwt.PyJWKClient] = None
_jwks_client_url: Optional[str] = None

def get_jwks_client() -> Optional[jwt.PyJWKClient]:
    """
    Returns a cached PyJWKClient instance for Keycloak's JWKS endpoint.
    """
    global _jwks_client, _jwks_client_url
    issuer = os.getenv("KEYCLOAK_ISSUER_URL")
    jwks_uri = os.getenv("KEYCLOAK_JWKS_URI")
    if not jwks_uri and issuer:
        jwks_uri = f"{issuer.rstrip('/')}/protocol/openid-connect/certs"
    
    if not jwks_uri:
        return None
        
    if _jwks_client is None or _jwks_client_url != jwks_uri:
        try:
            ttl = int(os.getenv("KEYCLOAK_JWKS_CACHE_TTL_SECONDS", "300"))
        except ValueError:
            ttl = 300
        _jwks_client = jwt.PyJWKClient(
            jwks_uri,
            cache_keys=True,
            max_cached_keys=16,
            cache_jwk_set=True,
            lifespan=ttl,
        )
        _jwks_client_url = jwks_uri
    return _jwks_client

def decode_central_token(token: str) -> Optional[Dict]:
    """
    Decodes and validates a Keycloak OIDC token or centralized JWT.
    
    Validation order:
    1. Keycloak JWKS verification when KEYCLOAK_ISSUER_URL or KEYCLOAK_JWKS_URI is configured.
    2. Fallback to CENTRAL_JWT_PUBLIC_KEY or CENTRAL_JWT_SECRET for testing or local bridges.
    
    Returns the decoded claims dictionary if valid, None otherwise.
    """
    if not token or not isinstance(token, str):
        return None

    # 1. Attempt Keycloak OIDC JWKS validation if configured
    jwks_client = get_jwks_client()
    if jwks_client:
        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            issuer = os.getenv("KEYCLOAK_ISSUER_URL")
            audience = os.getenv("KEYCLOAK_AUDIENCE") or os.getenv("KEYCLOAK_CLIENT_ID")
            
            options = {
                "verify_signature": True,
                "verify_exp": True,
                "verify_iss": bool(issuer),
                "verify_aud": bool(audience),
            }
            
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256", "RS384", "RS512", "ES256", "ES384", "ES512"],
                issuer=issuer if issuer else None,
                audience=audience if audience else None,
                options=options,
            )
            return payload
        except jwt.PyJWTError as e:
            logger.debug(f"Keycloak JWKS token decode failed: {type(e).__name__}")
        except Exception as e:
            logger.warning(f"Unexpected error validating Keycloak token against JWKS: {type(e).__name__}")

    # 2. Fallback to configured central shared secret or public key
    key = os.getenv("CENTRAL_JWT_PUBLIC_KEY") or os.getenv("CENTRAL_JWT_SECRET")
    if key:
        try:
            algo = os.getenv("CENTRAL_ALGORITHM", "HS256")
            payload = jwt.decode(token, key, algorithms=[algo])
            return payload
        except jwt.PyJWTError:
            return None

    return None

