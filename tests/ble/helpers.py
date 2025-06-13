import asyncio
from bleak import BleakScanner, BLEDevice
from bleak.backends.scanner import AdvertisementData

from airthings_ble.device_type import AirthingsDeviceType
from tests.ble.const import (
    WAVE_GEN_1_SENSORS,
    WAVE_RADON,
    WAVE_PLUS,
    WAVE_MINI,
    WAVE_ENHANCE,
)


class AirthingsScanner:
    """Scanner for Airthings BLE devices."""

    def __init__(self, device_type: AirthingsDeviceType):
        """Initialize the scanner with a specific device type."""
        self.device_type = device_type

    def _device_filter(
        self,
        device: BLEDevice,
        advertisement_data: AdvertisementData
    ) -> bool:
        """Check if the device matches the filter."""
        # Double check manufacturer id (820)
        if advertisement_data.manufacturer_data.get(820) is None:
            return False
        uuids = advertisement_data.service_uuids
        if self.device_type == AirthingsDeviceType.WAVE_GEN_1:
            return "b42e1f6e-ade7-11e4-89d3-123b93f75cba" in uuids
        if self.device_type == AirthingsDeviceType.WAVE_RADON:
            return "b42e4a8e-ade7-11e4-89d3-123b93f75cba" in uuids
        if self.device_type == AirthingsDeviceType.WAVE_PLUS:
            return "b42e1c08-ade7-11e4-89d3-123b93f75cba" in uuids
        if self.device_type == AirthingsDeviceType.WAVE_MINI:
            return "b42e3882-ade7-11e4-89d3-123b93f75cba" in uuids
        if (
            self.device_type == AirthingsDeviceType.WAVE_ENHANCE_EU
            or self.device_type == AirthingsDeviceType.WAVE_ENHANCE_US
        ):
            return (
                "b42eb4a6-ade7-11e4-89d3-123b93f75cba" in uuids
                # and "Tern" in device.name
            )
        return False

    async def find_device_by_type(self) -> BLEDevice | None:
        """Find a device of a specific type in a list of devices."""
        return await BleakScanner.find_device_by_filter(
            self._device_filter,
            timeout=10
        )


def sensors_types_from_device_type(device_type: AirthingsDeviceType) -> list[str]:
    """Return the number of sensors for a specific device type."""
    if device_type == AirthingsDeviceType.WAVE_GEN_1:
        return WAVE_GEN_1_SENSORS
    if device_type == AirthingsDeviceType.WAVE_RADON:
        return WAVE_RADON
    if device_type == AirthingsDeviceType.WAVE_PLUS:
        return WAVE_PLUS
    if device_type == AirthingsDeviceType.WAVE_MINI:
        return WAVE_MINI
    if (
        device_type == AirthingsDeviceType.WAVE_ENHANCE_EU
        or device_type == AirthingsDeviceType.WAVE_ENHANCE_US
    ):
        return WAVE_ENHANCE
    return 0


async def _main():
    """Main function for testing purposes."""
    scanner = AirthingsScanner(AirthingsDeviceType.WAVE_GEN_1)
    device = await scanner.find_device_by_type()
    if device:
        print(f"Found device: {device}")
    else:
        print("No device found.")


if __name__ == "__main__":
    asyncio.run(_main())
