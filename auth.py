import jwt
from datetime import datetime, timedelta

SECRET_KEY = "SGC_PARAGUAY_2026_SECURITY_PRO_KEY_32"
ALGORITHM = "HS256"

def crear_token_acceso(datos: dict):
    payload = datos.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=60)
    payload.update({"exp": expiracion})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def validar_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None