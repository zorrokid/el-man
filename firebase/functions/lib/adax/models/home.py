"""Models for Adax API home"""
from dataclasses import dataclass

@dataclass
class Home:
    """Represents home in Adax API."""
    id: int
    name: str

def home_from_dict(source: dict) -> Home:
    """Converts dictionary to Home."""
    return Home(source['id'], source['name'])
