import logging
import pytest

from airthings_ble.device_type import AirthingsDeviceType
from airthings_ble.parser import AirthingsBluetoothDeviceData
from tests.ble.helpers import (
    AirthingsScanner,
    sensors_types_from_device_type,
)

_LOGGER = logging.getLogger(__name__)

_WAVE_ENHANCE_EU_US = [
    AirthingsDeviceType.WAVE_ENHANCE_EU,
    AirthingsDeviceType.WAVE_ENHANCE_US,]


@pytest.mark.asyncio
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.parametrize(
    "device_type,is_metric",
    [
        (AirthingsDeviceType.WAVE_GEN_1, True),
        (AirthingsDeviceType.WAVE_GEN_1, False),
        (AirthingsDeviceType.WAVE_RADON, True),
        (AirthingsDeviceType.WAVE_RADON, False),
        (AirthingsDeviceType.WAVE_PLUS, True),
        (AirthingsDeviceType.WAVE_PLUS, False),
        (AirthingsDeviceType.WAVE_MINI, True),
        (AirthingsDeviceType.WAVE_ENHANCE_EU, True),
    ],
)
async def test_update_device_over_ble(
    device_type: AirthingsDeviceType,
    is_metric: bool,
):
    """Test Wave Gen 1 over BLE."""
    scanner = AirthingsScanner(device_type=device_type)

    ble_device = await scanner.find_device_by_type(timeout=30)

    airthings = AirthingsBluetoothDeviceData(
        logger=_LOGGER,
        is_metric=is_metric,
    )

    assert ble_device is not None, "Device not found"

    try:
        device = await airthings.update_device(ble_device=ble_device)
    except Exception as e:
        pytest.fail(f"Exception occurred while updating device: {e}")

    if device_type in _WAVE_ENHANCE_EU_US:
        assert device.model in _WAVE_ENHANCE_EU_US, (
            f"Device type mismatch, expected one of: "
            f"{', '.join(map(str, _WAVE_ENHANCE_EU_US))}, got: {device.model}"
        )
    else:
        assert device.model == device_type, (
            f"Device type mismatch, expected: {device_type}, got: {device.model}"
        )

    assert device.sensors, "No sensors found in device"

    expected_sensors = sensors_types_from_device_type(device.model)
    assert len(device.sensors) >= len(expected_sensors), (
        f"Found {len(device.sensors)} sensors, expected at least "
        f"{', '.join(expected_sensors)} sensors"
    )

    # Ensure all expected sensors are present in the device
    def flatten_sensors(sensors):
        """Recursively flatten a list of sensors."""
        for sensor in sensors:
            if isinstance(sensor, list):
                yield from flatten_sensors(sensor)
            else:
                yield sensor

    flat_expected_sensors = list(flatten_sensors(expected_sensors))

    missing_sensors = [
        sensor for sensor
        in flat_expected_sensors
        if sensor not in device.sensors
    ]
    if missing_sensors:
        pytest.fail(
            f"Missing sensors in device: {', '.join(str(s) for s in missing_sensors)}"
            f", found: {', '.join(device.sensors)}"
        )

    # Optionally, log found sensors for debugging
    for sensor in flat_expected_sensors:
        _LOGGER.debug(f"Verified sensor present: {sensor}")
