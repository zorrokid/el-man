from models.home import Home
from models.device import from_dict as device_from_dict
from models.room import Room
from services.constants import HOUSE_INFO_COLLECTION


def get_homes(firestore_client) -> list[Home]:
    homes_list = []
    home_docs_ref = firestore_client.collection(HOUSE_INFO_COLLECTION)
    home_docs = home_docs_ref.stream()
    for home_doc in home_docs:
        rooms = []
        room_docs_ref = home_docs_ref.document(home_doc.id).collection("rooms")
        room_docs = room_docs_ref.stream()
        for room_doc in room_docs:
            devices = []
            devices_stream = room_docs_ref.document(room_doc.id).collection("devices").stream()
            for device in devices_stream:
                devices.append(device_from_dict(device.to_dict()))
            room_dict = room_doc.to_dict()
            room = Room(room_doc.id, room_dict['name'], room_dict['heatingEnabled'], room_dict['temperature'], devices)
            rooms.append(room)
        home_dict = home_doc.to_dict()
        price_max = home_dict['price_max'] if 'price_max' in home_dict else None
        home = Home(home_doc.id, home_dict['name'], price_max, rooms)
        homes_list.append(home)
    return homes_list
        


