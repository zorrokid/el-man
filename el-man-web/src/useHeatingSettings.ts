
import { getFirestore, collection, getDocs, Firestore, DocumentData } from 'firebase/firestore/lite';
import { useEffect, useState } from 'react';

    const getHeatingSettings = async (db: Firestore) => {
        const querySnapshot = await getDocs(collection(db, 'HeatingSettings'));
        const heatingSettings = querySnapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
        }));
        return heatingSettings;
    }


export const useHeatingSettings = () => {
    const [heatingSettings, setHeatingSettings] = useState<DocumentData[]| undefined>(undefined);
    const db = getFirestore();
    useEffect(() => {
        getHeatingSettings(db).then((s) => setHeatingSettings(s));
    }, [db]);
    return { heatingSettings};
}