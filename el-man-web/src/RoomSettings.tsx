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
                    : <SettingsInfo settings={settings} />
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

type SettingsInfoProps = {
    settings: HeatingSettings;
}

export const SettingsInfo = ({ settings }: SettingsInfoProps) => {
    return (
        <div>
            <p>Heating enabled: {settings.heatingEnabled ? 'Yes' : 'No'}</p>
            <p>Low price: {settings.lowPrice}</p>
            <p>Max price: {settings.maxPrice}</p>
            <p>Heating max temperature: {settings.heatingMaxTemperature}</p>
            <p>Heating min temperature: {settings.heatingMinTemperature}</p>
            <p>Heating mid temperature: {settings.heatingMidTemperature}</p>
        </div>
    );
}