"""
This file provides logic for generating JWT tokens for Jitsi rooms.

- JWT (JSON Web Token) tokens authorize users to join Jitsi rooms.
- Payload contains user details, room info, and expiration time.
- Tokens are signed using a secret key from the settings.

This ensures only authorized users can access specific rooms.
"""

import jwt
import time
from app.config.settings import settings

def generate_jitsi_token(room_name: str, user_name: str) -> str:
    """
    Generate a JWT token to authenticate the user for a specific Jitsi room.
    
    Args:
        room_name (str): Name of the room to join.
        user_name (str): Name of the user joining the room.

    Returns:
        str: A signed JWT token valid for one hour.
    """
    payload = {
        "context": {"user": {"name": user_name}},  # User identity for the room
        "aud": "jitsi",  # Audience for which the token is intended
        "iss": "your-app",  # Issuer (can be customized)
        "room": room_name,  # Room the user will join
        "exp": int(time.time()) + 3600  # Token expiration (1 hour)
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")
