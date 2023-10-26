from dataclasses import dataclass

@dataclass
class Home:
    id: int 
    name: str

def home_from_dict(source: dict) -> Home:
    return Home(source['id'], source['name'])
