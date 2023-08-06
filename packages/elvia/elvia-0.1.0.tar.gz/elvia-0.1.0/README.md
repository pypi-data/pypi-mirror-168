# Unofficial API bindings for Elvia's consumer facing APIs

![Build Status](https://github.com/andersem/elvia-python/actions/workflows/ci.yml/badge.svg)

With the Elvia API you can access information about your own power consumption and get the
current grid tariffes in Elvia's power grid.

## Installation

Install from pip by using:

```
pip install --upgrade elvia
```

### Requirements

- Python 3.6+

## Getting access tokens

Elvia's APIs are available for consumers using Elvia for their grid fees (nettleie).

The MeterValue and GridTariff APIs uses different authentication methods, and different tokens.

### Meter Value API

Get token using this guide: https://www.elvia.no/smart-forbruk/alt-om-din-strommaler/slik-gjor-du-det-aktivering-og-bruk-av-elvias-metervalueapi/

### Grid Tariff API

Get token by logging into https://elvia.portal.azure-api.net/signin and subscribe to the GridTariffAPI

## Using the API

```python
from elvia import Elvia
import json
import asyncio
import os

# token from elvia.no/minside
meter_value_token = os.environ.get("ELVIA_METER_VALUE_TOKEN")

# token from https://elvia.portal.azure-api.net/signin
grid_tariff_token = os.environ.get("ELVIA_GRID_TARIFF_TOKEN")

# the metering point id of your home
metering_point_id = os.environ.get("ELVIA_METERING_POINT_ID")

elvia = Elvia(meter_value_token = meter_value_token)

async def get_meter_values():
    meter_value_client = elvia.meter_value()
    meter_values = await meter_value_client.get_meter_values(
        start_time = "2021-12-08T01:00:00",
        end_time = "2021-12-08T02:00:00",
        metering_point_ids = [metering_point_id],
        include_production = True
    )
    print(json.dumps(meter_values))
asyncio.run(get_meter_values())

# And use it to get grid tariffs

elvia = Elvia(grid_tariff_token = grid_tariff_token)

async def get_grid_tariffs():
    grid_tariff_client = elvia.grid_tariff()

    grid_tariffs = await grid_tariff_client.grid_tariffs_for_metering_points(
        range = "today",
        metering_point_ids = [metering_point_id]
    )
    print(json.dumps(grid_tariffs))
asyncio.run(get_grid_tariffs())
```
