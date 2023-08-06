from typing import List
from elvia.request_handler import verify_response
from elvia.types.max_hours_types import MaxHoursResponse
from elvia.types.meter_value_types import MeterValueResponse
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse
import aiohttp


class MeterValue:
    """
    Elvia MeterValue client

    Contains methods to interact with the MeterValueApi
    """

    def __init__(
        self,
        api_url,
        token,
    ):
        self.api_url = api_url
        self.token = token

    async def get_max_hours(
        self,
        *,
        calculate_time: str = None,
        metering_point_ids: List[str] = [],
        include_production: bool = False,
    ) -> MaxHoursResponse:
        """
        Get the hour for maximum consumption (or production)
        in the current and previous month.
        The calculation works on a volume time series than start
        at the 1st of the previous month and ends at the the current hour.

        The calculation uses Norwegian time, even if the input time is UTC.

        :calculate_time: Format - date-time (as date-time in RFC3339). Timestamp for when the max hour calculation should be done. This means the API will pretend to be at this timestamp when calculating. I.e. 2021-09-01T14:59:59+02:00. The value can at most be 3 years back in time. Default: Now (Norwegian time)
        :metering_point_ids - A comma separated list of meteringpointid's. If blank, value is fetched from the contracts related to the access token.
        :include_production - Indicates production or consumption. False = consumption Default: false.
        :return: metering points
        """
        url_base = f"{self.api_url}/customer/metervalues/api/v1/maxhours"

        query = {}
        if calculate_time is not None:
            query["calculateTime"] = calculate_time
        if len(metering_point_ids) > 0:
            query["meteringPointIds"] = ",".join(metering_point_ids)
        if include_production:
            query["includeProduction"] = include_production
        url = urlparse(url_base)._replace(query=urlencode(query))
        url_string = urlunparse(url)
        async with aiohttp.ClientSession(
            headers={
                "Authorization": "Bearer " + self.token,
            }
        ) as websession:
            response = await websession.get(url_string)
            await verify_response(response, 200)
            return await response.json()

    async def get_meter_values(
        self,
        *,
        start_time: str = None,
        end_time: str = None,
        metering_point_ids: List[str] = [],
        include_production: bool = False,
    ) -> MeterValueResponse:
        """
        Get metering volumes for the given metering points in the requested period.

        :start_time: Format - date-time (as date-time in RFC3339). From timestamp for consumption. I.e. 2021-09-01T00:00:00+02:00. This value can maximum be 3 years back in time. Default: Last midnight (Norwegian time)
        :end_time: Format - date-time (as date-time in RFC3339). To timestamp for consumption. I.e. 2021-09-02T00:00:00+02:00 The start-end time span can be maximum 1 year. Default: The last hour (Norwegian time)
        :metering_point_ids - A comma separated list of meteringpointid's. If blank, value is fetched from the contracts related to the access token.
        :include_production - Indicates production or consumption. False = consumption Default: false.
        :return: metering points
        """

        url_base = f"{self.api_url}/customer/metervalues/api/v1/metervalues"
        query = {}
        if start_time is not None:
            query["startTime"] = start_time
        if end_time is not None:
            query["endTime"] = end_time
        if len(metering_point_ids) > 0:
            query["meteringPointIds"] = ",".join(metering_point_ids)
        if include_production:
            query["includeProduction"] = include_production

        url = urlparse(url_base)._replace(query=urlencode(query))
        async with aiohttp.ClientSession(
            headers={
                "Authorization": "Bearer " + self.token,
            }
        ) as websession:
            response = await websession.get(urlunparse(url))
            await verify_response(response, 200)
            return await response.json()
