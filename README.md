# el-man

This application is for managing electricity feeding based on electricity prices.

The Day Ahead prices are fetched from [ENTSO-E Transparency Platorm](https://transparency.entsoe.eu/)

Note prices in result are in €/MWH withouth taxes. 

To get the actual electricity price in add taxes to result.

# Usage
    
Generate a token for [ENTSO-E Transparency Platform API](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_authentication)
    

Export the token as an environment variable

```bash
export TOKEN=<token>
```

Usage is:

```bash
python3 main.py <EIC code of the area> 
```

For example:

```bash
python3 main.py 10YFI-1--------U
```
