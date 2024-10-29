import { useHeatingSettings } from "./useHeatingSettings";

export const HeatingSettings = () => {
    const {heatingSettings}  = useHeatingSettings();
    return (
        <div>
            <h2>Heating Settings</h2>
            <p>{heatingSettings?.map((setting) => <div>{
                Object.entries(setting).map(([key, value]) => <div>{key}: {value}</div>)
                }</div>)}</p>
        </div>
    )
}