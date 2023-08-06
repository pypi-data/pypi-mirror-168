from typing import List
from typing_extensions import TypedDict


class TariffType(TypedDict):
    tariffKey: str
    company: str
    customerType: str
    title: str
    resolution: int
    description: str


class TariffTypeResponse(TypedDict):
    tariffTypes: List[TariffType]


class PriceLevel(TypedDict):
    level: str
    levelInfo: str
    total: float
    fixed: float
    taxes: float
    currency: str
    uom: str


class FixedPrice(TypedDict):
    priceLevel: PriceLevel


class VariablePrice(TypedDict):
    total: float
    energy: float
    power: float
    taxes: float
    level: str
    currency: str
    uom: str


class PriceInfo(TypedDict):
    startTime: str
    expiredAt: str
    hoursShortName: str
    publicHoliday: bool
    fixedPrices: List[FixedPrice]
    variablePrice: VariablePrice


class TariffPrice:
    priceInfo: List[PriceInfo]


class GridTariff(TypedDict):
    tariffType: TariffType
    tariffPrice: TariffPrice


class GridTariffCollection(TypedDict):
    gridTariff: GridTariff
    meteringPointIds: List[str]


class TariffForMeteringPointsResponse(TypedDict):
    gridTariffCollections: List[GridTariffCollection]


class TariffQueryResponse(TypedDict):
    gridTariff: GridTariff
