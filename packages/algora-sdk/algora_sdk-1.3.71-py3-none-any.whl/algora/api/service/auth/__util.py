from typing import Optional


def _login_request_info(username: str, password: str, scope: Optional[str] = None) -> dict:
    data = {
            "client_id": "algora-api",
            "grant_type": "password",
            "username": username,
            "password": password
        }
    if scope is not None:
        data.update({'scope': scope})

    return {
        "url": f"https://auth.algoralabs.com/auth/realms/production/protocol/openid-connect/token",
        'data': data
    }


def _refresh_token_request_info(refresh_token: Optional[str] = None) -> dict:
    return {
        "url": f"https://auth.algoralabs.com/auth/realms/production/protocol/openid-connect/token",
        "data": {
            "client_id": "algora-api",
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
    }
