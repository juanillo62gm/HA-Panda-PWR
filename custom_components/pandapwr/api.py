"""API client for interacting with PandaPWR devices."""

import aiohttp
import async_timeout

HTTP_OK = 200


class PandaPWRApi:
    """API client for PandaPWR devices."""

    def __init__(self, ip_address: str) -> None:
        """Initialize the API client."""
        self._base_url = f"http://{ip_address}"
        self._session = aiohttp.ClientSession()

    async def test_connection(self) -> bool:
        """Test if the connection to the device can be established."""
        try:
            async with (
                async_timeout.timeout(10),
                self._session.get(f"{self._base_url}/update_ele_data") as response,
            ):
                return response.status == HTTP_OK
        except aiohttp.ClientError:
            return False

    async def get_data(self) -> dict:
        """Fetch data from the device."""
        try:
            async with (
                async_timeout.timeout(10),
                self._session.get(f"{self._base_url}/update_ele_data") as response,
            ):
                return await response.json()
        except aiohttp.ClientError:
            return {}

    async def set_power_state(self, state: int) -> bool:
        """Set power state (0 for off, 1 for on) using RAW payload."""
        payload = f"power={state}"
        try:
            async with (
                async_timeout.timeout(10),
                self._session.post(f"{self._base_url}/set", data=payload) as response,
            ):
                return response.status == HTTP_OK
        except aiohttp.ClientError:
            return False

    async def set_usb_state(self, state: int) -> bool:
        """Set USB state (0 for off, 1 for on) using RAW payload."""
        payload = f"usb={state}"
        try:
            async with (
                async_timeout.timeout(10),
                self._session.post(f"{self._base_url}/set", data=payload) as response,
            ):
                return response.status == HTTP_OK
        except aiohttp.ClientError:
            return False
