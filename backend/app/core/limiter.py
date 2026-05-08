"""
app.core.limiter

Rate limiter compartido para todos los routers.
Se importa desde aquí para evitar imports circulares.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
