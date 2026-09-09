import re
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Union
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from backend.app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)

def get_password_hash(password: str) -> str:
    """Uses salted SHA256 for dependable zero-dependency hashing across all platforms."""
    salt = settings.SECRET_KEY[:16]
    return hashlib.sha256(f"{salt}{password}".encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    salt = settings.SECRET_KEY[:16]
    computed = hashlib.sha256(f"{salt}{plain_password}".encode("utf-8")).hexdigest()
    return computed == hashed_password

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Security & Prompt Injection Defense
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(previous|all|the\s+above)\s+instructions",
    r"you\s+are\s+now\s+in\s+dan\s+mode",
    r"system\s+prompt\s+override",
    r"disregard\s+(all\s+rules|safety)",
    r"reveal\s+(system\s+prompt|instructions|secret\s+key)",
    r"drop\s+table\s+",
    r"<\s*script\s*>",
]

def sanitize_and_check_injection(text: str) -> tuple[str, bool]:
    """
    Sanitizes user input and flags malicious prompt-injection or jailbreak patterns.
    Returns: (cleaned_text, is_suspicious)
    """
    if not text:
        return "", False
    
    cleaned = text.strip()
    is_suspicious = False
    
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            is_suspicious = True
            break
            
    return cleaned, is_suspicious
