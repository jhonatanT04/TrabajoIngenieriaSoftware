import warnings

# Silence httpx deprecation about 'app' shortcut used by Starlette TestClient
warnings.filterwarnings(
    "ignore",
    message="The 'app' shortcut is now deprecated",
    category=DeprecationWarning,
)
