from elvia.error import MissingCredentialsException
from elvia.grid_tariff import GridTariff
from elvia.meter_value import MeterValue


class Elvia:
    def __init__(
        self,
        *,
        meter_value_token=None,
        grid_tariff_token=None,
        api_url="https://elvia.azure-api.net",
    ):
        self.meter_value_token = meter_value_token
        self.grid_tariff_token = grid_tariff_token
        self.api_url = api_url
        self.meter = None
        self.tariff = None

    def meter_value(self):
        if self.meter is None:
            if self.meter_value_token is None:
                raise MissingCredentialsException(
                    "meter_value_token is not set"
                )
            self.meter = MeterValue(
                self.api_url,
                self.meter_value_token,
            )
        return self.meter

    def grid_tariff(self):
        if self.tariff is None:
            if self.grid_tariff_token is None:
                raise MissingCredentialsException(
                    "grid_tariff_token is not set"
                )
            self.tariff = GridTariff(
                self.api_url,
                self.grid_tariff_token,
            )
        return self.tariff
