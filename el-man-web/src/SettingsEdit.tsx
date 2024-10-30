import { useState } from "react";
import { HeatingSettings } from "./useHeatingSettings";
import { useEditSettings } from "./useEditSettings";

type SettingsEditProps = {
    settings: HeatingSettings;
}

export const SettingsEdit = ({ settings }: SettingsEditProps) => {
    const { heatingEnabled, lowPrice, maxPrice, heatingMaxTemperature, heatingMinTemperature, heatingMidTemperature, setHeatingEnabled, setLowPrice, setMaxPrice, setHeatingMaxTemperature, setHeatingMidTemperature,setHeatingMinTemperature, saveSettings, isSaving } = useEditSettings(settings);
    return (
        <div>
            <CheckBoxInput label="Heating enabled" value={heatingEnabled} onChange={setHeatingEnabled} />
            <NumberInput label="Low price" value={lowPrice} onChange={setLowPrice} />
            <NumberInput label="Max price" value={maxPrice} onChange={setMaxPrice} />
            <NumberInput label="Max temperature" value={heatingMaxTemperature} onChange={setHeatingMaxTemperature} />
            <NumberInput label="Mid temperature" value={heatingMidTemperature} onChange={setHeatingMidTemperature} />
            <NumberInput label="Min temperature" value={heatingMinTemperature} onChange={setHeatingMinTemperature} />
            <button onClick={saveSettings} disabled={isSaving}>Save</button>
        </div>
    );
}

type NumberInputProps = {
    value: number,
    onChange: (value: number) => void,
    label: string,
}

const NumberInput = ({ value, onChange, label }: NumberInputProps) => {
    return (
        <label>
            {label}:
            <input type="number" value={value} onChange={(ev) => onChange(ev.target.valueAsNumber)} />
        </label>
    );
}

type CheckBoxInputProps = {
    value: boolean,
    onChange: (value: boolean) => void,
    label: string,
}

const CheckBoxInput = ({ value, onChange, label }: CheckBoxInputProps) => {
    return (
        <label>
            {label}:
            <input type="checkbox" checked={value} onChange={(ev) => onChange(ev.target.checked)} />
        </label>
    );
}