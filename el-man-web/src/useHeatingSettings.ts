import { getFirestore, collection, getDocs, Firestore, DocumentData } from 'firebase/firestore/lite';
import { useEffect, useState } from 'react';

export type HeatingSettings = {
    id: number;
    heatingEnabled: boolean;
    lowPrice: number;
    maxPrice: number;
    heatingMaxTemperature: number;
    heatingMinTemperature: number;
    heatingMidTemperature: number;
}

const getHeatingSettings = async (db: Firestore) => {
    const querySnapshot = await getDocs(collection(db, 'HeatingSettings'));
    const heatingSettings = querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
    }));
    return heatingSettings;
}

export const useHeatingSettings = () => {
    const [heatingSettings, setHeatingSettings] = useState<Map<number, HeatingSettings>>(new Map<number, HeatingSettings>());
    const [isLoading, setIsLoading] = useState(true);
    const db = getFirestore();
    useEffect(() => {
        getHeatingSettings(db).then((s) => {
            let settings = s.reduce((map: Map<number, HeatingSettings>, setting: DocumentData) => {
                // setting.id is same as room.id and can be used to map the settings to the rooms
                map.set(parseInt(setting.id), {
                    id: parseInt(setting.id),
                    heatingEnabled: setting.heatingEnabled,
                    lowPrice: setting.lowPrice,
                    maxPrice: setting.maxPrice,
                    heatingMaxTemperature: setting.heatingMaxTemperature,
                    heatingMinTemperature: setting.heatingMinTemperature,
                    heatingMidTemperature: setting.heatingMidTemperature
                });
                return map;
            }, new Map<number, HeatingSettings>());
            setHeatingSettings(settings);
            setIsLoading(false);
        });
    }, [db]);
    return { heatingSettings, isLoading };
}