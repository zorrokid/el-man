from lib.adax.adax_client import AdaxClient
from models.home import Home

def set_target_temperatures(homes: list[Home], price: float, adax_api_credentials: str, adax_client_id: str) -> None:
    print("Starting set_heaters")
    
    client = AdaxClient(adax_api_credentials, adax_client_id)
    token = client.get_token()

    for home in homes:
        print(f"Setting heaters for home {home.id}")
        price_max = home.price_max if home.price_max is not None else 0
        print(f"Max price  is {price_max}")
        for room in home.rooms:
            print(f"Setting heaters for room {room.id}")
            if price is None or price > price_max:
                print(f"Price is not available or or exceed maximum limit {price_max}, so turning heating off")
                client.set_heating_enabled(room.id, False, token)
            else:
                # TODO get target temperature from firestore
                # house info should be updated every hour
                print(f"Price {price} is lower than max price {price_max}, so turning heating on")
                client.set_room_target_temperature(room.id, 10 * 100, token)