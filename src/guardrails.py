
import re
from fastapi import HTTPException, Request
from datetime import datetime, timedelta

# Rate limiting configuration
RATE_LIMIT = 60  # max requests per minute
request_counts = {}

# PII detection patterns
PII_PATTERNS = [
    r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
    r"\b\d{4}-\d{4}-\d{4}-\d{4}\b",  # Credit Card
    r"\b\d{3}-\d{3}-\d{4}\b",  # Phone Number
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"  # Email
]

# Toxicity patterns
TOXICITY_PATTERNS = [
    "hate", "violence", "abuse"
]


def check_pii(text: str):
    """Check for PII in the input text and raise an exception if found."""
    for pattern in PII_PATTERNS:
        if re.search(pattern, text):
            raise HTTPException(status_code=400, detail="PII detected in input.")


def check_toxicity(text: str):
    """Check for toxic content in the input text and raise an exception if found."""
    for pattern in TOXICITY_PATTERNS:
        if pattern in text.lower():
            raise HTTPException(status_code=400, detail="Toxic content detected in input.")


def rate_limit(request: Request):
    """Rate limit requests based on client IP."""
    client_ip = request.client.host
    now = datetime.now()
    if client_ip not in request_counts:
        request_counts[client_ip] = []
    # Remove outdated requests
    request_counts[client_ip] = [timestamp for timestamp in request_counts[client_ip] if timestamp > now - timedelta(minutes=1)]
    # Check rate limit
    if len(request_counts[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")
    # Record new request
    request_counts[client_ip].append(now)
