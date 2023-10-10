# el-man

This application is for managing electricity feeding based on electricity prices.

The Day Ahead prices are fetched from [ENTSO-E Transparency Platorm](https://transparency.entsoe.eu/)

Export the token as an environment variable

```bash
export TOKEN=<token>
```

Usage is:

```bash
python3 main.py <EIC code of the area> <vat percentage> <UTC time difference in hours> 
```

Arguments are optional, default values are for Finland:
EIC code: 10YFI-1--------U
VAT percentage: 24
UTC time difference: 3

For example:

```bash
python3 main.py 10YFI-1--------U 24 3
```

There is also an example file if you don't have access to Entso-E API. Example data can be used with 'debug' argument:

```bash
python3 main.py <EIC code of the area> <vat percentage> <UTC time difference in hours> debug
```