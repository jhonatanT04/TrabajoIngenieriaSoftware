"""
Este archivo ahora solo mantiene una entrada que ejecuta la aplicación real
definida en `app/main.py`. La app principal y los modelos se movieron al paquete
`app` para un diseño más modular.
"""
from app.main import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)