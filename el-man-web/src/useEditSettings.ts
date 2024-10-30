import { useState } from "react";
import { HeatingSettings } from "./useHeatingSettings"
import { getFirestore, doc, updateDoc } from "firebase/firestore/lite";

export const useEditSettings = (settings: HeatingSettings) => {
    const [heatingEnabled, setHeatingEnabled] = useState(settings.heatingEnabled);
    const [lowPrice, setLowPrice] = useState(settings.lowPrice);
    const [maxPrice, setMaxPrice] = useState(settings.maxPrice);
    const [heatingMaxTemperature, setHeatingMaxTemperature] = useState(settings.heatingMaxTemperature);
    const [heatingMinTemperature, setHeatingMinTemperature] = useState(settings.heatingMinTemperature);
    const [heatingMidTemperature, setHeatingMidTemperature] = useState(settings.heatingMidTemperature);
    const [isSaving, setIsSaving] = useState(false);

    const db = getFirestore();

    const saveSettings = async () => {
        setIsSaving(true);
        const settingsRef = doc(db, 'HeatingSettings', `${settings.id}`);
        updateDoc(settingsRef, {
            heatingEnabled,
            lowPrice,
            maxPrice,
            heatingMaxTemperature,
            heatingMinTemperature,
            heatingMidTemperature
        }).then(() => {
            setIsSaving(false);
        });
    }


    return {
        heatingEnabled,
        setHeatingEnabled,
        lowPrice,
        setLowPrice,
        maxPrice,
        setMaxPrice,
        heatingMaxTemperature,
        setHeatingMaxTemperature,
        heatingMinTemperature,
        setHeatingMinTemperature,
        heatingMidTemperature,
        setHeatingMidTemperature,
        saveSettings,
        isSaving,
    }

}