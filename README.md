# P.I.G. (Patron Image Generator)
 Creates Image(s) for Each Patron on Each Tier

## Prerequisites

Have the following installed on your system:

1. **[Python 3.10+](https://www.python.org/downloads/)**
2. **[Poetry (For installing required packages)](https://python-poetry.org/docs/#installation)**

## Required Packages

Using **[Poetry](https://python-poetry.org/docs/#installation)** (or manually), please install the following packages using `poetry install`: 

1. **[python-dotenv](https://pypi.org/project/python-dotenv/)**
2. **[Pillow](https://pypi.org/project/Pillow)**
3. **[Patreon](https://pypi.org/project/Patreon)**

## Configuration

In order to use the script, you will need to create a Client  on the **[Patreon Developer Portal](https://www.patreon.com/portal/registration/register-clients)** where you will obtain an **API Key**

Once you have done that, you will need to copy the API Key and paste it into a .env file in the top directory. Make sure the file contains the following:

```bash
PATREON={YOUR API KEY HERE}
```

A Default Configuration File will be provided, if not provided, a `config.json` file will need to be created at root, containting the following code for recommended settings:
```json
{
  "tiers": [
    "Tier 1",
    "Tier 2",
    "Tier 3",
    "Tier 4"
  ],
  "font-sizes": {
    "header1": 150,
    "header2": 75,
    "member-list": 55
  },
  "limit-per-column": 4,
  "output-directory": "./output",
  "loop": {
    "enabled": false,
    "wait-time": -1
  }
}
```
Make sure to adjust the `"tiers"` entry to fit your patreon, and everything else is also configurable to fit your needs

You will also need to specify the fonts you would like to use in the form of `.ttf` files in the `fonts` directory, one named `header.ttf` and another named `content.ttf` for their respective texts. (`FixedSys` Font will be provided by default)