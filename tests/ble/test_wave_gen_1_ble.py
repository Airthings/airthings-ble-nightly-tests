import logging
import pytest

from airthings_ble.device_type import AirthingsDeviceType
from airthings_ble.parser import AirthingsBluetoothDeviceData
from tests.ble.helpers import find_device_by_type

_LOGGER = logging.getLogger(__name__)

airthings = AirthingsBluetoothDeviceData(
    logger=_LOGGER,
    is_metric=True,
    max_attempts=1,
)


# Before all tests
def setup_module(module):
    """Setup module for tests."""
    return


@pytest.mark.asyncio
async def test_wave_gen_1_over_ble():
    """Test Wave Gen 1 over BLE."""
    # ble_device = await find_device(mac_address="00:11:22:33:44:55")
    ble_device = await find_device_by_type(
        device_type=AirthingsDeviceType.WAVE_GEN_1
    )

    assert ble_device is not None, "Device not found"

    # Check for exceptions during device update
    try:
        device = await airthings.update_device(ble_device=ble_device)
        assert device is not None, "Device updated"
    except Exception as e:
        pytest.fail(f"Exception occurred while updating device: {e}")
