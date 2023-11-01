"""Models for Adax API credentials."""
from dataclasses import dataclass
@dataclass
class ApiCredentials:
    """Represents credentials in Adax API."""
    credentials: str
    client_id: str
