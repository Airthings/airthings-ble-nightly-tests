from enum import StrEnum


class SensorTypes(StrEnum):
    BATTERY = "battery"
    CO2 = "co2"
    HUMIDITY = "humidity"
    ILLUMINANCE = "illuminance"
    LUX = "lux"
    PRESSURE = "pressure"
    RADON_1DAY_AVG = "radon_1day_avg"
    RADON_LONGTERM_AVG = "radon_longterm_avg"
    SLA = "sla"
    TEMPERATURE = "temperature"
    VOC = "voc"


DEFAULT_SENSORS: list[SensorTypes] = [
    SensorTypes.HUMIDITY,
    SensorTypes.TEMPERATURE,
]

WAVE_GEN_1_SENSORS: list[SensorTypes] = [
    DEFAULT_SENSORS,
    SensorTypes.RADON_1DAY_AVG,
    SensorTypes.RADON_LONGTERM_AVG,
]

WAVE_RADON: list[SensorTypes] = [
    DEFAULT_SENSORS,
    SensorTypes.BATTERY,
    SensorTypes.ILLUMINANCE,
]

WAVE_PLUS: list[SensorTypes] = [
    WAVE_RADON,
    SensorTypes.CO2,
    SensorTypes.VOC,
]

WAVE_MINI: list[SensorTypes] = [
    DEFAULT_SENSORS,
    SensorTypes.BATTERY,
    SensorTypes.VOC,
]

WAVE_ENHANCE: list[SensorTypes] = [
    DEFAULT_SENSORS,
    SensorTypes.BATTERY,
    SensorTypes.CO2,
    SensorTypes.LUX,
    SensorTypes.PRESSURE,
    SensorTypes.SLA,
    SensorTypes.VOC,
]
