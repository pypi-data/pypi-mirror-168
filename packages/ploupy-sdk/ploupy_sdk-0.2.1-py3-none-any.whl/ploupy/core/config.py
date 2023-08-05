"""
Contains global configurations flags
"""

VERSION: str = "0.2.1"
"""
SDK version
"""

FLAG_DEPLOY: bool = True
"""
Flag that indicates whether the SDK is deploy or dev mode
"""

URL_SIO_DEV = "http://127.0.0.1:8000"
URL_SIO_PROD = "https://ploupy-socketio-production.up.railway.app"

URL_SIO = URL_SIO_PROD if FLAG_DEPLOY else URL_SIO_DEV
"""
Url of the socket-io server
"""
