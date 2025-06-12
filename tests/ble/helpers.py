from bleak import BleakScanner, BLEDevice
from bleak.backends.scanner import AdvertisementData

from airthings_ble.device_type import AirthingsDeviceType


async def find_device(
    mac_address: str,
) -> BLEDevice | None:
    """Find a device of a specific type in a list of devices."""
    return await BleakScanner.find_device_by_address(
        device_identifier=str,
        timeout=20,
        return_first=True,
    )


async def find_device_by_type(
    device_type: AirthingsDeviceType,
) -> BLEDevice | None:
    """Find a device of a specific type in a list of devices."""
    device_type
    return await BleakScanner.find_device_by_filter(
        _device_filter,
        timeout=20
    )


def _device_filter(device: BLEDevice, advertisement_data: AdvertisementData) -> bool:
    uuids = advertisement_data.service_uuids
    if "b42e1f6e-ade7-11e4-89d3-123b93f75cba" in uuids:
        return True
    return False
