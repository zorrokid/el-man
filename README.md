# el-man

This application is for managing electricity feeding based on electricity prices.

Currently implemented:
- fetching day ahead prices from [ENTSO-E Transparency Platorm](https://transparency.entsoe.eu/)
- parsing day ahead prices from response data

TODO:
- create a cloud function to fetch prices on daily basis
    - function stores results to cloud database
- create an app to fetch prices and settings from cloud database
    - app sets registered devices on / off based on hourly electricity price and price limits from settings

# Usage

You need a token to access the [ENTSO-E Transparency Platform RESTful API](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)

Export the token as an environment variable

```bash
export TOKEN=<token>
```

Usage is:
```bash
python3 main.py <EIC code of the area> <vat percentage> <UTC time difference in hours> 
```

Arguments are optional, default values are for Finland:
- EIC code: 10YFI-1--------U
- VAT percentage: 24
- UTC time difference: 3

For example:

```bash
python3 main.py 10YFI-1--------U 24 3
```

There is also an example file if you don't have access to Entso-E API. Example data can be used with 'debug' argument:

```bash
python3 main.py <EIC code of the area> <vat percentage> <UTC time difference in hours> debug
```
