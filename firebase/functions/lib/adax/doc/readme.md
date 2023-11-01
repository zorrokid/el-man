from: https://adax.no/en/wi-fi/api-development/

# Obtaining Authentication Credentials Required for Adax API

Using the Adax WiFi application you can create and get the authentication token used for accessing the Adax API. You should use at least the Adax WiFi
app version 3.7. The authentication token can be accessed following those steps:

    Navigate to Account Tab,
    Select “Remote user client API”
    Select “Add Credential”
    Give some name to the created credential and copy the generated password.

# Using Adax API

The API provides 3 end points:

    /auth/ for authentication to the REST service.
    /rest/v1/control/ for controlling your rooms
    /rest/v1/content/ for getting rooms statuses. (add ?withEnergy=1 to get heaters power consumption for past hour)
    /rest/v1/energy_log/{roomId} – returns hourly energy log from current time back to 1 week for the specified room in 1h intervals.

Control and status endpoins accepts and returns json documents.