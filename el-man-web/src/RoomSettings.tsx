import { SettingsEdit } from "./SettingsEdit";
import { HeatingSettings } from "./useHeatingSettings";
import { Room } from "./useRooms";

type RoomSettingsProps = {
    room: Room;
    settings: HeatingSettings | undefined;
}

export const RoomSettings = ({ room, settings }: RoomSettingsProps) => {
    return (
        <div>
            <RoomInfo room={room} />
            {
                settings === undefined
                    ? <p>No settings found</p>
                    : <SettingsEdit settings={settings} />
            }
        </div>
    );
}

type RoomInfoProps = {
    room: Room;
}

export const RoomInfo = ({ room }: RoomInfoProps) => {
    return (
        <div>
            <h3>{room.name}</h3>
            <p>Temperature: {room.temperature}</p>
            <p>Target temperature: {room.targetTemperature}</p>
        </div>
    );
}

