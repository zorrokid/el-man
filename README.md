# el-man

This application is for managing electric heating thermostates based on hourly electricity prices.

Currently implemented:
- Fetching day ahead prices from [ENTSO-E Transparency Platorm](https://transparency.entsoe.eu/) using their RESTful API
- Managing Adax thermostates using their [RESTful API](https://adax.no/en/wi-fi/api-development/)
- Storing data to Firebase Firestore
- Google Cloud Functions for triggering fetching day ahead prices and managing target temperature based on hourly prices
- Room specific heating settings

# System diagram


```mermaid
graph LR
    A[Google\n Cloud\n Functions]
    B[Entso-E\n Transparency\n Platform\n REST API]
    C[Adax\n REST\n API]
    D[Firebase\n Firestore]
    E[Heater\n thermostate]
    A -- set target\n temperature --> C
    C -- get room\n and device info --> A
    B -- get day\n ahead prices --> A
    A -- save prices --> D
    A -- save heating\n state --> D
    D -- get hourly\n price --> A
    D -- get heating\n settings --> A
    D -- get rooms --> A
    A -- save rooms\n and device info --> D
    C -- set target\n temperature --> E
 ```

# Usage
You need a 
- token to access the [ENTSO-E Transparency Platform RESTful API](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Adax API token and client id

# References
## Adax API

- https://api-1.adax.no/client-api/
- https://api-1.adax.no/client-api/openapi

## Shelly Plug-S

TODO: manage Shelly Plug-S

Device can be connected to Wi-Fi using Shelly app (select device > networks > Wi-Fi 1/2 > Enable > enter Wi-Fi credentials).

You get device IP from there.

Example requests:

```
curl http://192.168.1.105/relay/0?turn=on
curl http://192.168.1.105/relay/0?turn=off
```

Example response:

```json
{"ison":false,"has_timer":false,"timer_started":0,"timer_duration":0,"timer_remaining":0,"overpower":false,"source":"http"}
```
