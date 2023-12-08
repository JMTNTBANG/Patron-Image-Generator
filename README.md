# Patron Image Generator
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