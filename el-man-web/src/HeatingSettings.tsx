import { RoomSettings } from "./RoomSettings";
import { useHeatingSettings } from "./useHeatingSettings";
import { useRooms } from "./useRooms";

export const HeatingSettings = () => {
    const { heatingSettings, isLoading: isLoadingHeatingSettings } = useHeatingSettings();
    const { rooms, isLoading: isLoadingRooms } = useRooms();
    if (isLoadingHeatingSettings || isLoadingRooms) return <p>Loading...</p>;
    return (
        <div>
            {
                rooms?.map((room) => {
                    return <RoomSettings room={room} settings={heatingSettings.get(room.id)} />;
                })
            }
        </div>
    )
}