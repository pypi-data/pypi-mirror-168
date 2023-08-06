import json
from typing import Any, Dict
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse
import aiohttp
from elvia.error import ElviaClientException

from elvia.request_handler import verify_response
from elvia.types.grid_tariff_types import (
    TariffForMeteringPointsResponse,
    TariffTypeResponse,
)


class GridTariff:
    """
    Elvia GridTariff client

    Contains methods to interact with the GridTariffApi
    """

    def __init__(
        self,
        api_url,
        token,
    ):
        self.api_url = api_url
        self.token = token

    async def grid_tariffs_for_metering_points(
        self,
        *,
        range: str = "today",
        start_time: str = None,
        end_time: str = None,
        metering_point_ids=[],
    ) -> TariffForMeteringPointsResponse:
        """
        Provides private grid tariffs.
        """
        url_base = f"{self.api_url}/grid-tariff/digin/api/1/tariffquery/meteringpointsgridtariffs"
        if len(metering_point_ids) == 0:
            raise ElviaClientException(
                "At least one metering_point_id is needed"
            )
        body = {"meteringPointIds": metering_point_ids}
        if start_time is not None and end_time is not None:
            body["startTime"] = start_time
            body["endTime"] = end_time
        elif start_time is not None or end_time is not None:
            raise ElviaClientException(
                "Use either range or both start_time and end_time"
            )
        elif range is not None:
            body["range"] = range
        else:
            raise ElviaClientException(
                "Use either range or both start_time and end_time"
            )

        async with aiohttp.ClientSession(
            headers={
                "X-API-Key": self.token,
                "Content-Type": "application/json",
            }
        ) as websession:
            response = await websession.post(
                url_base,
                data=json.dumps(
                    {"range": range, "meteringPointIds": metering_point_ids}
                ),
            )
            await verify_response(response, 200)
            return await response.json()

    async def tarifftypes(
        self,
    ) -> TariffTypeResponse:
        """
        Provides private tarifftypes.
        """
        url_base = f"{self.api_url}/grid-tariff/digin/api/1/tarifftype"
        async with aiohttp.ClientSession(
            headers={
                "X-API-Key": self.token,
                "Content-Type": "application/json",
            }
        ) as websession:
            response = await websession.get(url_base)
            await verify_response(response, 200)
            return await response.json()

    async def tariffquery(
        self,
        tariff_key: str,
        *,
        range: str = "today",
        start_time: str = None,
        end_time: str = None,
    ) -> Dict[str, Any]:
        """
        Provides private tarifftypes.
        """
        url_base = f"{self.api_url}/grid-tariff/digin/api/1/tariffquery"
        query = {"TariffKey": tariff_key}
        if start_time is not None and end_time is not None:
            query["startTime"] = start_time
            query["endTime"] = end_time
        elif start_time is not None or end_time is not None:
            raise ElviaClientException(
                "Use either range or both start_time and end_time"
            )
        elif range is not None:
            query["range"] = range
        else:
            raise ElviaClientException(
                "Use either range or both start_time and end_time"
            )
        url = urlparse(url_base)._replace(query=urlencode(query))

        async with aiohttp.ClientSession(
            headers={
                "X-API-Key": self.token,
                "Content-Type": "application/json",
            }
        ) as websession:
            response = await websession.get(urlunparse(url))
            await verify_response(response, 200)
            return await response.json()

    async def ping(
        self,
    ) -> bool:
        """
        Ping the GridTariffAPI to check if it is up
        """
        url_base = f"{self.api_url}/grid-tariff/Ping"
        async with aiohttp.ClientSession(
            headers={
                "X-API-Key": self.token,
            }
        ) as websession:
            response = await websession.get(url_base)
            await verify_response(response, 200)
            return True
