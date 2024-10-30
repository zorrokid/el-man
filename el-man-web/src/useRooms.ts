import { getFirestore, collection, getDocs, Firestore, DocumentData } from 'firebase/firestore/lite';
import { useEffect, useState } from 'react';

export type Room = {
    id: number;
    heatingEnabled: boolean;
    homeId: number;
    name: string;
    targetTemperature: number;
    temperature: number;
}

const getRooms = async (db: Firestore) => {
    const querySnapshot = await getDocs(collection(db, 'Rooms'));
    const heatingSettings = querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
    }));
    return heatingSettings;
}

export const useRooms = () => {
    const [rooms, setRooms] = useState<Room[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const db = getFirestore();
    useEffect(() => {
        getRooms(db).then((s) => {
            let rooms = s.map((document: DocumentData) => ({
                id: parseInt(document.id),
                heatingEnabled: document.heatingEnabled,
                homeId: document.homeId,
                name: document.name,
                targetTemperature: document.targetTemperature,
                temperature: document.temperature
            }));
            setRooms(rooms);
            setIsLoading(false);
        });
    }, [db]);

    return { rooms, isLoading };

}